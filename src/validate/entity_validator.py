"""
Validates entities from API against custom extractions.
"""
from typing import List, Dict, Tuple
from utils.ocr_helpers import extract_custom_entities


def validate_entities(api_entities: List[Dict], text: str) -> List[Dict]:
    """Compare API entities to locally extracted ones."""
    custom: List[Tuple[str, str]] = extract_custom_entities(text)
    validated: List[Dict] = []
    for ent in api_entities:
        label = ent.get("type_")
        val = ent.get("mention_text")
        valid = (label, val) in custom
        validated.append({**ent, "valid": valid})
    return validated