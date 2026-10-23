"""Bounded offline checks against the actual static HTML candidate.

These checks establish source properties, not a penetration test, WCAG audit,
browser layout measurement, or performance result. QA accepts a small declarative
selector language and never evaluates agent-provided Python or JavaScript.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from html import unescape
from html.parser import HTMLParser
import json
import re

from pydantic import BaseModel, ConfigDict

from software_factory.contracts import QAPlan, Review

MAX_HTML_LENGTH = 200_000
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
STATIC_TAGS = set("html head title meta style body header footer main nav section article aside div span p h1 h2 h3 h4 h5 h6 a ul ol li dl dt dd strong em b i small abbr address blockquote cite code pre kbd samp time figure figcaption img picture source br hr table caption thead tbody tfoot tr th td col colgroup details summary mark sub sup s u wbr".split())


@dataclass
class Node:
    tag: str
    attrs: dict[str, str]
    parent: Node | None = None
    children: list[Node | str] = field(default_factory=list)

    def text(self) -> str:
        return " ".join(" ".join(child.text() if isinstance(child, Node) else child for child in self.children).split())


class Document(HTMLParser):
    def __init__(self, source: str):
        super().__init__(convert_charrefs=True)
        self.root = Node("document", {})
        self.stack = [self.root]
        self.nodes: list[Node] = []
        self.errors: list[str] = []
        self.feed(source)
        self.close()
        if len(self.stack) > 1:
            self.errors.append("Unclosed HTML elements")

    def handle_starttag(self, tag, attrs):
        names = [name for name, _ in attrs]
        if len(names) != len(set(names)):
            self.errors.append("Duplicate HTML attributes")
        node = Node(tag, {name: value or "" for name, value in attrs}, self.stack[-1])
        self.stack[-1].children.append(node)
        self.nodes.append(node)
        if tag not in VOID_TAGS:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag in VOID_TAGS:
            return
        if len(self.stack) > 1 and self.stack[-1].tag == tag:
            self.stack.pop()
            return
        self.errors.append("Mismatched HTML closing elements")
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def _document(html: str) -> Document:
    if not isinstance(html, str) or not html.strip() or len(html) > MAX_HTML_LENGTH:
        raise ValueError("HTML must be nonempty and at most 200,000 characters")
    return Document(html)


def _css_decoded(css: str) -> str:
    # Decode CSS escapes before checking tokens such as u\\72l(...).
    decoded = re.sub(r"\\([0-9a-fA-F]{1,6})\s?", lambda match: chr(int(match.group(1), 16)) if 0 < int(match.group(1), 16) <= 0x10FFFF else "\ufffd", css)
    decoded = re.sub(r"\\([^\r\n])", r"\1", decoded)
    return re.sub(r"/\*.*?\*/", "", decoded, flags=re.S)


def _css_normalized(css: str) -> str:
    return _css_decoded(css).casefold()


def _review(issues: list[str], clean_summary: str) -> Review:
    unique = list(dict.fromkeys(issues))
    return Review(approved=not unique, issues=unique[:30], summary="Local source checks blocked this candidate." if unique else clean_summary)


def inspect_security(html: str) -> Review:
    """Enforce a narrow self-contained, script-free static-site policy."""
    if not isinstance(html, str) or not html.strip() or len(html) > MAX_HTML_LENGTH:
        return _review(["Invalid or oversized candidate"], "")
    lower = unescape(html).casefold()
    issues = []
    if re.search(r"http\s*:\s*//", lower):
        issues.append("Insecure HTTP endpoint")
    if "password" in lower and "localstorage" in lower:
        issues.append("Passwords in localStorage")
    if "evil.com" in lower or re.search(r"\bexfiltrat\w*\b", lower):
        issues.append("Potential data exfiltration")
    try:
        document = _document(html)
    except Exception as error:
        return _review(issues + [f"Candidate could not be parsed: {type(error).__name__}"], "")
    issues.extend(document.errors)
    for node in document.nodes:
        if node.tag == "script":
            issues.append("Scripts are forbidden in the static-site demo")
        elif node.tag in {"iframe", "object", "embed", "base", "link", "form", "input", "button", "textarea", "select", "svg", "math"}:
            issues.append(f"Active or external content is forbidden: {node.tag}")
        elif node.tag not in STATIC_TAGS:
            issues.append(f"Unsupported element in the static-site policy: {node.tag}")
        if any(name.casefold().startswith("on") for name in node.attrs):
            issues.append("Inline event handlers are forbidden")
        if node.tag == "meta" and node.attrs.get("http-equiv", "").strip().casefold() == "refresh":
            issues.append("Meta refresh is forbidden")
        for name, value in node.attrs.items():
            if name in {"srcdoc", "ping"}:
                issues.append(f"Active request attribute is forbidden: {name}")
            if name in {"src", "href", "action", "formaction", "poster", "background", "data", "srcset", "xlink:href"}:
                normalized = re.sub(r"[\x00-\x20\x7f]+", "", unescape(value)).casefold()
                # Only fragment links are allowed. Assets and remote requests
                # cannot be smuggled into an otherwise static teaching fixture.
                if normalized and not (name == "href" and normalized.startswith("#")):
                    issues.append("External requests or non-fragment URLs are forbidden")
        css = node.text() if node.tag == "style" else node.attrs.get("style", "")
        normalized_css = _css_normalized(css)
        if re.search(r"\burl\s*\(|@import\b|\bimage-set\s*\(", normalized_css):
            issues.append("CSS resource loading is forbidden")
        if re.search(r"expression\s*\(|(?:^|[;{])\s*(?:behavior|-moz-binding)\s*:", normalized_css):
            issues.append("Active CSS behavior is forbidden")
    return _review(issues, "Passed the bounded static-site source policy; human review is still required.")


def inspect_ui(html: str) -> Review:
    """Check semantic source basics without asserting WCAG conformance."""
    try:
        document = _document(html)
    except Exception as error:
        return _review([f"Candidate could not be parsed: {type(error).__name__}"], "")
    issues = list(document.errors)
    nodes = document.nodes
    for tag in ("html", "main", "h1"):
        matching = [node for node in nodes if node.tag == tag]
        if len(matching) != 1:
            issues.append(f"Expected exactly one {tag} element")
    if not any(node.tag == "nav" for node in nodes):
        issues.append("A navigation landmark is required")
    if not any(node.tag == "html" and node.attrs.get("lang", "").strip() for node in nodes):
        issues.append("The html element needs a language")
    if not any(node.tag == "meta" and node.attrs.get("name", "").casefold() == "viewport" and re.search(r"width\s*=\s*device-width", node.attrs.get("content", ""), re.I) for node in nodes):
        issues.append("A width=device-width viewport declaration is required")
    ids = [node.attrs["id"] for node in nodes if "id" in node.attrs]
    if len(ids) != len(set(ids)):
        issues.append("HTML IDs must be unique")
    for node in nodes:
        if node.tag == "a":
            href = node.attrs.get("href", "")
            if href.startswith("#") and href[1:] not in ids:
                issues.append(f"Broken local navigation target: {href}")
            if not node.text() and not node.attrs.get("aria-label", "").strip():
                issues.append("Links need text or an accessible label")
        if node.tag == "img" and "alt" not in node.attrs:
            issues.append("Images need an alt attribute")
    return _review(issues, "Passed semantic HTML, language, viewport, and local-link source checks; visual and accessibility review remain human tasks.")


class QACaseResult(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    name: str
    selector: str
    assertion: str
    expected: str
    passed: bool
    observed: str


_SIMPLE_SELECTOR = re.compile(r"(?P<tag>[a-zA-Z][a-zA-Z0-9-]*)?(?P<qualifiers>(?:[.#][a-zA-Z_][a-zA-Z0-9_-]*)*)\Z")


def _selector_parts(selector: str) -> list[str]:
    parts = selector.strip().split()
    if not parts or any(not _SIMPLE_SELECTOR.fullmatch(part) or not part for part in parts):
        raise ValueError("Unsupported selector; use tag, #id, .class, or their descendant combinations")
    return parts


def _matches_simple(node: Node, part: str) -> bool:
    parsed = _SIMPLE_SELECTOR.fullmatch(part)
    if parsed is None:
        return False
    tag = parsed.group("tag")
    if tag and node.tag != tag.casefold():
        return False
    for marker, value in re.findall(r"([.#])([a-zA-Z_][a-zA-Z0-9_-]*)", parsed.group("qualifiers")):
        if marker == "#" and node.attrs.get("id") != value:
            return False
        if marker == "." and value not in node.attrs.get("class", "").split():
            return False
    return True


def _matches(node: Node, parts: list[str]) -> bool:
    if not _matches_simple(node, parts[-1]):
        return False
    ancestor = node.parent
    for part in reversed(parts[:-1]):
        while ancestor is not None and not _matches_simple(ancestor, part):
            ancestor = ancestor.parent
        if ancestor is None:
            return False
        ancestor = ancestor.parent
    return True


def _hidden(node: Node, document: Document) -> bool:
    hiding = r"(?:^|;)\s*(?:display\s*:\s*none\b|visibility\s*:\s*(?:hidden|collapse)\b|opacity\s*:\s*0(?:\.0*)?(?:\s*!important)?\s*(?:;|$))"
    current = node
    while current is not None:
        attrs = current.attrs
        style = _css_normalized(attrs.get("style", ""))
        if "hidden" in attrs or attrs.get("aria-hidden", "").casefold() == "true" or re.search(hiding, style, re.I):
            return True
        # A hiding rule can be conditional on a viewport. Conservatively fail
        # rather than claim visual visibility without a rendered browser.
        for stylesheet in (item.text() for item in document.nodes if item.tag == "style"):
            for selector, declaration in re.findall(r"([^{}]+)\{([^{}]*)\}", _css_decoded(stylesheet)):
                if re.search(hiding, declaration, re.I):
                    for option in selector.split(","):
                        try:
                            if _matches(current, _selector_parts(option)):
                                return True
                        except ValueError:
                            # Unknown CSS capable of hiding content cannot
                            # establish the narrow source-visibility assertion.
                            return True
        current = current.parent
    return False


def run_qa(html: str, plan: QAPlan) -> list[QACaseResult]:
    """Execute declarative source assertions; unsupported tests always fail."""
    checked_plan = QAPlan.model_validate(plan)
    try:
        document = _document(html)
        document_error = "; ".join(dict.fromkeys(document.errors))
    except Exception as error:
        document = None
        document_error = f"Candidate could not be parsed: {type(error).__name__}"
    results = []
    for test in checked_plan.test_cases:
        passed = False
        try:
            if document is None or document_error:
                raise ValueError(document_error)
            parts = _selector_parts(test.selector)
            nodes = [node for node in document.nodes if _matches(node, parts)]
            if test.assertion == "count":
                if not re.fullmatch(r"0|[1-9][0-9]*", test.expected):
                    raise ValueError("Count expectation must be a nonnegative decimal integer")
                passed = len(nodes) == int(test.expected)
                observed = f"Matched {len(nodes)} element(s)"
            elif test.assertion == "visible":
                if test.expected not in {"true", "false"}:
                    raise ValueError("Visible expectation must be 'true' or 'false'")
                source_visible = bool(nodes) and all(not _hidden(node, document) for node in nodes)
                passed = source_visible == (test.expected == "true")
                observed = f"Source visibility={str(source_visible).lower()}; DOM/HTML/CSS hiding checks, not rendered layout"
            elif test.assertion == "text":
                if not test.expected.strip():
                    raise ValueError("Text expectation cannot be empty")
                texts = [node.text() for node in nodes]
                passed = bool(nodes) and all(test.expected in text for text in texts)
                observed = " | ".join(texts)[:1000] if texts else "No matching element"
            elif test.assertion == "attribute":
                if test.expected.startswith("{"):
                    specification = json.loads(test.expected)
                    if not isinstance(specification, dict) or set(specification) != {"name", "value"}:
                        raise ValueError("Attribute expectation must contain exactly name and value")
                    name, expected = specification["name"], specification["value"]
                else:
                    name, separator, expected = test.expected.partition("=")
                    if not separator:
                        raise ValueError("Attribute expectation must be name=value")
                if not isinstance(name, str) or not re.fullmatch(r"[a-zA-Z_:][a-zA-Z0-9_:.-]*", name) or not isinstance(expected, str):
                    raise ValueError("Invalid attribute expectation")
                values = [node.attrs.get(name.casefold()) for node in nodes]
                passed = bool(nodes) and all(value == expected for value in values)
                observed = json.dumps(values)
            else:
                raise ValueError("Unsupported assertion")
        except (ValueError, TypeError, KeyError) as error:
            observed = str(error)
        results.append(QACaseResult(name=test.name, selector=test.selector, assertion=test.assertion,
                                    expected=test.expected, passed=passed, observed=observed))
    return results
