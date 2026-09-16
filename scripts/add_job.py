"""Extracts job details from a posting and appends a row to the Tracker sheet.

Run from the project root (or use the `add-app` shortcut, see README):
    .venv/Scripts/python.exe scripts/add_job.py [url]

If a URL is given, the agent tries to fetch and read the page itself. If
that fails -- the site blocks scraping, renders content via JavaScript, or
the page comes back empty -- it falls back to prompting you to paste the
text instead. With no URL, it goes straight to the paste prompt. Finish
pasted input with Ctrl+Z then Enter (Windows) or Ctrl+D (macOS/Linux).

Fields the agent can't confidently extract (Referral/Contact, Next Step,
Next Step Date, Notes) are left blank for you to fill in directly in the
sheet.
"""

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import requests
from bs4 import BeautifulSoup

from jobtracker.extract import extract
from jobtracker.sheets import append_row

DEFAULT_STATUS = "Applied"

# Below this many characters, treat a fetched page as blocked/JS-rendered/empty.
MIN_FETCHED_LENGTH = 200

REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}


def fetch_page_text(url: str) -> str:
    response = requests.get(url, headers=REQUEST_HEADERS, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    lines = [line.strip() for line in soup.get_text(separator="\n").splitlines() if line.strip()]
    return "\n".join(lines)


def prompt_for_paste() -> str:
    print("Paste the job posting or note below.")
    print("When done, press Enter then Ctrl+Z then Enter (Windows) or Ctrl+D (macOS/Linux):\n")
    return sys.stdin.read().strip()


def main():
    url = sys.argv[1] if len(sys.argv) > 1 else None
    text = ""

    if url:
        try:
            text = fetch_page_text(url)
        except requests.RequestException as exc:
            print(f"Couldn't fetch the URL automatically ({exc}).")
            text = ""

        if len(text) < MIN_FETCHED_LENGTH:
            print("Fetched page looks empty or blocked -- paste the posting instead.\n")
            text = prompt_for_paste()
    else:
        text = prompt_for_paste()

    if not text:
        print("No text entered -- nothing added.")
        return

    result = extract(text)
    if url and not result.job_link:
        result.job_link = url

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
        # Job Description: full text, kept in case the posting is taken down.
        # Collapsed to one line so the row doesn't grow to fit embedded newlines
        # (Sheets expands rows for real line breaks no matter the wrap setting).
        " ".join(text.split()),
    ]
    append_row(row)
    print("\nAdded to the Tracker sheet.")


if __name__ == "__main__":
    main()
