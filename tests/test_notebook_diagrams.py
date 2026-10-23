"""Keep learner exercise diagrams usable when notebooks move independently."""
from __future__ import annotations

import base64
import json
import re
from pathlib import Path
from xml.etree import ElementTree

import nbformat
import pytest
from nbconvert import HTMLExporter

from tools import build_core_notebooks as notebook_builder
from tools.build_learner_pack import package_files


SVG_MIME = "image/svg+xml"
SVG_NAMESPACE = "{http://www.w3.org/2000/svg}"
ATTACHMENT_REFERENCE = re.compile(r"attachment:([^\s)'\"<>]+)")
SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" role="img" '
    'aria-labelledby="flow-title flow-description">'
    '<title id="flow-title">Exercise flow</title>'
    '<desc id="flow-description">Validate a candidate before passing it to review.</desc>'
    '<text x="10" y="20">Validate → Review</text></svg>'
)


def _write_source(path: Path, *, diagram: str, kind: str = "markdown", reference: str = "flow.svg") -> Path:
    marker = {"id": "exercise-flow", "type": kind, "diagram": diagram}
    content = (f"# ![Validate the candidate before review](attachment:{reference})\n"
               if kind == "markdown" else "value = 1\n")
    path.write_text("# %% " + json.dumps(marker) + "\n" + content, encoding="utf-8")
    return path


def _diagram_cells(notebook: dict) -> list[dict]:
    return [cell for cell in notebook["cells"] if cell.get("attachments")]


def _assert_attached_diagrams(notebook: dict) -> None:
    svg_count = 0
    for cell in notebook["cells"]:
        source = "".join(cell["source"])
        references = set(ATTACHMENT_REFERENCE.findall(source))
        attachments = cell.get("attachments", {})
        assert references == set(attachments), (cell["id"], references, set(attachments))
        if attachments:
            assert cell["cell_type"] == "markdown"
        for name, content in attachments.items():
            if SVG_MIME not in content:
                continue
            svg_count += 1
            raw = base64.b64decode(content[SVG_MIME], validate=True)
            svg = ElementTree.fromstring(raw)
            assert svg.tag == SVG_NAMESPACE + "svg"
            for tag in ("title", "desc"):
                element = svg.find(SVG_NAMESPACE + tag)
                assert element is not None and "".join(element.itertext()).strip(), (name, tag)
            # A useful Markdown alternative remains available without image rendering.
            image = re.search(r"!\[([^\]]+)\]\(attachment:" + re.escape(name) + r"\)", source)
            assert image is not None and image.group(1).strip(), (cell["id"], name)
    assert svg_count > 0, "Each required notebook needs an embedded SVG exercise diagram"


@pytest.mark.unit
def test_source_builder_embeds_a_portable_svg_attachment(tmp_path, monkeypatch):
    monkeypatch.setattr(notebook_builder, "ROOT", tmp_path)
    diagram = tmp_path / "resources" / "flow.svg"
    diagram.parent.mkdir()
    diagram.write_text(SVG, encoding="utf-8")
    source = _write_source(tmp_path / "lesson.py", diagram="resources/flow.svg")

    notebook = notebook_builder.notebook_from_source(source)

    attachment = notebook["cells"][0]["attachments"]["flow.svg"][SVG_MIME]
    assert base64.b64decode(attachment, validate=True) == diagram.read_bytes()
    _assert_attached_diagrams(notebook)


@pytest.mark.unit
@pytest.mark.parametrize("case", ["code", "outside_root", "non_svg", "mismatched_reference"])
def test_source_builder_rejects_invalid_diagram_markers(tmp_path, monkeypatch, case):
    course = tmp_path / "course"
    course.mkdir()
    monkeypatch.setattr(notebook_builder, "ROOT", course)
    (course / "flow.svg").write_text(SVG, encoding="utf-8")
    (tmp_path / "outside.svg").write_text(SVG, encoding="utf-8")
    (course / "flow.txt").write_text(SVG, encoding="utf-8")
    options = {
        "code": {"diagram": "flow.svg", "kind": "code"},
        "outside_root": {"diagram": "../outside.svg"},
        "non_svg": {"diagram": "flow.txt", "reference": "flow.txt"},
        "mismatched_reference": {"diagram": "flow.svg", "reference": "wrong.svg"},
    }
    source = _write_source(course / "lesson.py", **options[case])

    with pytest.raises(ValueError):
        notebook_builder.notebook_from_source(source)


@pytest.mark.unit
@pytest.mark.parametrize("filename", notebook_builder.CORE_FILENAMES)
def test_required_notebooks_have_accessible_embedded_diagrams_and_clear_actions(repo_root, filename):
    notebook = json.loads((repo_root / "notebooks" / filename).read_text(encoding="utf-8"))
    _assert_attached_diagrams(notebook)
    assert not any(cell["id"].startswith("design-checkpoint-") for cell in notebook["cells"])
    intro = []
    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            break
        intro.append("".join(cell["source"]))
    for action in ("Run", "Edit", "Inspect", "Finish"):
        assert re.search(r"\b" + action + r"\b", "\n".join(intro), re.IGNORECASE), (filename, action)


@pytest.mark.unit
@pytest.mark.parametrize("filename", notebook_builder.CORE_FILENAMES)
def test_html_export_renders_embedded_diagrams_without_source_files(repo_root, tmp_path, monkeypatch, filename):
    notebook = json.loads((repo_root / "notebooks" / filename).read_text(encoding="utf-8"))
    cells = _diagram_cells(notebook)
    assert cells
    # Export only the self-contained cells from an unrelated, empty directory.
    portable = nbformat.reads(json.dumps({**notebook, "cells": cells}), as_version=4)
    monkeypatch.chdir(tmp_path)

    html, _ = HTMLExporter().from_notebook_node(portable)

    assert "attachment:" not in html
    assert html.count("data:image/svg+xml;base64,") >= len(cells)
    for cell in cells:
        for content in cell["attachments"].values():
            assert content[SVG_MIME] in html


@pytest.mark.unit
def test_learner_pack_preserves_embedded_diagram_payloads(repo_root):
    payload = package_files(repo_root)
    for filename in notebook_builder.CORE_FILENAMES:
        name = "notebooks/" + filename
        original = json.loads((repo_root / name).read_text(encoding="utf-8"))
        packaged = json.loads(payload[name])
        original_cells = {cell["id"]: cell for cell in _diagram_cells(original)}
        packaged_cells = {cell["id"]: cell for cell in _diagram_cells(packaged)}
        assert original_cells.keys() == packaged_cells.keys()
        for cell_id, cell in original_cells.items():
            assert packaged_cells[cell_id]["attachments"] == cell["attachments"]
            assert set(ATTACHMENT_REFERENCE.findall("".join(packaged_cells[cell_id]["source"]))) == set(cell["attachments"])
        _assert_attached_diagrams(packaged)
