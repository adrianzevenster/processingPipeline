"""
Command-line interface to run the document authentication pipeline.
"""
import os
import sys
from pathlib import Path
# Insert project root and src directory into PYTHONPATH for pytest
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(1, str(project_root / 'src'))
import json
import click
from pathlib import Path

# Ensure project's src folder is in sys.path when invoked via console script
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

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

    # Handle raw JSON creds in CI
    cred_env = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', '')
    if cred_env.strip().startswith('{'):
        temp_dir = Path(os.getenv('RUNNER_TEMP', dst.parent))
        temp_dir.mkdir(parents=True, exist_ok=True)
        sa_file = temp_dir / 'service-account.json'
        sa_file.write_text(cred_env)
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(sa_file)

    # Ingest
    pdf_texts = ingest_pdfs(src)
    img_texts = ingest_images(src)

    # Initialize clients
    try:
        dai = DocumentAIClient()
        gem = GeminiClient()
    except Exception as e:
        from google.auth.exceptions import DefaultCredentialsError
        if isinstance(e, DefaultCredentialsError):
            click.echo(
                "Error: GCP credentials not found. "
                "Set GOOGLE_APPLICATION_CREDENTIALS or run gcloud auth application-default login."
            )
            sys.exit(1)
        raise

    all_docs = {**pdf_texts, **img_texts}
    for name, text in all_docs.items():
        cleaned = clean_text(text)
        # Document AI with fallback
        from google.api_core.exceptions import PermissionDenied
        try:
            doc = dai.process(cleaned.encode('utf-8'), 'text/plain')
        except PermissionDenied:
            click.echo(f"Warning: permission denied for '{name}', skipping Document AI.")
            class _DummyDoc: entities = []
            doc = _DummyDoc()

        # Extract entities
        api_entities = [
            {'type_': e.type_, 'mention_text': e.mention_text} for e in doc.entities
        ]
        # Validate entities
        results = validate_entities(api_entities, cleaned)
        (dst / f"{name}_results.json").write_text(json.dumps(results, indent=2))

        # Summarize metrics
        try:
            confidences = [e.confidence for e in doc.entities]
            avg_conf = sum(confidences) / len(confidences) if confidences else None
        except AttributeError:
            avg_conf = None
        try:
            gem_resp = gem.analyze(cleaned)
            gem_conf = gem_resp.get('confidence')
            gem_out = gem_resp.get('output', gem_resp)
        except Exception:
            gem_conf = None
            gem_out = None

        summary = {
            'document': name,
            'num_api_entities': len(api_entities),
            'avg_entity_confidence': avg_conf,
            'gemini_output': gem_out,
            'gemini_confidence': gem_conf,
        }
        (dst / f"{name}_summary.json").write_text(json.dumps(summary, indent=2))

    click.echo(f"Processed {len(all_docs)} documents.")

if __name__ == '__main__':
    cli()