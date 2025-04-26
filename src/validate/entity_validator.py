"""
Validates API entities against locally extracted entities.
"""
from typing import List, Dict, Tuple
from utils.ocr_helpers import extract_custom_entities


def validate_entities(api_entities: List[Dict], text: str) -> List[Dict]:
    """
    Compare API entities against locally extracted entities, with normalization.

    Args:
        api_entities: List of dicts from API, each with 'type_' and 'mention_text'.
        text: Raw text to extract custom entities from.

    Returns:
        List of entities augmented with 'valid' boolean.
    """
    # Extract custom entities from the text
    custom: List[Tuple[str, str]] = extract_custom_entities(text)
    validated: List[Dict] = []

    for entity in api_entities:
        label = entity.get("type_")
        val = entity.get("mention_text")

        # Normalize numeric values (e.g., strip leading '$' and whitespace)
        if isinstance(val, str):
            normalized = val.lstrip('$').strip()
        else:
            normalized = val

        # Determine validity: match original or normalized value
        is_valid = (label, val) in custom or (label, normalized) in custom

        # Append result
        validated.append({**entity, "valid": is_valid})

    return validated