from io import BytesIO
from pathlib import Path
import re
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt
from fpdf import FPDF
from backend.utils.sanitizer import sanitize_text
PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOGO_PATH = PROJECT_ROOT / "assets" / "logo.png"

def _lines(text): return sanitize_text(text).split("\n")
def format_txt(text): return sanitize_text(text).encode("utf-8")

def format_docx(text, doc_type):
    doc = Document(); s = doc.sections[0]
    s.top_margin=s.bottom_margin=Inches(.7); s.left_margin=s.right_margin=Inches(.85)
    if LOGO_PATH.exists():
        p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.add_run().add_picture(str(LOGO_PATH), width=Inches(1.1))
    p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    r=p.add_run(doc_type.title()); r.bold=True; r.font.name="Times New Roman"; r.font.size=Pt(16)
    numbered=[]
    for line in _lines(text):
        if not line: continue
        p=doc.add_paragraph(); p.paragraph_format.space_after=Pt(6); p.paragraph_format.line_spacing=1.15
        heading = bool(len(line) < 90 and (line.isupper() or re.match(r"^\d+[.)]\s+[A-Z]", line) or line.lower().startswith(("document status", "parties", "terms"))))
        if re.match(r"^\d+[\.)]\s+", line): numbered.append(re.sub(r"^\d+[\.)]\s+", "", line))
    if numbered:
        doc.add_paragraph(); table=doc.add_table(rows=1, cols=2); table.style="Table Grid"
        table.rows[0].cells[0].text="No."; table.rows[0].cells[1].text="Clause"
        for i,term in enumerate(numbered,1):
            cells=table.add_row().cells; cells[0].text=str(i); cells[1].text=term
    f=s.footer.paragraphs[0]; f.alignment=WD_ALIGN_PARAGRAPH.CENTER; rr=f.add_run("LegalEase - AI-assisted document draft"); rr.font.size=Pt(8)
    out=BytesIO(); doc.save(out); return out.getvalue()

class LegalEasePDF(FPDF):
    def __init__(self, doc_type): super().__init__(); self.doc_type=doc_type
    def header(self):
        if LOGO_PATH.exists():
            try: self.image(str(LOGO_PATH), x=90, y=8, w=30)
            except Exception: pass
        self.set_y(28); self.set_font("Helvetica","B",14); self.cell(0,8,self.doc_type.title(),align="C"); self.ln(10)
    def footer(self): self.set_y(-15); self.set_font("Helvetica",size=8); self.cell(0,8,"LegalEase - AI-assisted document draft",align="C")

def format_pdf(text, doc_type):
    pdf=LegalEasePDF(doc_type); pdf.set_auto_page_break(auto=True,margin=18); pdf.set_margins(18,42,18); pdf.add_page()
    for line in _lines(text):
        if not line: pdf.ln(3); continue
        heading=len(line)<90 and (line.isupper() or re.match(r"^\d+[\.)]\s+[A-Z]",line) or line.lower().startswith(("document status","parties","terms")))
        pdf.set_font("Helvetica","B" if heading else "",11 if heading else 10); pdf.multi_cell(0,6 if heading else 5.5,line); pdf.ln(1)
    return bytes(pdf.output())
