"""One-off setup script: turns a blank 'Sheet1' into the Tracker tab layout.

Run once, from the project root:
    .venv/Scripts/python.exe scripts/setup_sheet.py

Safe to re-run — it just re-applies the same header/formula/dropdown.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import gspread
from google.oauth2.service_account import Credentials
from gspread.utils import ValidationConditionType

from jobtracker import config
from jobtracker.sheets import SCOPES, TRACKER_TAB

HEADERS = [
    "Company",
    "Role",
    "Status",
    "Date Applied",
    "Location",
    "Work Mode",
    "Salary Range",
    "Source",
    "Referral/Contact",
    "Next Step",
    "Next Step Date",
    "Job Link",
    "Notes",
    "Job Description",
    "Days Since Applied",
]

STATUS_VALUES = [
    "Not Applied Yet",
    "Applied",
    "OA/Assessment",
    "Phone Screen",
    "Interviewing",
    "Offer",
    "Accepted",
    "Rejected",
    "Withdrawn",
    "Ghosted",
]

# Column O = Days Since Applied, column D = Date Applied (both 1-indexed: D=4, O=15)
DAYS_SINCE_FORMULA = '=ARRAYFORMULA(IF(D2:D="","",TODAY()-D2:D))'


def main():
    creds = Credentials.from_service_account_file(
        str(config.GOOGLE_CREDENTIALS_PATH), scopes=SCOPES
    )
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(config.SPREADSHEET_ID)

    worksheet = spreadsheet.sheet1
    if worksheet.title != TRACKER_TAB:
        worksheet.update_title(TRACKER_TAB)
        print(f"Renamed '{worksheet.title}' tab to '{TRACKER_TAB}'.")

    worksheet.update(values=[HEADERS], range_name="A1")
    worksheet.format("A1:O1", {"textFormat": {"bold": True}})
    print("Header row written.")

    worksheet.add_validation(
        "C2:C1000",
        ValidationConditionType.one_of_list,
        STATUS_VALUES,
        showCustomUi=True,
    )
    print("Status dropdown added (C2:C1000).")

    worksheet.update(values=[[DAYS_SINCE_FORMULA]], range_name="O2", raw=False)
    print("Days Since Applied auto-formula added at O2 (spills down automatically).")

    # Job Description (column N) holds long pasted text. Clip it instead of
    # wrapping so rows stay a fixed height rather than growing to fit the text.
    worksheet.format("N2:N1000", {"wrapStrategy": "CLIP"})
    print("Job Description column set to clip (no row expansion) on paste.")


if __name__ == "__main__":
    main()
