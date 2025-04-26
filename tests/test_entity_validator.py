from validate.entity_validator import validate_entities

def test_validate_entities_against_custom_patterns():
    text = "2025-04-25 $123.45"
    api_entities = [
        {"type_": "DATE",   "mention_text": "2025-04-25"},
        {"type_": "AMOUNT", "mention_text": "$123.45"},
        {"type_": "DATE",   "mention_text": "1999-01-01"},
    ]
    results = validate_entities(api_entities, text)
    assert results[0]["valid"] is True
    assert results[1]["valid"] is True
    assert results[2]["valid"] is False
