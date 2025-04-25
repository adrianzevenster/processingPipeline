"""
Cleans and normalizes extracted text.
"""
import re

def clean_text(text: str) -> str:
    text = re.sub(r"[\r\t]", " ", text)
    text = re.sub(r" +", " ", text)
    return text.strip()