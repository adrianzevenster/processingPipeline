from typing import List, Dict, Tuple
from src.utils.ocr_helpers import extract_custom_entities


def validate_entities(api_entities: List[Dict], text: str) -> List[Dict]:
    """
    Compare API entities against locally extracted entities, normalizing values as needed.

    Args:
        api_entities: List of dicts from API with keys 'type_' and 'mention_text'.
        text: The raw text to extract custom entities from.

    Returns:
        List of entities with an additional 'valid' boolean key.
    """
    custom: List[Tuple[str, str]] = extract_custom_entities(text)
    validated: List[Dict] = []
    for entity in api_entities:
        label = entity.get("type_")
        val = entity.get("mention_text")
        # Normalize currency values by stripping leading '$' or spaces
        val_stripped = val.lstrip('$ ') if isinstance(val, str) else val
        # Check both original and normalized value against custom patterns
        is_valid = (label, val) in custom or (label, val_stripped) in custom
        validated.append({**entity, "valid": is_valid})
    return validated