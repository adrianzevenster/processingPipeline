"""
Helper functions for custom entity extraction (e.g., regex-based).
"""
import re
from typing import List, Tuple

ENTITY_PATTERNS = {
    "DATE": r"\b\d{4}-\d{2}-\d{2}\b",
    "AMOUNT": r"\b\$?\d+(?:,\d{3})*(?:\.\d{2})?\b",
}


def extract_custom_entities(text: str) -> List[Tuple[str, str]]:
    """Extract entities from text using predefined regex patterns."""
    matches: List[Tuple[str, str]] = []
    for label, pattern in ENTITY_PATTERNS.items():
        for m in re.finditer(pattern, text):
            matches.append((label, m.group(0)))
    return matches