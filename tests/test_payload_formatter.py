from validate.payload_formatter import build_validation_payload

def test_build_validation_payload():
    text = "2025-07-01 $1,234.56 random content"
    payload = build_validation_payload(text)
    assert 'entities' in payload
    assert {'type': 'DATE',   'value': '2025-07-01'} in payload['entities']
    assert {'type': 'AMOUNT', 'value': '1,234.56'} in payload['entities']
