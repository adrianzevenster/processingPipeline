"""
pytest configuration: add project root to PYTHONPATH so tests can import modules under src/ directory.
"""
import sys
from pathlib import Path
# Insert project root (parent directory of this tests folder) into sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Stub out DocumentAIClient initialization to prevent credential errors during tests
import pytest
from src.clients.documentai_client import DocumentAIClient

@pytest.fixture(autouse=True)
def dummy_client_init(monkeypatch):
    """Replace DocumentAIClient.__init__ so no real GCP credential checks occur."""
    monkeypatch.setattr(DocumentAIClient, '__init__', lambda self: None)