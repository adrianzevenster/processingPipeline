from transform.cleaner import clean_text

def test_clean_text_removes_control_chars_and_excess_whitespace():
    dirty = "Hello\tWorld\rFoo  Bar"
    cleaned = clean_text(dirty)
    assert "\t" not in cleaned
    assert "\r" not in cleaned
    assert "  " not in cleaned
    assert cleaned == "Hello World Foo Bar"
