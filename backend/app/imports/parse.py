"""Ingredient line parsing: "2 ząbki czosnku, posiekane" -> amount, unit, name, note.

Deterministic and language-light (Polish and English). It splits a line into
parts; it does not decide which food the name is (see ``match``). Anything it
cannot read stays in ``name`` so the matcher and, later, the LLM step can see it.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from fractions import Fraction

from app.core.text import fold
from app.nutrition.units import UNIT_ALIASES

_VULGAR = {"½": 0.5, "⅓": 1 / 3, "⅔": 2 / 3, "¼": 0.25, "¾": 0.75, "⅛": 0.125}
_NUMBER = r"\d+(?:[.,]\d+)?(?:\s*/\s*\d+)?"
# "1 1/2", "1½", "2-3", "2\u20133" (en dash), "½"
_AMOUNT = re.compile(
    rf"^\s*(?P<a>{_NUMBER}(?:\s+\d+\s*/\s*\d+)?|[{''.join(_VULGAR)}])"
    rf"(?P<v>[{''.join(_VULGAR)}])?"
    rf"(?:\s*[-\u2013]\s*(?P<b>{_NUMBER}))?"
)
# phrases meaning "no fixed amount"
_TO_TASTE = ("do smaku", "to taste", "as needed", "opcjonalnie", "optional", "według uznania")
# words between the unit and the name that carry no meaning
_FILLERS = {"of", "a", "an"}
# "sól i pieprz", "salt and pepper", "oil or butter": more than one ingredient
_JOINERS = re.compile(r"\s(?:i|oraz|lub|albo|and|or|&|\+)\s", re.IGNORECASE)
# a comma that starts a note, not a decimal comma ("2,5 dkg")
_NOTE_COMMA = re.compile(r"(?<!\d),|,(?!\d)")


@dataclass(frozen=True, slots=True)
class ParsedLine:
    raw: str
    amount: float | None
    unit: str | None  # a code from app.nutrition.units, None if not stated
    name: str
    note: str | None = None
    optional: bool = False
    # the name joins several ingredients ("salt and pepper"): ask, don't guess
    several: bool = False


def _number(text: str) -> float:
    text = text.replace(",", ".").strip()
    if " " in text and "/" in text:  # "1 1/2"
        whole, frac = text.split(None, 1)
        return float(whole) + float(Fraction(frac.replace(" ", "")))
    if "/" in text:
        return float(Fraction(text.replace(" ", "")))
    return float(text)


def _amount(text: str) -> tuple[float | None, str]:
    m = _AMOUNT.match(text)
    if not m:
        return None, text
    a = m.group("a")
    value = _VULGAR[a] if a in _VULGAR else _number(a)
    if m.group("v"):
        value += _VULGAR[m.group("v")]
    if m.group("b"):  # a range: take the middle
        value = (value + _number(m.group("b"))) / 2
    return value, text[m.end() :]


def _unit(text: str) -> tuple[str | None, str]:
    rest = text.lstrip()
    # "200g", "1.5kg" leave the unit glued to nothing after the number was taken
    words = rest.split()
    if not words:
        return None, rest
    for n in (2, 1):  # "fl oz" before "fl"
        if len(words) >= n:
            candidate = fold(" ".join(words[:n]))
            code = UNIT_ALIASES.get(candidate) or UNIT_ALIASES.get(candidate.rstrip("."))
            if code:
                return code, " ".join(words[n:])
    return None, rest


def parse_line(raw: str) -> ParsedLine:
    text = " ".join(raw.replace("\u00a0", " ").split()).lstrip("-•*· ").strip()
    optional = False
    folded = fold(text)
    for phrase in _TO_TASTE:
        if phrase in folded:
            optional = True
            idx = folded.find(phrase)
            text = (text[:idx] + text[idx + len(phrase) :]).strip(" ,;")
            folded = fold(text)

    notes = [n.strip() for n in re.findall(r"\(([^)]*)\)", text) if n.strip()]
    text = re.sub(r"\([^)]*\)", " ", text)
    parts = _NOTE_COMMA.split(text, maxsplit=1)
    if len(parts) == 2:
        text, after = parts
        if after.strip():
            notes.append(after.strip())

    amount, rest = _amount(text)
    unit, rest = _unit(rest) if amount is not None else _unit(text)
    if amount is None and unit is not None:  # "szczypta soli": one of the unit
        amount = 1.0
    if amount is None:
        rest = text if unit is None else rest

    words = [w for w in rest.split() if fold(w) not in _FILLERS]
    name = " ".join(words).strip(" .,;:")
    return ParsedLine(
        raw=raw,
        amount=amount,
        unit=unit,
        name=name,
        note="; ".join(notes) or None,
        optional=optional,
        several=bool(_JOINERS.search(f" {name} ")),
    )
