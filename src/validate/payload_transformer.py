"""
Formats custom-extracted entities into structured API request payloads.
"""
from typing import List, Dict, Tuple
from utils.ocr_helpers import extract_custom_entities


def build_validation_payload(text: str) -> Dict[str, List[Dict[str, str]]]:
    """
    Creates a payload mapping each extracted entity to a dict for API calls.

    Args:
        text: Raw document text.
    Returns:
        A dict with key 'entities', list of dicts with 'type' and 'value'.
    """
    custom: List[Tuple[str, str]] = extract_custom_entities(text)
    return {
        'entities': [
            {'type': label, 'value': value}
            for label, value in custom
        ]
    }
