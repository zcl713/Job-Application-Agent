# Job Application Tracker Agent

A small agent that turns a pasted job posting (or a quick note like "applied
to Acme, Data Analyst, via LinkedIn") into a new row in a Google Sheet.

It extracts the structured details it can confidently infer via the Groq API
(company, role, location, work mode, source, salary range, job link), fills
in today's date as the applied date, and stores the full pasted text in a
"Job Description" column so you still have the posting if it's ever taken
down. Anything it can't infer (referral/contact, next step, next step date,
notes) is left blank for you to fill in by hand as the application progresses.

## Setup

1. **Install dependencies**

   ```
   python -m venv .venv
   .venv/Scripts/python.exe -m pip install -r requirements.txt
   ```

2. **Create a Google service account** (one-time)
   - In Google Cloud Console, create a project, enable the Google Sheets API,
     and create a service account.
   - Download its JSON key and save it as `credentials/service_account.json`
     (this path is gitignored — never commit it).
   - Create a Google Sheet for tracking applications and share it with the
     service account's email address (found in the JSON key) with Editor access.

3. **Get a Groq API key** from [console.groq.com/keys](https://console.groq.com/keys).

4. **Configure environment variables**

   Copy `.env.example` to `.env` and fill in:
   - `SPREADSHEET_ID` — the ID from your sheet's URL
     (`https://docs.google.com/spreadsheets/d/THIS_PART/edit`)
   - `GOOGLE_CREDENTIALS_PATH` — only needed if it differs from the default
     `credentials/service_account.json`
   - `GROQ_API_KEY` — can instead be set as an OS-level environment variable
     if you'd rather not put it in `.env`

5. **Lay out the sheet** (one-time, safe to re-run)

   ```
   .venv/Scripts/python.exe scripts/setup_sheet.py
   ```

   This renames the first tab to "Tracker", writes the header row, adds a
   Status dropdown, and adds an auto-computed "Days Since Applied" column.

## Usage

Run the agent and paste in a job posting or a quick note:

```
.venv/Scripts/python.exe scripts/add_job.py
```

Paste the text, then finish input with **Ctrl+Z then Enter** (Windows) or
**Ctrl+D** (macOS/Linux). The agent prints what it extracted and appends a
new row to the Tracker sheet with:

- Extracted fields (company, role, location, work mode, source, salary range, job link)
- **Status** defaulted to `Applied`
- **Date Applied** set to today
- **Job Description** set to the full text you pasted

Afterwards, open the sheet to fill in Referral/Contact, Next Step, Next Step
Date, and Notes, and to update Status as the application progresses.

## Project structure

```
jobtracker/
  config.py    Loads settings from .env / environment variables
  extract.py   Groq-based extraction of structured fields from free text
  sheets.py    Google Sheets connection and row-appending
scripts/
  setup_sheet.py     One-time Tracker tab layout (headers, dropdown, formula)
  add_job.py         Main entry point: paste text -> extract -> append row
  test_connection.py Manual test: appends a fake row to confirm sheet access
  test_extract.py    Manual test: runs a sample posting through extraction
```

## Testing

```
.venv/Scripts/python.exe scripts/test_extract.py     # verify Groq extraction
.venv/Scripts/python.exe scripts/test_connection.py  # verify sheet read/write access
```
