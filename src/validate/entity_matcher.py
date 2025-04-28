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
    Compares custom-extracted entities to API entities, highlighting matches and misses.

    Args:
        text: Raw document text.
        api_entities: List of dicts with keys 'type_' and 'mention_text'.
    Returns:
        Dict with keys 'custom', 'matches', and 'missing'.
    """
    # 1) extract your own entities
    custom: List[Tuple[str, str]] = extract_custom_entities(text)
    custom_dicts = [{'type': t, 'value': v} for t, v in custom]

    matches = []
    missing = []
    for entity in custom_dicts:
        found = any(
            e['type_'] == entity['type'] and
            e['mention_text'] == entity['value']
            for e in api_entities
        )
        if found:
            matches.append(entity)
        else:
            missing.append(entity)

    return {
        'custom': custom_dicts,
        'matches': matches,
        'missing': missing
    }
