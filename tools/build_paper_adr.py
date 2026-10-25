"""Build the one-page paper Capstone ADR using ReportLab.

Run with a Python environment containing reportlab. The worksheet section in INSTRUCTOR_PLAYBOOK.md remains the accessible text
companion to the print worksheet.
"""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    Flowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "pdf/capstone_paper_adr_quick_sheet.pdf"
INK = colors.HexColor("#17212B")
MUTED = colors.HexColor("#455565")
LINE = colors.HexColor("#B8C2CC")


class WritingLines(Flowable):
    def __init__(self, width: float, count: int = 3):
        super().__init__()
        self.width = width
        self.height = count * 16
        self.count = count

    def draw(self):
        self.canv.setStrokeColor(LINE)
        self.canv.setLineWidth(0.45)
        for index in range(self.count):
            y = self.height - 12 - index * 16
            self.canv.line(0, y, self.width, y)


def build() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=38,
        rightMargin=38,
        topMargin=32,
        bottomMargin=30,
        title="Capstone Paper ADR - Offline Fallback",
        author="Managing Multi-Agent Teams",
    )
    width = A4[0] - 76
    styles = {
        "title": ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=19, leading=23, textColor=INK, spaceAfter=7),
        "body": ParagraphStyle("body", fontName="Helvetica", fontSize=10.2, leading=13.2, textColor=INK, spaceAfter=6),
        "question": ParagraphStyle("question", fontName="Helvetica-Bold", fontSize=11.4, leading=15, textColor=INK, spaceAfter=4),
        "anchor": ParagraphStyle("anchor", fontName="Helvetica", fontSize=9, leading=11.5, textColor=MUTED, spaceAfter=3),
        "small": ParagraphStyle("small", fontName="Helvetica", fontSize=8.8, leading=11.3, textColor=MUTED, spaceAfter=5),
        "score": ParagraphStyle("score", fontName="Helvetica-Bold", fontSize=10.2, leading=13, textColor=INK),
    }
    story = [
        Paragraph("Capstone Paper ADR", styles["title"]),
        Paragraph("Offline fallback - three questions, 20 ADR marks", styles["body"]),
        Paragraph("Use when a device, package, power, or connectivity failure prevents execution. Write short answers or pseudo-code. No code execution is required.", styles["body"]),
        Paragraph("<b>Learner:</b> __________________________ <b>Date:</b> ____________ <b>Case:</b> ______________", styles["body"]),
        Spacer(1, 6),
    ]
    questions = [
        (
            "1. Contract and architecture - 6 marks",
            "What risk does the Development-to-Security boundary address? Name the DevDeliverable fields and sketch how the Coordinator validates the handoff before Security starts.",
            "<b>Scoring:</b> concrete risk (2); correct fields and validation rule (2); explanation of the Development, Coordinator, and Security boundaries (2).",
        ),
        (
            "2. Governance and evidence - 7 marks",
            "Which tools may the Manager, Coder, QA, Pen Tester, and Security Manager use? What test or audit evidence would show the boundaries held? Label evidence as observed or proposed.",
            "<b>Scoring:</b> Development role/tool separation (2); scan and approval separation (2); contract rejection and ordered audit evidence (2); observed/proposed distinction (1).",
        ),
        (
            "3. Production next step - 7 marks",
            "What is the largest remaining risk, what concrete control would you add before production, and how would you check that the control works?",
            "<b>Scoring:</b> specific remaining risk (2); control and credible rationale (3); practical verification or acceptance check (2).",
        ),
    ]
    for title, prompt, anchor in questions:
        story.extend([
            Paragraph(title, styles["question"]),
            Paragraph(prompt, styles["body"]),
            WritingLines(width),
            Paragraph(anchor, styles["anchor"]),
            Spacer(1, 9),
        ])
    table = Table(
        [[Paragraph("Q1 ____ / 6", styles["score"]), Paragraph("Q2 ____ / 7", styles["score"]), Paragraph("Q3 ____ / 7", styles["score"]), Paragraph("Total ____ / 20", styles["score"])]],
        colWidths=[width * .23, width * .23, width * .23, width * .31],
    )
    table.setStyle(TableStyle([
        ("LINEABOVE", (0, 0), (-1, 0), .8, INK),
        ("LINEBELOW", (0, 0), (-1, -1), .8, INK),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.extend([
        table,
        Spacer(1, 8),
        Paragraph("<b>Assessor:</b> ___________________ <b>Feedback / accommodation record:</b> _________________________", styles["small"]),
        Paragraph("Award partial credit within each allocation. Sound reasoning satisfies the accepted Capstone fallback pass condition. Record these marks in ADR &amp; defense /20. This sheet awards ADR marks only and does not create code execution evidence or code marks.", styles["small"]),
        Paragraph("If code could not be assessed, leave its mark blank and record the reason or an explicitly agreed accommodation. The course tracker leaves the total blank while a required component is missing.", styles["small"]),
    ])
    document.build(story)
    print(OUTPUT)


if __name__ == "__main__":
    build()
