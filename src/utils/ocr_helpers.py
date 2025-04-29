"""
Regex-based custom entity extraction patterns.
"""
import re
from typing import List, Tuple

ENTITY_PATTERNS = {
    "DATE": r"\b\d{4}-\d{2}-\d{2}\b",
    # Match amounts with two decimal places and optional thousands separators
    "AMOUNT": r"\b\d{1,3}(?:,\d{3})*\.\d{2}\b",
}


def extract_custom_entities(text: str) -> List[Tuple[str, str]]:
    """Extracts custom entities from the text using regex patterns."""
    matches: List[Tuple[str, str]] = []
    for label, pattern in ENTITY_PATTERNS.items():
        for m in re.finditer(pattern, text):
            # Keep raw matched text (including commas)
            matches.append((label, m.group(0)))
    return matches