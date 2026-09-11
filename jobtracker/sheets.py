"""Connects to the Job Application Tracker Google Sheet via a service account."""

import gspread
from google.oauth2.service_account import Credentials

from jobtracker import config

# Scope = the permission we're asking Google for: read/write access to Sheets.
# (Opening by ID rather than by name means we don't need Drive API access too.)
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

TRACKER_TAB = "Tracker"


def get_tracker_worksheet():
    creds = Credentials.from_service_account_file(
        str(config.GOOGLE_CREDENTIALS_PATH), scopes=SCOPES
    )
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(config.SPREADSHEET_ID)
    return spreadsheet.worksheet(TRACKER_TAB)


def append_row(values: list):
    """Appends one row to the bottom of the Tracker tab.

    `values` must be in the same column order as the sheet header.
    """
    worksheet = get_tracker_worksheet()
    worksheet.append_row(values, value_input_option="USER_ENTERED")
