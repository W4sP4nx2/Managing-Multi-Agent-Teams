"""Audit active curriculum links; apply only a reviewed, unchanged audit report.

The offline check never changes source files. Network checks are opt-in and do
not treat access restrictions or transport failures as proof a URL is dead.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
from html import escape, unescape
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Callable
from urllib.error import HTTPError, URLError
from urllib.parse import quote, unquote, urlsplit, urlunsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener
from zipfile import ZipFile

from markdown_it import MarkdownIt
from markdown_it.common.utils import unescapeAll

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_VERSION = 1
REDIRECTS = "_archive/documentation_before_hub/redirects.json"
EXCLUDED = {".git", ".venv", "venv", "node_modules", "__pycache__", ".cache", "dist", "output", ".test-results"}
SOURCE_SUFFIXES = {".md", ".html", ".htm", ".ipynb", ".pptx", ".svg"}
MARKDOWN = MarkdownIt("commonmark", {"html": True})


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _git(root: Path, *args: str) -> bytes | None:
    result = subprocess.run(["git", "-C", str(root), *args], stdout=subprocess.PIPE,
                            stderr=subprocess.DEVNULL, check=False)
    return result.stdout if result.returncode == 0 else None


def _inside(root: Path, path: Path) -> bool:
    return path.resolve().is_relative_to(root.resolve())


def _editable(root: Path, path: Path) -> bool:
    if not _inside(root, path):
        return False
    parts = path.resolve().relative_to(root.resolve()).parts
    return bool(parts) and parts[0] != "_archive" and not any(p in EXCLUDED for p in parts)


def discover_sources(root: Path) -> list[str]:
    """Derive the editable curriculum from its existing distribution contracts."""
    from tools.build_learner_pack import FILES
    import yaml

    names = set(FILES)
    names.update(p.relative_to(root).as_posix() for p in root.glob("*.md"))
    for pattern in ("slides/*.md", "leadership/**/*.md", "instructor/solutions/core*.md"):
        names.update(p.relative_to(root).as_posix() for p in root.glob(pattern))
    manifest_path = root / "notebook_manifest.yml"
    if manifest_path.exists():
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        names.update("notebooks/" + row["file"] for row in manifest.get("required_sequence", []))
        advanced = manifest.get("advanced_reference", {})
        if advanced.get("file"):
            names.add(advanced["file"])
    return sorted(name for name in names if Path(name).suffix.lower() in SOURCE_SUFFIXES
                  and (root / name).is_file() and not name.startswith("_archive/")
                  and _inside(root, root / name))


@dataclass
class Reference:
    target: str
    start: int
    end: int
    wrapper_start: int
    wrapper_end: int
    label_start: int
    label_end: int
    kind: str = "markdown"
    label: str = ""
    definition: bool = False
    extra: dict = field(default_factory=dict)


@dataclass
class Document:
    source: str
    origin: str
    text: str
    kind: str = "markdown"
    cell: str | None = None
    cell_index: int | None = None
    offsets: list[int] | None = None
    member: str | None = None
    references: list[Reference] = field(default_factory=list)


def _line_starts(text: str) -> list[int]:
    return [0] + [m.end() for m in re.finditer("\n", text)]


def _normalize_label(text: str) -> str:
    return " ".join(unescapeAll(text).split()).upper()


def _destination(text: str, position: int) -> tuple[int, int, int] | None:
    """Return destination start/end and position after it, with balanced () support."""
    i = position
    while i < len(text) and text[i].isspace():
        i += 1
    if i >= len(text):
        return None
    if text[i] == "<":
        start = i + 1
        i += 1
        while i < len(text):
            if text[i] == "\\":
                i += 2
            elif text[i] == ">":
                return start, i, i + 1
            elif text[i] in "\n<":
                return None
            else:
                i += 1
        return None
    start, depth = i, 0
    while i < len(text):
        if text[i] == "\\":
            i += 2
            continue
        if text[i] == "(":
            depth += 1
        elif text[i] == ")":
            if depth == 0:
                break
            depth -= 1
        elif text[i].isspace() and depth == 0:
            break
        i += 1
    return (start, i, i) if depth == 0 else None


def _bracket_end(text: str, start: int, masked: list[bool]) -> int | None:
    depth, i = 1, start + 1
    while i < len(text):
        if text[i] == "\\":
            i += 2
            continue
        if not masked[i]:
            if text[i] == "[":
                depth += 1
            elif text[i] == "]":
                depth -= 1
                if depth == 0:
                    return i
        i += 1
    return None


def _same_url(left: str, right: str) -> bool:
    return unquote(unescape(unescapeAll(left))) == unquote(unescape(right))


def markdown_references(text: str) -> list[Reference]:
    """Use CommonMark recognition plus source spans, keeping unrelated bytes intact."""
    env: dict = {}
    tokens = MARKDOWN.parse(text, env)
    lines = _line_starts(text)
    masked = [False] * len(text)

    def mask(start: int, end: int) -> None:
        masked[start:end] = [True] * (end - start)

    for token in tokens:
        if token.type in {"fence", "code_block"} and token.map:
            a, b = token.map
            mask(lines[a], lines[b] if b < len(lines) else len(text))
    # Backtick spans and HTML tag attributes are not Markdown destinations.
    for match in re.finditer(r"(`+)([\s\S]*?)(?<!`)\1(?!`)", text):
        if not masked[match.start()]:
            mask(match.start(), match.end())
    for match in re.finditer(r"<(pre|code|script|style)\b[^>]*>[\s\S]*?</\1\s*>", text, re.I):
        mask(match.start(), match.end())
    for match in re.finditer(r"<!--([\s\S]*?)-->|</?[A-Za-z][A-Za-z0-9-]*(?=[\s/>])[^>]*>", text):
        mask(match.start(), match.end())

    references: list[Reference] = []
    definitions: dict[str, Reference] = {}
    for label, row in env.get("references", {}).items():
        a, b = row["map"]
        start, end = lines[a], lines[b] if b < len(lines) else len(text)
        prefix = re.match(r" {0,3}\[[^\]\n]+\]:", text[start:end])
        if prefix:
            span = _destination(text, start + prefix.end())
            if span:
                ds, de, _ = span
                ref = Reference(row["href"], ds, de, start, end, start, start,
                                definition=True, kind="definition")
                definitions[label] = ref
                references.append(ref)
        mask(start, end)

    for match in re.finditer(r"!?\[", text):
        start = match.start()
        bracket = match.end() - 1
        if masked[start] or (start and text[start - 1] == "\\"):
            continue
        # Do not also interpret the '[' in an image as a shortcut reference.
        if text[start] == "[" and start and text[start - 1] == "!":
            continue
        end_label = _bracket_end(text, bracket, masked)
        if end_label is None:
            continue
        cursor = end_label + 1
        is_image = text[start] == "!"
        raw_label = text[bracket + 1:end_label]
        if cursor < len(text) and text[cursor] == "(":
            span = _destination(text, cursor + 1)
            if not span:
                continue
            ds, de, cursor = span
            while cursor < len(text) and text[cursor].isspace():
                cursor += 1
            if cursor < len(text) and text[cursor] in "\"'(":
                closing = ")" if text[cursor] == "(" else text[cursor]
                cursor += 1
                while cursor < len(text) and text[cursor] != closing:
                    cursor += 2 if text[cursor] == "\\" else 1
                cursor += 1
                while cursor < len(text) and text[cursor].isspace():
                    cursor += 1
            if cursor >= len(text) or text[cursor] != ")":
                continue
            wrapper_end = cursor + 1
            children = MARKDOWN.parseInline(text[start:wrapper_end], env)[0].children or []
            kind = "image" if is_image else "link_open"
            parsed = next((t for t in children if t.type == kind), None)
            target = parsed.attrGet("src" if is_image else "href") if parsed else None
            if target is None or not _same_url(text[ds:de], target):
                continue
            references.append(Reference(target, ds, de, start, wrapper_end, bracket + 1,
                                        end_label, label=raw_label,
                                        kind="image" if is_image else "markdown"))
        else:
            reference_label = raw_label
            wrapper_end = cursor
            if cursor < len(text) and text[cursor] == "[":
                end_ref = _bracket_end(text, cursor, masked)
                if end_ref is None:
                    continue
                reference_label = text[cursor + 1:end_ref] or raw_label
                wrapper_end = end_ref + 1
                # The identifier in [label][identifier] is part of this link,
                # not a second shortcut link on the next scanner iteration.
                mask(cursor, wrapper_end)
            definition = definitions.get(_normalize_label(reference_label))
            if definition:
                children = MARKDOWN.parseInline(text[start:wrapper_end], env)[0].children or []
                if any(t.type == ("image" if is_image else "link_open") for t in children):
                    references.append(Reference(definition.target, definition.start, definition.end,
                                                start, wrapper_end, bracket + 1, end_label,
                                                kind="reference", label=raw_label,
                                                extra={"definition_start": definition.wrapper_start}))
    for match in re.finditer(r"<(https?://[^<>\s]+)>", text, re.I):
        if not masked[match.start()]:
            references.append(Reference(unescape(match.group(1)), match.start(1), match.end(1),
                                        match.start(), match.end(), match.start(1), match.end(1),
                                        kind="autolink", label=match.group(1)))
    return sorted(references, key=lambda ref: (ref.wrapper_start, ref.start, ref.kind))


def static_path_references(text: str, wrapped: list[Reference]) -> list[Reference]:
    """Recognize literal paths in prose code spans, not executable examples."""
    references = []
    line_offsets = _line_starts(text)
    suffixes = {".md", ".mdx", ".ipynb", ".py", ".pptx", ".pdf", ".svg", ".png",
                ".html", ".txt", ".json", ".yaml", ".yml", ".sh", ".xlsx", ".mjs"}
    tokens = MARKDOWN.parse(text)
    examples = "\n".join(token.content for token in tokens if token.type in {"fence", "code_block"})
    for token in tokens:
        if token.type != "inline" or not token.map or not token.children:
            continue
        allowed = {c.content for c in token.children if c.type == "code_inline"}
        if not allowed:
            continue
        start_line, end_line = token.map
        start = line_offsets[start_line]
        end = line_offsets[end_line] if end_line < len(line_offsets) else len(text)
        for match in re.finditer(r"(`+)([^`\n]+)\1", text[start:end]):
            target = match.group(2)
            if (target not in allowed or any(ch in target for ch in "*?{}[]()<>\n")
                    or any(ch.isspace() for ch in target)):
                continue
            parts = urlsplit(target)
            path = unquote(parts.path).replace("\\", "/")
            if parts.scheme or parts.netloc or path.startswith("/") or Path(path).suffix.lower() not in suffixes:
                continue
            if any(p in EXCLUDED for p in Path(path).parts) or path.startswith((".env", "/tmp/", "tmp/")):
                continue
            if re.search(r"(?<![\w/])" + re.escape(target) + r"(?![\w/])", examples):
                # A file named in an executable/example block can be created
                # inside a disposable exercise rather than in this repository.
                continue
            ws, we = start + match.start(), start + match.end()
            if any(ref.wrapper_start <= ws < ref.wrapper_end for ref in wrapped):
                continue
            line = text[text.rfind("\n", 0, ws) + 1:text.find("\n", we) if "\n" in text[we:] else len(text)]
            if re.search(r"\b(example|illustrative|placeholder|proposed|such as)\b|e\.g\.", line, re.I):
                continue
            ds, de = start + match.start(2), start + match.end(2)
            references.append(Reference(target, ds, de, ws, we, ds, de, kind="static", label=target))
    return references


class HTMLReferences(HTMLParser):
    def __init__(self, text: str):
        super().__init__(convert_charrefs=False)
        self.text = text
        self.lines = _line_starts(text)
        self.references: list[Reference] = []
        self.ids: set[str] = set()
        self.open_links: list[Reference] = []
        self.skip: list[str] = []

    def position(self) -> int:
        row, col = self.getpos()
        return self.lines[row - 1] + col

    def handle_starttag(self, tag: str, attrs: list) -> None:
        start = self.position()
        raw = self.get_starttag_text()
        attrs_dict = dict(attrs)
        if attrs_dict.get("id"):
            self.ids.add(attrs_dict["id"])
        if tag == "a" and attrs_dict.get("name"):
            self.ids.add(attrs_dict["name"])
        if tag in {"pre", "code", "script", "style"}:
            self.skip.append(tag)
        if self.skip:
            return
        for match in re.finditer(r"\b(?:href|src|xlink:href)\s*=\s*(?:([\"'])(.*?)\1|([^\s>]+))", raw, re.I | re.S):
            group = 2 if match.group(1) else 3
            ds, de = start + match.start(group), start + match.end(group)
            ref = Reference(unescape(match.group(group)), ds, de, start, start + len(raw),
                            start + len(raw), start + len(raw), kind="html", label=attrs_dict.get("alt", ""),
                            extra={"tag": tag, "quote": match.group(1) or ""})
            self.references.append(ref)
            if tag == "a":
                self.open_links.append(ref)

    def handle_startendtag(self, tag: str, attrs: list) -> None:
        self.handle_starttag(tag, attrs)
        if self.skip and self.skip[-1] == tag:
            self.skip.pop()

    def handle_endtag(self, tag: str) -> None:
        if self.skip:
            if self.skip[-1] == tag:
                self.skip.pop()
            return
        if tag == "a" and self.open_links:
            ref = self.open_links.pop()
            ref.label_end = self.position()
            close = re.match(r"</a\s*>", self.text[self.position():], re.I)
            ref.wrapper_end = self.position() + (close.end() if close else 0)
            ref.label = self.text[ref.label_start:ref.label_end]


def html_references(text: str) -> list[Reference]:
    parser = HTMLReferences(text)
    parser.feed(text)
    return parser.references


def _heading_text(token) -> str:
    return "".join(t.content for t in token.children or [] if t.type in {"text", "code_inline", "image"})


def _slug(text: str) -> str:
    return re.sub(r"[^\w\- ]", "", unescape(text).lower()).replace(" ", "-")


def document_anchors(text: str, markdown: bool = True) -> set[str]:
    parser = HTMLReferences(text)
    if markdown:
        tokens = MARKDOWN.parse(text)
        for token in tokens:
            if token.type == "html_block":
                parser.feed(token.content)
            elif token.type == "inline":
                for child in token.children or []:
                    if child.type == "html_inline":
                        parser.feed(child.content)
        anchors = set(parser.ids)
        used: set[str] = set()
        for index, token in enumerate(tokens):
            if token.type == "heading_open" and index + 1 < len(tokens):
                base = _slug(_heading_text(tokens[index + 1]))
                candidate, suffix = base, 0
                while candidate in used:
                    suffix += 1
                    candidate = f"{base}-{suffix}"
                used.add(candidate)
                anchors.add(candidate)
    else:
        parser.feed(text)
        anchors = set(parser.ids)
    return anchors


def _source_documents(name: str, text: str, source_name: str) -> list[Document]:
    docs: list[Document] = []
    current: Document | None = None
    offset = 0
    for line in text.splitlines(keepends=True):
        if line.startswith("# %% "):
            marker = json.loads(line[len("# %% "):])
            current = (Document(source_name, name, "", cell=marker.get("id"), offsets=[])
                       if marker["type"] == "markdown" else None)
            if current:
                docs.append(current)
        elif current:
            prefix = 2 if line.startswith("# ") else 1 if line.startswith("#") else 0
            logical = line[prefix:]
            current.text += logical
            current.offsets.extend(range(offset + prefix, offset + len(line)))
        offset += len(line)
    return docs


def _pptx_documents(name: str, data_path: Path) -> list[Document]:
    docs = []
    with ZipFile(data_path) as archive:
        for member in sorted(archive.namelist()):
            if not member.startswith("ppt/slides/_rels/") or not member.endswith(".rels"):
                continue
            text = archive.read(member).decode("utf-8")
            doc = Document(name, name, text, kind="pptx", member=member)
            for match in re.finditer(r"<(?:\w+:)?Relationship\b[^>]*?/?>", text):
                raw = match.group()
                attrs = {a.group(1): unescape(a.group(3)) for a in re.finditer(
                    r"\b([\w:]+)\s*=\s*([\"'])(.*?)\2", raw, re.S)}
                if attrs.get("TargetMode") != "External":
                    continue
                target = re.search(r"\bTarget\s*=\s*([\"'])(.*?)\1", raw, re.S)
                if not target:
                    continue
                ds, de = match.start() + target.start(2), match.start() + target.end(2)
                doc.references.append(Reference(attrs["Target"], ds, de, match.start(), match.end(),
                                                match.start(), match.start(), kind="pptx",
                                                extra={"relationship_id": attrs.get("Id"), "quote": target.group(1)}))
            docs.append(doc)
    return docs


@dataclass
class FetchResult:
    status: int | None
    url: str
    body: bytes = b""
    content_type: str = ""
    error: str | None = None
    truncated: bool = False


def _challenge_response(response: FetchResult) -> bool:
    sample = response.body[:256000].decode("utf-8", "replace").lower()
    # Ordinary documentation and GitHub pages contain CAPTCHA libraries and
    # access-control terminology. Those strings in scripts or prose are not
    # evidence that the visitor received a challenge instead of the document.
    title_match = re.search(r"<title\b[^>]*>([\s\S]*?)</title>", sample)
    title = unescape(re.sub(r"<[^>]+>", " ", title_match.group(1))) if title_match else ""
    if re.search(r"just a moment|attention required|access denied|security check|robot check", title):
        return True
    visible = re.sub(r"<(script|style)\b[^>]*>[\s\S]*?</\1\s*>", " ", sample)
    visible = unescape(re.sub(r"<[^>]+>", " ", visible))
    visible = " ".join(visible.split())
    return len(visible) < 8000 and any(marker in visible for marker in (
        "verify you are human", "enable javascript and cookies", "robot check",
        "complete the captcha", "please enable javascript to continue",
    ))


def _fragment_verified(url: str, probe: dict) -> bool:
    fragment = unquote(urlsplit(url).fragment)
    if not fragment:
        return True
    response = probe["response"]
    return ("html" in response.content_type and not response.truncated
            and fragment in document_anchors(response.body.decode("utf-8", "replace"), markdown=False))


class _Redirects(HTTPRedirectHandler):
    max_redirections = 6
    max_repeats = 3


def fetch_url(url: str) -> FetchResult:
    """A bounded, credential-free GET; no HEAD-only false negatives."""
    request = Request(url, headers={"User-Agent": "Curriculum-Link-Audit/1.0", "Accept": "*/*"})
    try:
        with build_opener(_Redirects()).open(request, timeout=12) as response:
            body = response.read(2 * 1024 * 1024 + 1)
            return FetchResult(response.status, response.geturl(), body[:2 * 1024 * 1024],
                               response.headers.get("Content-Type", ""), truncated=len(body) > 2 * 1024 * 1024)
    except HTTPError as exc:
        try:
            body = exc.read(2 * 1024 * 1024 + 1)
        except OSError:
            body = b""
        return FetchResult(exc.code, exc.geturl(), body[:2 * 1024 * 1024],
                           exc.headers.get("Content-Type", "") if exc.headers else "",
                           error=f"HTTP {exc.code}", truncated=len(body) > 2 * 1024 * 1024)
    except (URLError, TimeoutError, OSError, ValueError) as exc:
        return FetchResult(None, url, error=f"{type(exc).__name__}: {exc}")


class Auditor:
    def __init__(self, root: Path, external: bool, fetcher: Callable[[str], FetchResult] | None,
                 replacements: dict[str, str] | None):
        self.root = root.resolve()
        self.external = external
        self.fetcher = fetcher or fetch_url
        self.replacements = replacements or {}
        self.inputs: dict[str, str] = {}
        self.documents: list[Document] = []
        self.notebook_sources: dict[str, str] = {}
        self.anchor_cache: dict[str, set[str]] = {}
        self.probes: dict[str, dict] = {}
        self.git_cache: dict[str, str | None] = {}
        raw_index = _git(self.root, "ls-files", "--stage", "-z")
        self.index_hash = digest(raw_index) if raw_index is not None else None
        raw_names = _git(self.root, "ls-files", "--cached", "--others", "--exclude-standard", "-z")
        if raw_names is None:
            names = [p.relative_to(self.root).as_posix() for p in self.root.rglob("*")
                     if p.is_file() and not any(part in EXCLUDED or part.startswith(".")
                                                for part in p.relative_to(self.root).parts)]
        else:
            names = raw_names.decode("utf-8", "surrogateescape").split("\0")
        self.files = sorted({n for n in names if n and (self.root / n).is_file()
                             and not any(p in EXCLUDED for p in Path(n).parts)
                             and _inside(self.root, self.root / n)})
        self.redirects = {}
        if (self.root / REDIRECTS).is_file():
            rows = json.loads(self.read(REDIRECTS))
            self.redirects = {row["source"]: row for row in rows}

    def read(self, name: str) -> str:
        data = (self.root / name).read_bytes()
        self.inputs[name] = digest(data)
        return data.decode("utf-8")

    def load(self, name: str) -> None:
        path = self.root / name
        if not _editable(self.root, path):
            raise ValueError(f"Refusing editable source outside active curriculum: {name}")
        if path.suffix == ".pptx":
            self.inputs[name] = digest(path.read_bytes())
            self.documents.extend(_pptx_documents(name, path))
            return
        text = self.read(name)
        if path.suffix == ".ipynb":
            source = "tools/notebook_sources/" + path.stem + ".py"
            if (self.root / source).is_file():
                self.documents.extend(_source_documents(name, self.read(source), source))
                self.notebook_sources[name] = source
            else:
                notebook = json.loads(text)
                self.documents.extend(Document(name, name, "".join(cell["source"]),
                                               cell=cell.get("id"), cell_index=i)
                                      for i, cell in enumerate(notebook["cells"])
                                      if cell["cell_type"] == "markdown")
        else:
            kind = "html" if path.suffix in {".html", ".htm", ".svg"} else "markdown"
            self.documents.append(Document(name, name, text, kind=kind))

    def anchors(self, name: str) -> set[str]:
        if name not in self.anchor_cache:
            text = self.read(name)
            if Path(name).suffix == ".ipynb":
                notebook = json.loads(text)
                # Rendered Markdown headings share a page and duplicate counter.
                text = "\n\n".join("".join(c["source"]) for c in notebook["cells"]
                                    if c["cell_type"] == "markdown")
                ids = {c["id"] for c in notebook["cells"] if c.get("id")}
            else:
                ids = set()
            self.anchor_cache[name] = ids | document_anchors(text, Path(name).suffix not in {".html", ".htm", ".svg"})
        return self.anchor_cache[name]

    def git_object(self, name: str) -> str | None:
        if name in self.git_cache:
            return self.git_cache[name]
        result = None
        if name and not name.startswith("../") and not Path(name).is_absolute():
            if _git(self.root, "cat-file", "-e", ":" + name) is not None:
                result = ":" + name
            else:
                commit = _git(self.root, "log", "--all", "-1", "--format=%H", "--diff-filter=AM", "--", name)
                if commit and commit.strip():
                    candidate = commit.decode().strip() + ":" + name
                    if _git(self.root, "cat-file", "-e", candidate) is not None:
                        result = candidate
        self.git_cache[name] = result
        return result

    def probe(self, url: str) -> dict:
        first = self.fetcher(url)
        attempts = [first]
        if first.status in {404, 410}:
            attempts.append(self.fetcher(url))
        last = attempts[-1]
        challenged = any(_challenge_response(a) for a in attempts)
        if challenged:
            state = "uncertain"
        elif last.status is not None and 200 <= last.status < 300:
            state = "verified"
        elif len(attempts) == 2 and all(a.status in {404, 410} for a in attempts):
            state = "permanent"
        else:
            state = "uncertain"
        return {"state": state, "attempts": [a.status for a in attempts], "final_url": last.url,
                "error": last.error, "response": last}

    def local(self, origin: str, target: str) -> tuple[str, str | None, dict]:
        parts = urlsplit(target)
        raw_path = unquote(parts.path).replace("\\", "/")
        origin_path = self.root / origin
        candidate = ((origin_path.parent / raw_path).resolve() if raw_path else origin_path.resolve())
        canonical = candidate.relative_to(self.root).as_posix() if _inside(self.root, candidate) else ""
        root_candidate = (self.root / raw_path.lstrip("/")).resolve()
        root_name = root_candidate.relative_to(self.root).as_posix() if _inside(self.root, root_candidate) else ""
        resolved = canonical if canonical and candidate.exists() else None
        fragment = unquote(parts.fragment)
        mapped = False
        if resolved is None and root_name and root_candidate.exists():
            resolved = root_name
        if resolved is None:
            for key in dict.fromkeys((canonical, root_name)):
                row = self.redirects.get(key)
                if row and (self.root / row["target"]).exists():
                    resolved = row["target"]
                    fragment = row["fragments"].get(fragment, fragment) if fragment else row["anchor"]
                    mapped = True
                    break
        if resolved is None and raw_path:
            suffix = raw_path.lstrip("./")
            candidates = [n for n in self.files if n == suffix or n.endswith("/" + suffix)]
            if not candidates:
                candidates = [n for n in self.files if Path(n).name == Path(raw_path).name]
            if len(candidates) == 1:
                resolved = candidates[0]
            elif len(candidates) > 1:
                return "ambiguous_local", None, {"candidates": sorted(candidates)}
        if resolved is None:
            for name in dict.fromkeys((canonical, root_name)):
                obj = self.git_object(name)
                if obj:
                    return "git_only", None, {"git_object": obj, "path": name}
            return "missing_local", None, {}
        extra = {"resolved_path": resolved}
        if fragment and Path(resolved).suffix.lower() in {".md", ".ipynb", ".html", ".htm", ".svg"}:
            anchors = self.anchors(resolved)
            if fragment not in anchors:
                matches = [a for a in anchors if a.casefold() == fragment.casefold() or a == _slug(fragment)]
                if len(matches) == 1:
                    fragment = matches[0]
                    mapped = True
                else:
                    return "missing_anchor", None, {**extra, "fragment": fragment}
        relative = os.path.relpath(self.root / resolved, origin_path.parent).replace(os.sep, "/")
        encoded = quote(relative, safe="/-._~%") if raw_path else ""
        replacement = urlunsplit(("", "", encoded, parts.query, quote(fragment, safe="-._~!$&'()*+,;=:@/?%")))
        # Preserve all compliant spelling, escaping, and encoding.
        if resolved == canonical and not mapped:
            return "valid_local", None, extra
        return "repair_local", replacement, extra

    def classify(self, doc: Document, ref: Reference) -> tuple[str, str | None, dict]:
        try:
            parts = urlsplit(ref.target)
        except ValueError as exc:
            return "unverified_target", None, {"error": str(exc)}
        if parts.scheme in {"http", "https"} or parts.netloc:
            base = urlunsplit((parts.scheme or "https", parts.netloc, parts.path, parts.query, ""))
            if not self.external:
                return "unverified_external", None, {"reason": "network check not requested"}
            probe = self.probes.setdefault(base, self.probe(base)) if base not in self.probes else self.probes[base]
            evidence = {k: v for k, v in probe.items() if k != "response"}
            if probe["state"] == "permanent":
                exact_replacement = self.replacements.get(ref.target)
                replacement = exact_replacement or self.replacements.get(base)
                if replacement:
                    replacement_parts = urlsplit(replacement)
                    if parts.fragment and not exact_replacement and not replacement_parts.fragment:
                        replacement_parts = replacement_parts._replace(fragment=parts.fragment)
                        replacement = urlunsplit(replacement_parts)
                    replacement_base = urlunsplit(replacement_parts._replace(fragment=""))
                    if replacement_base not in self.probes:
                        self.probes[replacement_base] = self.probe(replacement_base)
                    replacement_probe = self.probes[replacement_base]
                    if replacement_probe["state"] == "verified" and _fragment_verified(replacement, replacement_probe):
                        return "repair_external", replacement, evidence
                    return "unverified_external_replacement", None, {
                        **evidence, "candidate_replacement": replacement,
                        "reason": "replacement destination or fragment could not be verified"}
                return "dead_external", None, evidence
            if probe["state"] == "verified":
                if parts.fragment:
                    response = probe["response"]
                    if "html" in response.content_type and not response.truncated:
                        anchors = document_anchors(response.body.decode("utf-8", "replace"), markdown=False)
                        if unquote(parts.fragment) in anchors:
                            return "verified_external", None, {**evidence, "fragment_verified": True}
                    return "unverified_external_anchor", None, evidence
                return "verified_external", None, evidence
            return "uncertain_external", None, evidence
        if parts.scheme and parts.scheme != "file":
            return "ignored_scheme", None, {"scheme": parts.scheme}
        result = self.local(doc.origin, ref.target)
        if ref.kind == "static" and result[0] == "repair_local":
            # Code-span file labels are already plain text. A verified mapping
            # establishes the reference without rewriting useful prose. Only
            # navigational hrefs require source-relative spelling.
            return "valid_local", None, result[2]
        return result


def _unwrap_edits(doc: Document, ref: Reference, local: bool) -> tuple[str, list[dict]]:
    text = doc.text
    line_start = text.rfind("\n", 0, ref.wrapper_start) + 1
    end = text.find("\n", ref.wrapper_end)
    line_end = len(text) if end < 0 else end + 1
    before, after = text[line_start:ref.wrapper_start], text[ref.wrapper_end:line_end]
    sole = bool(re.fullmatch(r"\s*(?:[-*+]\s+|\d+[.)]\s+)?", before) and not after.strip())
    if ref.definition:
        return "remove_definition", [{"start": ref.wrapper_start, "end": ref.wrapper_end, "new": "", "full_line": True}]
    if local and sole and ref.kind != "pptx":
        return "remove_line", [{"start": line_start, "end": line_end, "new": "", "full_line": True}]
    if ref.kind == "static":
        return "keep", []
    if ref.kind == "html" and ref.extra.get("tag") != "a":
        return "unwrap", [{"start": ref.wrapper_start, "end": ref.wrapper_end, "new": ref.label}]
    if ref.kind == "pptx":
        return "unwrap", [{"start": ref.wrapper_start, "end": ref.wrapper_end, "new": ""}]
    return "unwrap", [{"start": ref.wrapper_start, "end": ref.label_start, "new": ""},
                       {"start": ref.label_end, "end": ref.wrapper_end, "new": ""}]


def _replace_edit(ref: Reference, replacement: str) -> dict:
    if ref.kind in {"html", "pptx"}:
        replacement = escape(replacement, quote=True)
        if ref.extra.get("quote") == "'":
            replacement = replacement.replace("&#x27;", "&#39;")
    return {"start": ref.start, "end": ref.end, "new": replacement}


def _json_value_spans(text: str) -> dict[tuple, tuple[int, int]]:
    decoder = json.JSONDecoder()
    spans = {}

    def skip(i):
        while i < len(text) and text[i].isspace():
            i += 1
        return i

    def parse(i, path):
        i = skip(i)
        start = i
        if text[i] == "{":
            i = skip(i + 1)
            while text[i] != "}":
                key, i = decoder.raw_decode(text, i)
                i = skip(i)
                if text[i] != ":":
                    raise ValueError("Invalid JSON object")
                i = skip(parse(i + 1, path + (key,)))
                if text[i] == ",":
                    i = skip(i + 1)
                else:
                    break
            i += 1
        elif text[i] == "[":
            i = skip(i + 1)
            index = 0
            while text[i] != "]":
                i = skip(parse(i, path + (index,)))
                index += 1
                if text[i] == ",":
                    i = skip(i + 1)
                else:
                    break
            i += 1
        else:
            _, i = decoder.raw_decode(text, i)
        if len(path) == 3 and path[0] == "cells" and path[2] == "source":
            spans[path] = (start, i)
        return i

    parse(0, ())
    return spans


def _apply_text_edits(text: str, edits: list[dict]) -> str:
    unique = {(e["start"], e["end"], e["new"]): e for e in edits if e["start"] != e["end"] or e["new"]}
    ordered = sorted(unique.values(), key=lambda e: (e["start"], -e["end"]))
    filtered = []
    for edit in ordered:
        if filtered and edit["start"] < filtered[-1]["end"]:
            if not filtered[-1]["new"] and edit["end"] <= filtered[-1]["end"]:
                continue
            raise ValueError("Overlapping repairs require a new audit")
        filtered.append(edit)
    for edit in reversed(filtered):
        if "old" in edit and text[edit["start"]:edit["end"]] != edit["old"]:
            raise ValueError("Repair span does not match the audited input")
        text = text[:edit["start"]] + edit["new"] + text[edit["end"]:]
    return text


def _materialize(doc: Document, edits: list[dict], auditor: Auditor) -> list[dict]:
    if not edits:
        return []
    if doc.cell_index is not None:
        raw = auditor.read(doc.source)
        notebook = json.loads(raw)
        cell = notebook["cells"][doc.cell_index]
        logical = _apply_text_edits(doc.text, edits)
        value = logical.splitlines(keepends=True) if isinstance(cell["source"], list) else logical
        start, end = _json_value_spans(raw)[("cells", doc.cell_index, "source")]
        indentation = re.match(r"[ \t]*", raw[raw.rfind("\n", 0, start) + 1:]).group()
        rendered = json.dumps(value, ensure_ascii=False, indent=2).replace("\n", "\n" + indentation)
        return [{"path": doc.source, "start": start, "end": end, "old": raw[start:end], "new": rendered}]
    results = []
    raw = auditor.read(doc.source) if doc.offsets is not None else doc.text
    for edit in edits:
        a, b = edit["start"], edit["end"]
        if doc.offsets is not None:
            start = doc.offsets[a] if a < len(doc.offsets) else doc.offsets[-1] + 1
            end = doc.offsets[b - 1] + 1 if b > a else start
            if edit.get("full_line"):
                start = raw.rfind("\n", 0, start) + 1
        else:
            start, end = a, b
        result = {"path": doc.source, "start": start, "end": end,
                  "old": raw[start:end], "new": edit["new"]}
        if doc.member:
            result["member"] = doc.member
        results.append(result)
    return results


def audit(root: Path = ROOT, sources: list[str] | None = None, *, external: bool = False,
          fetcher: Callable[[str], FetchResult] | None = None,
          replacements: dict[str, str] | None = None) -> dict:
    """Return a JSON-compatible audit and exact repair spans; write nothing."""
    root = Path(root).resolve()
    auditor = Auditor(root, external, fetcher, replacements)
    names = sorted(set(sources if sources is not None else discover_sources(root)))
    for name in names:
        auditor.load(name)
    for doc in auditor.documents:
        if doc.kind != "pptx":
            doc.references = html_references(doc.text) if doc.kind == "html" else markdown_references(doc.text)
            if doc.kind == "markdown":
                doc.references.extend(static_path_references(doc.text, doc.references))
                # Inline HTML in Markdown obeys the same fenced-code exclusions.
                token_lines = _line_starts(doc.text)
                for token in MARKDOWN.parse(doc.text):
                    if token.type == "html_block" and token.map:
                        start = token_lines[token.map[0]]
                        fragment = token.content
                        for ref in html_references(fragment):
                            for attr in ("start", "end", "wrapper_start", "wrapper_end", "label_start", "label_end"):
                                setattr(ref, attr, getattr(ref, attr) + start)
                            doc.references.append(ref)
                    elif token.type == "inline" and token.map and token.children:
                        # HTML anchors are common inside a Markdown paragraph.
                        content = token.content
                        if any(c.type == "html_inline" for c in token.children):
                            block_start = token_lines[token.map[0]]
                            offset = doc.text.find(content, block_start)
                            if offset >= 0:
                                # Preserve positions while hiding inline examples
                                # from HTMLParser in mixed HTML/code paragraphs.
                                masked_content = re.sub(r"(`+)([\s\S]*?)\1",
                                                        lambda m: " " * len(m.group()), content)
                                for ref in html_references(masked_content):
                                    for attr in ("start", "end", "wrapper_start", "wrapper_end", "label_start", "label_end"):
                                        setattr(ref, attr, getattr(ref, attr) + offset)
                                    doc.references.append(ref)
    if external:
        urls = set()
        for doc in auditor.documents:
            for ref in doc.references:
                try:
                    parts = urlsplit(ref.target)
                    if parts.scheme in {"http", "https"} or parts.netloc:
                        urls.add(urlunsplit((parts.scheme or "https", parts.netloc, parts.path, parts.query, "")))
                except ValueError:
                    pass
        with ThreadPoolExecutor(max_workers=4) as executor:
            auditor.probes.update(zip(sorted(urls), executor.map(auditor.probe, sorted(urls))))
    findings, all_edits = [], []
    for doc in auditor.documents:
        doc_edits = []
        for ref in sorted(doc.references, key=lambda r: (r.wrapper_start, r.start, r.kind)):
            status, replacement, evidence = auditor.classify(doc, ref)
            resolution_status = status
            action, edits = "keep", []
            if replacement is not None:
                action, edits = "replace", [_replace_edit(ref, replacement)]
            elif status in {"missing_local", "missing_anchor", "dead_external"}:
                action, edits = _unwrap_edits(doc, ref, status != "dead_external")
                if ref.kind == "static" and action == "keep":
                    status = "plain_missing_path"
            doc_edits.extend(edits)
            finding = {"source": doc.source, "origin": doc.origin, "line": doc.text.count("\n", 0, ref.wrapper_start) + 1,
                       "target": ref.target, "kind": ref.kind, "status": status,
                       "resolution_status": resolution_status, "action": action, **evidence}
            if doc.cell is not None:
                finding["cell"] = doc.cell
            if doc.member:
                finding["member"] = doc.member
            if replacement is not None:
                finding["replacement"] = replacement
            findings.append(finding)
            if ref.kind == "pptx" and action == "unwrap":
                slide_member = doc.member.replace("/_rels/", "/").removesuffix(".rels")
                with ZipFile(root / doc.source) as archive:
                    slide = archive.read(slide_member).decode("utf-8")
                relationship_id = re.escape(ref.extra["relationship_id"])
                pattern = r"<(?:\w+:)?hlink(?:Click|MouseOver)\b(?=[^>]*\b(?:\w+:)?id=[\"']" + relationship_id + r"[\"'])[^>]*(?:/>|>[\s\S]*?</(?:\w+:)?hlink(?:Click|MouseOver)>)"
                for match in re.finditer(pattern, slide):
                    all_edits.append({"path": doc.source, "member": slide_member, "start": match.start(),
                                      "end": match.end(), "old": match.group(), "new": ""})
        all_edits.extend(_materialize(doc, doc_edits, auditor))
    for dependency in ("notebook_manifest.yml", "tools/audit_links.py", "tools/build_learner_pack.py"):
        if (root / dependency).is_file():
            auditor.inputs[dependency] = digest((root / dependency).read_bytes())
    counts = Counter(f["status"] for f in findings)
    repairs = sum(f["action"] != "keep" for f in findings)
    uncertain = sum(n for status, n in counts.items() if status.startswith(("unverified", "uncertain"))
                    or status in {"ambiguous_local", "git_only"})
    return {"schema_version": SCHEMA_VERSION, "root": str(root), "external_requested": external,
            "external_checked_at": datetime.now(timezone.utc).isoformat() if external else None,
            "sources": names, "inputs": dict(sorted(auditor.inputs.items())), "git_index_sha256": auditor.index_hash,
            "notebook_sources": auditor.notebook_sources,
            "summary": {"files": len(names), "references": len(findings), "repairs": repairs,
                        "unverified": uncertain, "statuses": dict(sorted(counts.items()))},
            "findings": findings, "edits": sorted(all_edits, key=lambda e: (e["path"], e.get("member", ""), e["start"], e["end"]))}


def apply_report(root: Path, report: dict) -> list[str]:
    """Apply only the report's recorded repairs after validating every input."""
    root = Path(root).resolve()
    if report.get("schema_version") != SCHEMA_VERSION or report.get("root") != str(root):
        raise ValueError("Report version/root does not match this checkout")
    for name, expected in report["inputs"].items():
        path = root / name
        if not _inside(root, path) or not path.is_file() or digest(path.read_bytes()) != expected:
            raise ValueError(f"Stale audit input: {name}; run check again")
    raw_index = _git(root, "ls-files", "--stage", "-z")
    current_index = digest(raw_index) if raw_index is not None else None
    if current_index != report.get("git_index_sha256"):
        raise ValueError("Git index changed since audit; run check again")
    # A new untracked file or empty directory can invalidate a recorded removal
    # without changing any content hash or the Git index. Recheck local lookup
    # decisions against the current resolution landscape before any writes.
    resolver = Auditor(root, False, None, None)
    for finding in report["findings"]:
        if finding["status"] not in {"valid_local", "repair_local", "missing_local", "missing_anchor",
                                     "plain_missing_path", "ambiguous_local", "git_only"}:
            continue
        status, replacement, _ = resolver.local(finding["origin"], finding["target"])
        expected = finding.get("resolution_status", finding["status"])
        if finding.get("kind") == "static" and expected == "valid_local" and status == "repair_local":
            status, replacement = "valid_local", None
        if status != expected or replacement != finding.get("replacement"):
            raise ValueError(f"Stale audit resolution: {finding['target']}; run check again")
    grouped = defaultdict(list)
    for edit in report["edits"]:
        name = edit["path"]
        if not _editable(root, root / name) or name not in report["inputs"]:
            raise ValueError(f"Refusing repair outside audited active sources: {name}")
        grouped[(name, edit.get("member"))].append(edit)
    # Prepare all bytes before writing, so invalid spans never produce a partial repair.
    updates: dict[str, bytes] = {}
    member_updates = defaultdict(dict)
    for (name, member), edits in grouped.items():
        if member:
            with ZipFile(root / name) as archive:
                original = archive.read(member).decode("utf-8")
            member_updates[name][member] = _apply_text_edits(original, edits).encode("utf-8")
        else:
            original = (root / name).read_bytes().decode("utf-8")
            updates[name] = _apply_text_edits(original, edits).encode("utf-8")
    if member_updates:
        from io import BytesIO
        for name, members in member_updates.items():
            output = BytesIO()
            with ZipFile(root / name) as original, ZipFile(output, "w") as destination:
                destination.comment = original.comment
                for info in original.infolist():
                    destination.writestr(info, members.get(info.filename, original.read(info.filename)))
            updates[name] = output.getvalue()
    from tools.build_core_notebooks import notebook_from_source
    for notebook, source in report.get("notebook_sources", {}).items():
        if source in updates:
            # Parse the repaired source in memory using the same canonical format.
            from tempfile import TemporaryDirectory
            with TemporaryDirectory() as temporary:
                source_path = Path(temporary) / Path(source).name
                source_path.write_bytes(updates[source])
                payload = notebook_from_source(source_path)
            before = json.loads((root / notebook).read_bytes())
            if [c for c in before["cells"] if c["cell_type"] == "code"] != [
                    c for c in payload["cells"] if c["cell_type"] == "code"]:
                raise ValueError(f"Notebook code drifted from canonical source: {notebook}")
            updates[notebook] = (json.dumps(payload, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    changed = []
    for name, data in sorted(updates.items()):
        path = root / name
        if path.read_bytes() != data:
            path.write_bytes(data)
            changed.append(name)
    return changed


def readable_report(report: dict) -> str:
    summary = report["summary"]
    lines = ["# Active curriculum link audit", "",
             f"Checked {summary['files']} source files and {summary['references']} references.", "",
             f"Proposed repairs: **{summary['repairs']}**. Unverified or ambiguous references: **{summary['unverified']}**.", "",
             "Archived files are destination candidates only. Existing slide-reference edits are editorial updates, not link repairs.", "",
             "## Status counts", "", "| Status | References |", "| --- | ---: |"]
    lines.extend(f"| {status} | {count} |" for status, count in summary["statuses"].items())
    if report.get("external_checked_at"):
        lines.extend(["", f"HTTP observations recorded at {report['external_checked_at']}. Live availability can change."])
    else:
        lines.extend(["", "External availability was not checked. Use the explicit `--external` option."])
    for title, rows in (
        ("Proposed repairs", [f for f in report["findings"] if f["action"] != "keep"]),
        ("Unverified and unresolved references", [f for f in report["findings"]
          if f["status"].startswith(("unverified", "uncertain")) or f["status"] in {"ambiguous_local", "git_only", "plain_missing_path"}]),
    ):
        lines.extend(["", f"## {title}", ""])
        if not rows:
            lines.append("None.")
            continue
        lines.extend(["| Source | Target | Status / action | Evidence |", "| --- | --- | --- | --- |"])
        for finding in rows:
            source = f"{finding['origin']}:{finding['line']}"
            if finding.get("cell"):
                source += f" (cell {finding['cell']})"
            detail = finding.get("reason") or finding.get("error") or finding.get("replacement") or finding.get("final_url") or ""
            fields = [source, finding["target"], finding["status"] + " / " + finding["action"], detail]
            fields = [str(field).replace("|", "\\|").replace("\n", " ") for field in fields]
            lines.append("| " + " | ".join(fields) + " |")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    commands = parser.add_subparsers(dest="command", required=True)
    check = commands.add_parser("check", help="Read-only audit; network access is opt-in")
    check.add_argument("--external", action="store_true")
    check.add_argument("--report", type=Path)
    check.add_argument("--replacements", type=Path, help="JSON object of explicit old URL to replacement URL mappings")
    apply = commands.add_parser("apply", help="Apply verified repairs from an unchanged report")
    apply.add_argument("--from-report", "--report", dest="report", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "apply":
            report = json.loads(args.report.read_text(encoding="utf-8"))
            changed = apply_report(args.root, report)
            print(f"Applied link repairs to {len(changed)} file(s).")
            for name in changed:
                print(name)
            return 0
        replacements = json.loads(args.replacements.read_text(encoding="utf-8")) if args.replacements else None
        report = audit(args.root, external=args.external, replacements=replacements)
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            readable_path = args.report.with_suffix(".md")
            if readable_path == args.report:
                readable_path = args.report.with_name(args.report.stem + ".readable.md")
            readable_path.write_text(readable_report(report), encoding="utf-8")
        summary = report["summary"]
        print(f"Audited {summary['files']} files and {summary['references']} references: "
              f"{summary['repairs']} repair(s), {summary['unverified']} unverified.")
        if not args.external:
            print("External URL availability was not checked (use --external).")
        return 1 if summary["repairs"] else 0
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as exc:
        print(f"Link audit error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
