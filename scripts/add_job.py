"""Extracts job details from pasted text and appends a row to the Tracker sheet.

Run from the project root:
    .venv/Scripts/python.exe scripts/add_job.py

Paste the job posting (or a quick note) when prompted, then finish input with
Ctrl+Z followed by Enter (Windows) or Ctrl+D (macOS/Linux).

Fields the agent can't confidently extract (Referral/Contact, Next Step, Next
Step Date, Notes) are left blank for you to fill in directly in the sheet.
"""

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from jobtracker.extract import extract
from jobtracker.sheets import append_row

DEFAULT_STATUS = "Applied"


def main():
    print("Paste the job posting or note below.")
    print("When done, press Enter then Ctrl+Z then Enter (Windows) or Ctrl+D (macOS/Linux):\n")
    text = sys.stdin.read().strip()
    if not text:
        print("No text entered -- nothing added.")
        return

    result = extract(text)
    print("\nExtracted:")
    print(result.model_dump_json(indent=2))

    row = [
        result.company or "",
        result.role or "",
        DEFAULT_STATUS,
        date.today().isoformat(),
        result.location or "",
        result.work_mode or "",
        result.salary_range or "",
        result.source or "",
        "",  # Referral/Contact -- fill in manually
        "",  # Next Step -- fill in manually
        "",  # Next Step Date -- fill in manually
        result.job_link or "",
        "",  # Notes -- fill in manually
        text,  # Job Description -- full pasted text, kept in case the posting is taken down
    ]
    append_row(row)
    print("\nAdded to the Tracker sheet.")


if __name__ == "__main__":
    main()
