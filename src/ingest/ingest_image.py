"""
Ingests image files and extracts text via OCR.
"""
from pathlib import Path
from PIL import Image
import pytesseract
from pytesseract import TesseractNotFoundError


def load_image(path: Path) -> str:
    img = Image.open(path)
    try:
        return pytesseract.image_to_string(img)
    except TesseractNotFoundError:
        return ""


def ingest_images(source: Path) -> dict:
    texts = {}
    for ext in ("*.png", "*.jpg", "*.jpeg", "*.tiff"):
        for file in source.glob(ext):
            texts[file.name] = load_image(file)
    return texts