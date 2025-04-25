"""
Command-line interface to run the document authentication pipeline.
"""
import os
import click
from pathlib import Path
from ingest.ingest_pdf import ingest_pdfs
from ingest.ingest_image import ingest_images
from transform.cleaner import clean_text
from clients.documentai_client import DocumentAIClient
from clients.gemini_client import GeminiClient
from validate.entity_validator import validate_entities
from utils.config import INPUT_DIR, OUTPUT_DIR


def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)

@click.group()
def cli():
    """Pipeline CLI entry point."""
    pass

@cli.command()
@click.option('--input-dir', default=lambda: os.getenv('INPUT_DIR'), help='Input directory')
@click.option('--output-dir', default=lambda: os.getenv('OUTPUT_DIR'), help='Output directory')
def run(input_dir, output_dir):
    """Run full ingestion, processing, and validation pipeline."""
    src = Path(input_dir)
    dst = Path(output_dir)
    ensure_dir(dst)

    # Ingest
    pdf_texts = ingest_pdfs(src)
    img_texts = ingest_images(src)

    # Clients
    dai = DocumentAIClient()
    gem = GeminiClient()

    # Process docs
    for name, text in {**pdf_texts, **img_texts}.items():
        cleaned = clean_text(text)
        # Document AI
        doc = dai.process(cleaned.encode('utf-8'), 'text/plain')
        api_entities = [{'type_': e.type_, 'mention_text': e.mention_text} for e in doc.entities]
        results = validate_entities(api_entities, cleaned)
        (dst / f"{name}_results.json").write_text(str(results))

    click.echo(f"Processed {len(pdf_texts)+len(img_texts)} documents.")

if __name__ == '__main__':
    cli()