from pathlib import Path
from PyPDF2 import PdfReader


def load_pdf(path: Path) -> str:
    reader = PdfReader(str(path))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def ingest_pdfs(source: Path) -> dict:
    texts = {}
    for file in source.glob("*.pdf"):
        texts[file.name] = load_pdf(file)
    return texts