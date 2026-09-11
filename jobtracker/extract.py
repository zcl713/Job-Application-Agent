"""Turns free-text job postings/notes into structured fields via the Groq API."""

import json
from typing import Optional

from groq import Groq
from pydantic import BaseModel

from jobtracker import config

# Groq's strict JSON-schema mode (guaranteed-valid output) is only supported
# on a few models -- the GPT-OSS ones. Other Groq models only do best-effort JSON.
MODEL = "openai/gpt-oss-20b"

SYSTEM_PROMPT = (
    "You extract structured job-application details from free text pasted by the user "
    "(a job posting, or a quick note like 'applied to Acme, Data Analyst, via LinkedIn'). "
    "Leave a field null if it isn't stated or can't be confidently inferred -- never guess."
)

RESPONSE_SCHEMA = {
    "type": "json_schema",
    "json_schema": {
        "name": "job_extraction",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "company": {"type": ["string", "null"]},
                "role": {"type": ["string", "null"]},
                "location": {"type": ["string", "null"]},
                "work_mode": {"type": ["string", "null"]},
                "source": {"type": ["string", "null"]},
                "salary_range": {"type": ["string", "null"]},
                "job_link": {"type": ["string", "null"]},
            },
            "required": [
                "company",
                "role",
                "location",
                "work_mode",
                "source",
                "salary_range",
                "job_link",
            ],
            "additionalProperties": False,
        },
    },
}


class JobExtraction(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    location: Optional[str] = None
    work_mode: Optional[str] = None  # e.g. Remote, Hybrid, On-site
    source: Optional[str] = None  # e.g. LinkedIn, company website, referral
    salary_range: Optional[str] = None
    job_link: Optional[str] = None


def extract(text: str) -> JobExtraction:
    if not config.GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is not set. Add it to your .env file.")

    client = Groq(api_key=config.GROQ_API_KEY)
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
        response_format=RESPONSE_SCHEMA,
    )
    data = json.loads(completion.choices[0].message.content)
    return JobExtraction(**data)
