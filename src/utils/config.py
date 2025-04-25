"""
Configuration loader for environment variables.
"""
import os
from dotenv import load_dotenv

# Load .env file into environment
load_dotenv()

# GCP config (optional)
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
GCP_LOCATION = os.getenv("GCP_LOCATION")
GCP_PROCESSOR_ID = os.getenv("GCP_PROCESSOR_ID")

# Gemini config
GEMINI_ENDPOINT_URL = os.getenv("GEMINI_ENDPOINT_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Input/Output dirs
INPUT_DIR = os.getenv("INPUT_DIR")
OUTPUT_DIR = os.getenv("OUTPUT_DIR")