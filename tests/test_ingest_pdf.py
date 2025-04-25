import pytest
from pathlib import Path
from src.ingest.ingest_pdf import load_pdf, ingest_pdfs
from PyPDF2 import PdfWriter

@pytest.fixture
def sample_pdf(tmp_path):
    path = tmp_path / "sample.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    with open(path, "wb") as f:
        writer.write(f)
    return path


def test_load_pdf_returns_string(sample_pdf):
    text = load_pdf(sample_pdf)
    assert isinstance(text, str)


def test_ingest_pdfs(sample_pdf):
    dir = sample_pdf.parent
    result = ingest_pdfs(dir)
    assert sample_pdf.name in result
    assert isinstance(result[sample_pdf.name], str)