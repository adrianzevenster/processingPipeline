# tests/test_entity_matcher.py

from validate.entity_matcher import match_entities

def test_match_entities_all_present():
    text = "2025-07-01 $100.00"
    api_entities = [
        {'type_': 'DATE',   'mention_text': '2025-07-01'},
        {'type_': 'AMOUNT', 'mention_text': '$100.00'}
    ]
    result = match_entities(text, api_entities)

    # Custom extraction strips the '$' on amounts
    assert result['custom'] == [
        {'type': 'DATE',   'value': '2025-07-01'},
        {'type': 'AMOUNT', 'value': '100.00'}
    ]
    # All custom entities should be found in API response
    assert result['matches'] == result['custom']
    assert result['missing'] == []

def test_match_entities_missing_some():
    text = "2025-12-31 $42.50 extra"
    api_entities = [
        {'type_': 'DATE', 'mention_text': '2025-12-31'}
        # Note: AMOUNT is absent
    ]
    result = match_entities(text, api_entities)

    # Custom gives both DATE and AMOUNT
    assert {'type': 'DATE',   'value': '2025-12-31'} in result['custom']
    assert {'type': 'AMOUNT', 'value': '42.50'} in result['custom']

    # DATE should match, AMOUNT should be missing
    assert {'type': 'DATE',   'value': '2025-12-31'} in result['matches']
    assert {'type': 'AMOUNT', 'value': '42.50'} in result['missing']
