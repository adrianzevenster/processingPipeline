from pathlib import Path
from ingest.ingest_pdf import load_pdf, ingest_pdfs
from PyPDF2 import PdfWriter

def create_pdf(path: Path):
    w = PdfWriter()
    w.add_blank_page(72,72)
    with open(path, 'wb') as f:
        w.write(f)


def test_load_pdf(tmp_path):
    p = tmp_path / 'a.pdf'
    create_pdf(p)
    assert isinstance(load_pdf(p), str)


def test_ingest_pdf(tmp_path):
    p = tmp_path / 'a.pdf'; create_pdf(p)
    res = ingest_pdfs(tmp_path)
    assert 'a.pdf' in res