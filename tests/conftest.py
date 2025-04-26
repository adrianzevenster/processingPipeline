# tests/conftest.py

import sys
from pathlib import Path

# 1) Make the project root and src/ importable
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(1, str(project_root / "src"))

import pytest
from clients.documentai_client import DocumentAIClient

# 2) Stub out the DocumentAIClient __init__ so it doesn’t require real credentials
@pytest.fixture(autouse=True)
def dummy_client_init(monkeypatch):
    """Prevent DocumentAIClient from validating/accessing real GCP during tests."""
    monkeypatch.setattr(DocumentAIClient, "__init__", lambda self: None)
