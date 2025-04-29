"""
Validates API entities against custom-extracted entities.
"""
from typing import List, Dict, Tuple
from utils.ocr_helpers import extract_custom_entities


def validate_entities(api_entities: List[Dict], text: str) -> List[Dict]:
    """
    Compare API entities to locally extracted ones, with normalization.

    Args:
        api_entities: API-returned list of dicts ('type_', 'mention_text').
        text: Raw text to extract custom entities from.
    Returns:
        List of entities augmented with 'valid' boolean.
    """
    custom: List[Tuple[str, str]] = extract_custom_entities(text)
    validated: List[Dict] = []

    for entity in api_entities:
        label = entity.get("type_")
        val = entity.get("mention_text")

        # Normalize: strip '$', commas, whitespace
        if isinstance(val, str):
            normalized = val.lstrip('$').replace(',', '').strip()
        else:
            normalized = val

        # Check raw or normalized against custom tuples
        valid = (label, val) in custom or (label, normalized) in custom
        validated.append({**entity, "valid": valid})

    return validated