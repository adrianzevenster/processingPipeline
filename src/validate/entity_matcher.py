"""
Matches custom-extracted entities against API-returned entities.
"""
from typing import List, Dict, Tuple
from utils.ocr_helpers import extract_custom_entities


def match_entities(
        text: str,
        api_entities: List[Dict[str, str]]
) -> Dict[str, List[Dict[str, object]]]:
    """
    Compare custom-extracted entities to API entities, highlighting matches and missing items.

    Args:
        text: Raw document text.
        api_entities: List of dicts with 'type_' and 'mention_text'.
    Returns:
        Dict with keys 'custom', 'matches', 'missing'.
    """
    # Extract custom entities (raw values including commas)
    custom: List[Tuple[str, str]] = extract_custom_entities(text)
    custom_dicts = [{'type': t, 'value': v} for t, v in custom]

    matches = []
    missing = []
    for entity in custom_dicts:
        found = False
        for e in api_entities:
            api_label = e.get('type_')
            api_val = e.get('mention_text')
            if api_label != entity['type']:
                continue
            # Normalize API value
            norm = api_val.lstrip('$').replace(',', '').strip()
            if api_val == entity['value'] or norm == entity['value']:
                found = True
                break
        if found:
            matches.append(entity)
        else:
            missing.append(entity)

    return {
        'custom': custom_dicts,
        'matches': matches,
        'missing': missing
    }