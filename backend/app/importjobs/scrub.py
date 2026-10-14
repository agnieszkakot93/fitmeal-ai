"""Removing what isn't recipe from imported text (Development Plan §7.2, §7.7).

Until the LLM step rewrites steps in our own words, titles, steps and lines
are kept only after URLs, emails, phone numbers, PESEL and IBAN numbers are
cut out. Nine or more digits in a row (with spaces or dashes) are never an
amount, so ingredient lines survive.
"""

from __future__ import annotations

import re

# C0 controls and DEL, except tab and newline; Postgres rejects NUL outright
CONTROLS = re.compile(r"[\x00-\x08\x0b-\x1f\x7f]")
_PATTERNS = [
    re.compile(r"\b(?:https?://|www\.)\S+", re.IGNORECASE),
    re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+"),
    re.compile(r"\b[A-Z]{2}\d{2}(?:[ ]?[A-Z0-9]{4}){3,7}(?:[ ]?[A-Z0-9]{1,3})?\b"),  # IBAN
    re.compile(r"(?:\+\d{1,3}[ -]?)?\(?\d(?:[ ()-]?\d){8,}"),  # phones, PESEL, long ids
]


def controls(text: str) -> str:
    """Control characters become spaces (PDF text carries form feeds)."""
    return CONTROLS.sub(" ", text)


def scrub(text: str) -> str:
    text = controls(text)
    for pattern in _PATTERNS:
        text = pattern.sub(" ", text)
    return " ".join(text.split())
