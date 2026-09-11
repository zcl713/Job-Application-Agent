"""Loads settings from the .env file so no paths or keys are hardcoded elsewhere."""

import os
from pathlib import Path

from dotenv import load_dotenv

# BASE_DIR = the job-app-agent/ folder, regardless of where this script is run from
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

GOOGLE_CREDENTIALS_PATH = BASE_DIR / os.environ.get(
    "GOOGLE_CREDENTIALS_PATH", "credentials/service_account.json"
)
SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID", "")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
