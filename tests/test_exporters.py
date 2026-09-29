from backend.utils.exporters import format_docx,format_pdf,format_txt
SAMPLE="""TEST AGREEMENT\n\n1. PARTIES\nAlice, Example Corp\n\n2. TERMS\nPayment within 30 days.\n"""
def test_txt(): assert format_txt(SAMPLE).startswith(b"TEST AGREEMENT")
def test_docx(): assert format_docx(SAMPLE,"Test Agreement")[:2]==b"PK"
def test_pdf(): assert format_pdf(SAMPLE,"Test Agreement").startswith(b"%PDF")
