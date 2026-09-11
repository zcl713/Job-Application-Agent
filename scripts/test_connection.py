"""Quick manual test: appends one obviously-fake row to confirm auth + sharing work.

Run from the project root:
    .venv/Scripts/python.exe scripts/test_connection.py
"""

import sys
from pathlib import Path

# Allow running this script directly (`python scripts/test_connection.py`)
# by putting the project root on the import path.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from jobtracker.sheets import append_row

TEST_ROW = [
    "Test Company",       # Company
    "Test Role",          # Role
    "Applied",             # Status
    "2026-09-11",          # Date Applied
    "Remote",               # Location
    "Remote",               # Work Mode
    "",                     # Salary Range
    "Test Script",          # Source
    "",                     # Referral/Contact
    "",                     # Next Step
    "",                     # Next Step Date
    "",                     # Job Link
    "This row confirms the connection works — feel free to delete it.",  # Notes
    "",                     # Job Description
]

if __name__ == "__main__":
    append_row(TEST_ROW)
    print("Success! Check the Tracker tab for a new 'Test Company' row.")
