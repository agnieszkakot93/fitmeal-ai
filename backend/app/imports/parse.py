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
from app.imports.words import is_descriptor
from app.nutrition.units import UNIT_ALIASES, UNITS, UnitKind

_VULGAR = {"½": 0.5, "⅓": 1 / 3, "⅔": 2 / 3, "¼": 0.25, "¾": 0.75, "⅛": 0.125}
_NUMBER = r"\d+(?:[.,]\d+)?(?:\s*/\s*\d+)?"
# "1 1/2", "1½", "2-3", "2\u20133" (en dash), "½"
_AMOUNT = re.compile(
    rf"^\s*(?P<a>{_NUMBER}(?:\s+\d+\s*/\s*\d+)?|[{''.join(_VULGAR)}])"
    rf"(?:\s*(?P<v>[{''.join(_VULGAR)}]))?"
    rf"(?:\s*[-\u2013]\s*(?P<b>{_NUMBER}))?"
)
# phrases meaning "no fixed amount"
_TO_TASTE = ("do smaku", "to taste", "as needed", "opcjonalnie", "optional", "według uznania")
# words between the unit and the name that carry no meaning
_FILLERS = {"of", "a", "an"}
# "sól i pieprz", "salt and pepper", "oil or butter": more than one ingredient
_JOINERS = re.compile(r"\s(?:i|oraz|lub|albo|and|or|&|\+)\s", re.IGNORECASE)
# amounts written as words; "a"/"an" count only before a unit ("a handful of")
_WORD_AMOUNTS = {"pol": 0.5, "poltora": 1.5, "half": 0.5}
_ARTICLES = {"a", "an", "one"}
# "(ok. 300 g)", "(28 oz)", "(180 g each)": a weight stated in a note
_NOTE_WEIGHT = re.compile(
    rf"^(?:ok\.?|okolo|about|approx\.?|approximately|ca\.?|~)?\s*(?P<n>{_NUMBER})\s*"
    r"(?P<u>[a-z]+)\.?(?:\s+(?P<each>each|kazd\w*))?$"
)
# "coconut oil for the pan": what follows is a note
_PURPOSE = re.compile(r"\s+for\s+.*$", re.IGNORECASE)
# a can's stated weight includes the liquid the line pours away
_DRAINED = ("drained", "odsacz", "odciek")
# words in a comma tail that make it a note, not a second ingredient
_NOTE_WORDS = {"for", "to", "dla", "do", "na", "of", "z", "ze", "optional"}
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
    # a total weight stated in a note ("2 cukinie (ok. 600 g)"): it beats the portion
    weight_g: float | None = None


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
        words = text.split(None, 1)
        if words and fold(words[0]) in _WORD_AMOUNTS:
            return _WORD_AMOUNTS[fold(words[0])], words[1] if len(words) > 1 else ""
        if len(words) == 2 and fold(words[0]) in _ARTICLES and _unit(words[1])[0]:
            return 1.0, words[1]
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


def _unit_code(word: str) -> str | None:
    folded = fold(word).strip(".,")
    return UNIT_ALIASES.get(folded)


def _note_weight(notes: list[str], amount: float | None) -> float | None:
    for note in notes:
        m = _NOTE_WEIGHT.match(fold(note))
        code = _unit_code(m.group("u")) if m else None
        if m and code and UNITS[code].kind is UnitKind.MASS:
            grams = _number(m.group("n")) * UNITS[code].factor
            return grams * (amount or 1.0) if m.group("each") else grams
    return None


def _drained_can(unit: str | None, notes: list[str]) -> bool:
    return unit == "can" and any(d in fold(n) for n in notes for d in _DRAINED)


def _is_second_ingredient(tail: str) -> bool:
    """ "sól, pieprz": a short tail that names something rather than describing it."""
    words = tail.split()
    return 0 < len(words) <= 2 and not any(
        fold(w) in _NOTE_WORDS or is_descriptor(w) or _unit_code(w) for w in words
    )


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
    tail = ""
    if len(parts) == 2:
        text, tail = parts[0], parts[1].strip()

    amount, rest = _amount(text)
    unit, rest = _unit(rest) if amount is not None else _unit(text)
    if amount is None and unit is not None:  # "szczypta soli": one of the unit
        amount = 1.0
    if amount is None:
        rest = text if unit is None else rest

    words = [w for w in rest.split() if fold(w) not in _FILLERS]
    # "2 garlic cloves", "2 celery stalks": a portion unit after the name
    if amount is not None and unit is None and len(words) > 1:
        code = _unit_code(words[-1])
        if code and UNITS[code].kind is UnitKind.PORTION:
            unit, words = code, words[:-1]
    several = False
    if tail:
        tail_unit = _unit_code(tail) if len(tail.split()) == 1 else None
        if tail_unit and unit is None:  # "pomidorki koktajlowe, garść"
            unit, amount = tail_unit, amount or 1.0
        elif amount is None and unit is None and _is_second_ingredient(tail):
            several = True
        else:
            notes.append(tail)
    name = " ".join(words).strip(" .,;:")
    purpose = _PURPOSE.search(name)
    if purpose:
        notes.append(purpose.group().strip())
        name = name[: purpose.start()].strip()
    return ParsedLine(
        raw=raw,
        amount=amount,
        unit=unit,
        name=name,
        note="; ".join(notes) or None,
        optional=optional,
        several=several or bool(_JOINERS.search(f" {name} ")),
        weight_g=None if _drained_can(unit, notes) else _note_weight(notes, amount),
    )
