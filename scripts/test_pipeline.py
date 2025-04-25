"""
Automated local run of the pipeline: sets up `data/input` with sample PDF/image,
invokes the CLI, and lists outputs.
"""
import shutil
import sys
from pathlib import Path
from clients.documentai_client import DocumentAIClient
from clients.gemini_client import GeminiClient

class DummyDoc:
    entities = []

# Prevent actual GCP and Gemini calls:
DocumentAIClient.__init__ = lambda self: None
DocumentAIClient.process = lambda self, content, mime: DummyDoc()
GeminiClient.__init__ = lambda self: None
GeminiClient.analyze = lambda self, prompt: {}
# Add project root to PYTHONPATH so we can `import cli` directly
sys.path.insert(0, str(Path(__file__).parent.parent))

from click.testing import CliRunner
from cli import cli

# Define paths
project_root = Path(__file__).parent.parent
input_dir   = project_root / 'data' / 'input'
output_dir  = project_root / 'data' / 'output'

# Clean previous data directories
if input_dir.exists():
    shutil.rmtree(input_dir)
if output_dir.exists():
    shutil.rmtree(output_dir)

# Create fresh directories
for d in (input_dir, output_dir):
    d.mkdir(parents=True, exist_ok=True)

# Create sample PDF
from PyPDF2 import PdfWriter
pdf_path = input_dir / 'sample.pdf'
writer = PdfWriter()
writer.add_blank_page(width=72, height=72)
with open(pdf_path, 'wb') as f:
    writer.write(f)

# Create sample image
from PIL import Image, ImageDraw
img_path = input_dir / 'sample.png'
img = Image.new('RGB', (100, 30), color='white')
draw = ImageDraw.Draw(img)
draw.text((10, 10), 'Hello 2025-04-25 $123.45', fill='black')
img.save(img_path)

# Invoke the pipeline
runner = CliRunner()
result = runner.invoke(
    cli,
    ['run',
     '--input-dir', str(input_dir),
     '--output-dir', str(output_dir)]
)
print(result.output)
if result.exit_code != 0:
    raise SystemExit(f"Pipeline failed with exit code {result.exit_code}")

# List output files
outputs = list(output_dir.glob('*_results.json'))
print(f"Generated {len(outputs)} result file(s):")
for f in outputs:
    print(f" - {f.name}")
