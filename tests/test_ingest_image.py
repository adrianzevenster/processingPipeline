import pytest
from pathlib import Path
from ingest.ingest_image import load_image, ingest_images
from PIL import Image

@pytest.fixture
def sample_image(tmp_path):
    path = tmp_path / "sample.png"
    img = Image.new("RGB", (10, 10), color="white")
    img.save(path)
    return path

def test_load_image_returns_text(sample_image, monkeypatch):
    monkeypatch.setattr("pytesseract.image_to_string", lambda img: "hello")
    text = load_image(sample_image)
    assert text == "hello"

def test_ingest_images(sample_image, monkeypatch):
    monkeypatch.setattr("pytesseract.image_to_string", lambda img: "world")
    result = ingest_images(sample_image.parent)
    assert sample_image.name in result
    assert result[sample_image.name] == "world"
