"""Render the authoritative leadership Markdown as a one-page A4 PDF.

Run with a Python environment containing reportlab and pypdf, for example the
Codex bundled workspace Python. The source uses headings, paragraphs and bold
text only; unsupported Markdown fails rather than disappearing from the PDF.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from xml.sax.saxutils import escape

from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "leadership/executive_brief.md"
OUTPUT = ROOT / "pdf/executive_brief_governed_multi_agent_training.pdf"
TITLE = "Executive Brief: Governed Multi-Agent AI Training Curriculum"
INK = colors.HexColor("#1E1E24")
PAPER = colors.HexColor("#F8F9FA")
ACCENT = colors.HexColor("#0066FF")


def register_fonts(font_dir: Path) -> None:
    """Embed Arial; use --font-dir for an installation outside macOS."""
    for face, filename in (("Arial", "Arial.ttf"), ("Arial-Bold", "Arial Bold.ttf")):
        path = font_dir / filename
        if not path.is_file():
            raise FileNotFoundError(f"Arial font missing: {path}; supply --font-dir")
        pdfmetrics.registerFont(TTFont(face, str(path)))
    pdfmetrics.registerFontFamily("Arial", normal="Arial", bold="Arial-Bold")


def inline(text: str) -> str:
    """Escape source text before translating the supported bold span syntax."""
    chunks = re.split(r"(\*\*.*?\*\*)", text)
    return "".join(
        f"<b>{escape(chunk[2:-2])}</b>" if chunk.startswith("**") else escape(chunk)
        for chunk in chunks
    )


def read_blocks(source: Path) -> list[tuple[str, str]]:
    blocks: list[tuple[str, str]] = []
    for block in source.read_text(encoding="utf-8").strip().split("\n\n"):
        block = block.strip()
        if not block:
            continue
        if block.startswith("# "):
            blocks.append(("title", block[2:]))
        elif block.startswith("## "):
            blocks.append(("heading", block[3:]))
        else:
            if re.search(r"(?m)^(?:#|[-*>]|\d+\.)\s|\[[^\]]+\]\(|`", block):
                raise ValueError("Source contains unsupported Markdown")
            blocks.append(("body", " ".join(block.splitlines())))
    if not blocks or blocks[0] != ("title", TITLE):
        raise ValueError(f"Source must begin with the exact title: {TITLE}")
    if sum(kind == "title" for kind, _ in blocks) != 1:
        raise ValueError("Source must contain one title")
    return blocks


def decorate(canvas, document) -> None:
    canvas.saveState()
    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, *A4, fill=1, stroke=0)
    canvas.setFillColor(ACCENT)
    canvas.rect(document.leftMargin, A4[1] - 36, 42, 3, fill=1, stroke=0)
    canvas.setStrokeColor(ACCENT)
    canvas.setLineWidth(0.5)
    canvas.line(document.leftMargin, 34, A4[0] - document.rightMargin, 34)
    canvas.restoreState()


def build(source: Path, output: Path, font_dir: Path) -> None:
    register_fonts(font_dir)
    blocks = read_blocks(source)
    styles = {
        "title": ParagraphStyle(
            "title", fontName="Arial-Bold", fontSize=21, leading=24.8,
            textColor=INK, spaceAfter=13,
        ),
        "heading": ParagraphStyle(
            "heading", fontName="Arial-Bold", fontSize=11.3, leading=14,
            textColor=ACCENT, spaceBefore=8.7, spaceAfter=3, keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "body", fontName="Arial", fontSize=10.7, leading=14.2,
            textColor=INK, spaceAfter=5,
        ),
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(
        str(output), pagesize=A4, leftMargin=45, rightMargin=45,
        topMargin=51, bottomMargin=43, title=TITLE,
        author="Managing Multi-Agent Teams", pageCompression=1,
    )
    document.build(
        [Paragraph(inline(text), styles[kind]) for kind, text in blocks],
        onFirstPage=decorate, onLaterPages=decorate,
    )
    reader = PdfReader(output)
    if len(reader.pages) != 1:
        raise ValueError(f"Expected one page, rendered {len(reader.pages)}; shorten the source")
    extracted = " ".join(reader.pages[0].extract_text().split())
    expected = " ".join(re.sub(r"\*\*(.*?)\*\*", r"\1", text) for _, text in blocks)
    if extracted != " ".join(expected.split()):
        raise ValueError("PDF text differs from the authoritative Markdown")
    print(f"Built {output}")
    print(f"Pages: 1; source words: {len(expected.split())}; font: embedded Arial")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument(
        "--font-dir", type=Path, default=Path("/System/Library/Fonts/Supplemental"),
        help="Directory containing Arial.ttf and Arial Bold.ttf",
    )
    args = parser.parse_args()
    build(args.source, args.output, args.font_dir)
