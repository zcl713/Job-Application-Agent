"""Quick manual test: runs a sample job posting through extraction and prints the result.

Run from the project root:
    .venv/Scripts/python.exe scripts/test_extract.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from jobtracker.extract import extract

SAMPLE_TEXT = """
Acme Robotics is hiring a Senior Data Analyst in Austin, TX (hybrid, 3 days/week
in office). $95,000-$115,000/year. Apply via our careers page:
https://acme.example.com/careers/data-analyst
"""

if __name__ == "__main__":
    result = extract(SAMPLE_TEXT)
    print(result.model_dump_json(indent=2))
