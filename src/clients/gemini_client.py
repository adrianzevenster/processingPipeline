"""
Simple wrapper for external Gemini API.
"""
import requests
from utils.config import GEMINI_ENDPOINT_URL, GEMINI_API_KEY

class GeminiClient:
    def __init__(self):
        self.url = GEMINI_ENDPOINT_URL
        self.headers = {"Authorization": f"Bearer {GEMINI_API_KEY}"}

    def analyze(self, prompt: str) -> dict:
        r = requests.post(self.url, json={"prompt": prompt}, headers=self.headers)
        r.raise_for_status()
        return r.json()