from src.transform.cleaner import clean_text


def test_clean_text_removes_control_chars_and_excess_whitespace():
    dirty = "Hello	World Foo Bar"
    cleaned = clean_text(dirty)
    assert "	" not in cleaned
    assert "    " not in cleaned
    assert "  " not in cleaned
    assert cleaned == "Hello World Foo Bar"