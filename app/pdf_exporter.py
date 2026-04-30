from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, black
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import mm
import re

ORANGE = HexColor("#E67E22")
DARK = HexColor("#2C3E50")

class PDFExporter:
    def clean(self, text):
        text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
        text = re.sub(r"[#]+", "", text)
        return text.strip()

    def export(self, report: str, filename: str, title: str, location: str, date: str):
        doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=20*mm,
            leftMargin=20*mm,
            topMargin=20*mm,
            bottomMargin=20*mm
        )

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle("title",
            fontSize=18, textColor=ORANGE, alignment=1,
            fontName="Helvetica-Bold", spaceAfter=4)

        subtitle_style = ParagraphStyle("subtitle",
            fontSize=10, textColor=HexColor("#777777"), alignment=1,
            fontName="Helvetica", spaceAfter=10)

        heading_style = ParagraphStyle("heading",
            fontSize=12, textColor=ORANGE,
            fontName="Helvetica-Bold", spaceBefore=8, spaceAfter=4)

        body_style = ParagraphStyle("body",
            fontSize=10, textColor=DARK,
            fontName="Helvetica", spaceAfter=3, leading=15)

        bullet_style = ParagraphStyle("bullet",
            fontSize=10, textColor=DARK,
            fontName="Helvetica", spaceAfter=3,
            leftIndent=15, leading=15)

        story = []

        # Title & subtitle
        story.append(Paragraph(title, title_style))
        story.append(Paragraph(f"Location: {location} &nbsp;&nbsp;|&nbsp;&nbsp; Date: {date}", subtitle_style))
        story.append(Spacer(1, 6*mm))

        # Parse report lines
        for line in report.split("\n"):
            line = line.strip()

            if not line:
                story.append(Spacer(1, 3*mm))
                continue

            # Section headings
            if re.match(r"^(###|\*\*)\s*\d+\.", line):
                clean = self.clean(line)
                story.append(Paragraph(clean, heading_style))

            # Bullet points
            elif line.startswith("*") or line.startswith("-"):
                clean = re.sub(r"^[\*\-]+\s*", "- ", line)
                clean = self.clean(clean)
                story.append(Paragraph(clean, bullet_style))

            # Normal text
            else:
                clean = self.clean(line)
                if clean:
                    story.append(Paragraph(clean, body_style))

        doc.build(story)
        #uses ReportLab 
