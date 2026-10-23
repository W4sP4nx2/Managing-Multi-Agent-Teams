"""Rebuild the seven offline handouts, maintained extensions, and CrewAI reference.

Editable cell sources live in tools/notebook_sources/*.py. Markdown lines are
comments beneath a JSON cell marker; code cells remain normal Python. Stable IDs
preserve links to assessment cells and test repair targets.
"""
from __future__ import annotations

import argparse
import base64
import json
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "tools/notebook_sources"
CORE_FILENAMES = (
    "00_sandbox_preflight.ipynb",
    "01_lab_pydantic.ipynb",
    "02_lab_crewai.ipynb",
    "03_lab_security.ipynb",
    "04_capstone.ipynb",
    "05_live_software_factory.ipynb",
    "06_local_cicd.ipynb",
)
BONUS_FILENAME = "bonus_live_demo.ipynb"
MOCK_CICD_FILENAME = "11_mock_cicd_pipeline.ipynb"
REFERENCE_FILENAME = "01_Bridge_Sequential_Crew.ipynb"


def notebook_from_source(path: Path) -> dict:
    cells = []
    marker = None
    lines = []

    def append_cell():
        if marker is None:
            return
        source = "\n".join(lines).strip("\n")
        cell = {"id": marker["id"], "cell_type": marker["type"], "metadata": {},
                "source": source.splitlines(keepends=True)}
        if "diagram" in marker:
            asset = (ROOT / marker["diagram"]).resolve()
            if (marker["type"] != "markdown" or not asset.is_relative_to(ROOT.resolve())
                    or asset.suffix.lower() != ".svg"):
                raise ValueError(f"Diagram must be a repository-local SVG in a Markdown cell: {path}")
            if f"attachment:{asset.name}" not in source:
                raise ValueError(f"Diagram attachment is not referenced in {path}: {asset.name}")
            svg = asset.read_bytes()
            if ElementTree.fromstring(svg).tag != "{http://www.w3.org/2000/svg}svg":
                raise ValueError(f"Diagram is not an SVG document: {asset}")
            cell["attachments"] = {asset.name: {
                "image/svg+xml": base64.b64encode(svg).decode("ascii"),
            }}
        if marker["type"] == "code":
            cell.update(execution_count=None, outputs=[])
        cells.append(cell)

    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# %% "):
            append_cell()
            marker = json.loads(line[len("# %% "):])
            if marker["type"] not in {"markdown", "code"}:
                raise ValueError(f"Unsupported cell type in {path}: {marker}")
            lines = []
        elif marker is None:
            if line.strip():
                raise ValueError(f"Content before first cell marker in {path}")
        elif marker["type"] == "markdown":
            if line == "#" or not line:
                lines.append("")
            elif line.startswith("# "):
                lines.append(line[2:])
            else:
                raise ValueError(f"Markdown must be commented in {path}: {line}")
        else:
            lines.append(line)
    append_cell()
    if not cells or len({cell["id"] for cell in cells}) != len(cells):
        raise ValueError(f"Missing cells or duplicate IDs in {path}")
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3.12", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.12"},
        },
        "nbformat": 4, "nbformat_minor": 5,
    }


def build(output_root: Path = ROOT, check: bool = False) -> list[Path]:
    paths = []
    targets = [("notebooks", name) for name in CORE_FILENAMES]
    targets.append(("extensions", BONUS_FILENAME))
    targets.append(("extensions", MOCK_CICD_FILENAME))
    targets.append(("crewai_learning", REFERENCE_FILENAME))
    for folder, filename in targets:
        payload = notebook_from_source(SOURCES / (Path(filename).stem + ".py"))
        rendered = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
        target = output_root / folder / filename
        if check:
            if not target.is_file() or json.loads(target.read_text(encoding="utf-8")) != payload:
                raise ValueError(f"Notebook differs from source: {target}; run tools/build_core_notebooks.py")
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(rendered, encoding="utf-8")
        paths.append(target)
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if a distributed notebook differs from source")
    args = parser.parse_args()
    for path in build(check=args.check):
        print(f"{'verified' if args.check else 'wrote'} {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
