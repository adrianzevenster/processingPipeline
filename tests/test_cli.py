"""
Integration tests for the CLI pipeline, using local sample PDF and image.
"""
from pathlib import Path
from click.testing import CliRunner
import pytest

# Import the CLI entry point directly (module installed at top level)
from src.cli import cli
from src.clients.documentai_client import DocumentAIClient

# Dummy document class to simulate Document AI response
class DummyDoc:
    entities = []

# Fixture to override DocumentAIClient.process to avoid real API calls
@pytest.fixture(autouse=True)
def dummy_documentai(monkeypatch):
    monkeypatch.setattr(
        DocumentAIClient,
        'process',
        lambda self, content, mime: DummyDoc()
    )

# Helpers to create sample PDF and image files

def create_sample_pdf(path: Path):
    from PyPDF2 import PdfWriter
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    with open(path, 'wb') as f:
        writer.write(f)


def create_sample_image(path: Path):
    from PIL import Image, ImageDraw
    img = Image.new('RGB', (100, 30), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), 'Hello', fill=(0, 0, 0))
    img.save(path)


def test_cli_run(tmp_path):
    input_dir = tmp_path / 'input'
    output_dir = tmp_path / 'output'
    input_dir.mkdir()
    # Create sample files
    create_sample_pdf(input_dir / 'test.pdf')
    create_sample_image(input_dir / 'test.png')

    runner = CliRunner()
    result = runner.invoke(
        cli,
        ['run',
         '--input-dir', str(input_dir),
         '--output-dir', str(output_dir)]
    )
    assert result.exit_code == 0
    # Check that result files were created
    files = list(output_dir.iterdir())
    assert any(f.name.endswith('_results.json') for f in files)