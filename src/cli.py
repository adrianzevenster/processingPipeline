"""
Command-line interface to run the document authentication pipeline.
"""
import os
import sys
from pathlib import Path

# Ensure project's src folder is in sys.path when invoked via console script
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

import click
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

    # Initialize clients (requires GCP credentials)
    try:
        dai = DocumentAIClient()
        gem = GeminiClient()
    except Exception as e:
        import sys
        from google.auth.exceptions import DefaultCredentialsError
        if isinstance(e, DefaultCredentialsError):
            click.echo("Error: GCP credentials not found. Please set the GOOGLE_APPLICATION_CREDENTIALS environment variable to your service account JSON, or run 'gcloud auth application-default login'.")
            sys.exit(1)
        else:
            raise


    # Process each document
    all_docs = {**pdf_texts, **img_texts}
    for name, text in all_docs.items():
        cleaned = clean_text(text)
        # Document AI processing with fallback on PermissionDenied
        from google.api_core.exceptions import PermissionDenied
        try:
            doc = dai.process(cleaned.encode('utf-8'), 'text/plain')
        except PermissionDenied:
            click.echo(f"Warning: permission denied processing document '{name}', skipping Document AI extraction.")
            # Fallback to dummy doc with no entities
            class _DummyDoc:
                entities = []
            doc = _DummyDoc()
        api_entities = [{'type_': e.type_, 'mention_text': e.mention_text} for e in doc.entities]
        # Validate entities
        results = validate_entities(api_entities, cleaned)
        # Write results
        (dst / f"{name}_results.json").write_text(str(results))

    click.echo(f"Processed {len(all_docs)} documents.")

if __name__ == '__main__':
    cli()