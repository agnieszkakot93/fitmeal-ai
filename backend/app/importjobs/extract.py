"""From a page or pasted text to a draft recipe: title, ingredient lines, steps.

Link import reads schema.org JSON-LD (``app.imports.page``). Text import is
meant to go through the LLM step (Development Plan §2.4); until Bedrock is
cleared (AWS DPA, §7.4) a deterministic splitter stands in for it. Either way
the lines then go through ``parse`` and ``match``, so nutrition never comes
from the model.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field, replace
from typing import Any

from app.core.text import fold
from app.importjobs.scrub import scrub
from app.imports.page import MAX_LINE_CHARS, MAX_LINES, MAX_NAME_CHARS, PageRecipe
from app.imports.parse import parse_line

_INGREDIENT_HEADERS = {"skladniki", "ingredients", "you will need", "potrzebujesz"}
_STEP_HEADERS = {
    "przygotowanie",
    "sposob przygotowania",
    "wykonanie",
    "instructions",
    "method",
    "directions",
    "steps",
    "preparation",
}
# "4 porcje", "porcje: 4", "serves 4", "servings: 2", "makes 12", "yield: 6"
_SERVINGS_LINE = re.compile(
    r"^(?:(?:porcj\w*|serves|servings?|makes|yield|na)\s*:?\s*(?P<a>\d{1,3})\b"
    r"|(?P<b>\d{1,3})\s*(?:porcj\w*|servings?|osob\w*|people)\b)",
)
_FIRST_INT = re.compile(r"\d{1,3}")
_BULLET = re.compile(r"^\s*(?:[-•*·]\s*|\d{1,2}[.)]\s+)")
_POLISH = re.compile(r"[ąćęłńóśźż]", re.IGNORECASE)
_MAX_TITLE_WORDS = 12
_MAX_SHORT_INGREDIENT_WORDS = 4
_MAX_SCANNED_LINES = 4 * MAX_LINES  # "sól", "salt and pepper": no amount, still an ingredient


@dataclass(frozen=True, slots=True)
class Draft:
    """A recipe before matching: what the import cache stores."""

    title: str | None
    ingredients: list[str]
    instructions: list[str] = field(default_factory=list)
    servings: int | None = None
    language: str = "en"

    def to_json(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Draft:
        return cls(**data)

    def scrubbed(self) -> Draft:
        """Personal data and links cut out of every text field (``scrub``)."""
        return replace(
            self,
            title=scrub(self.title) or None if self.title else None,
            ingredients=[t for t in map(scrub, self.ingredients) if t],
            instructions=[t for t in map(scrub, self.instructions) if t],
        )


def servings_from(value: str | None) -> int | None:
    """ "4", "4 porcje", ["2", "2 servings"] already flattened by ``page``."""
    if not value:
        return None
    m = _FIRST_INT.search(value)
    n = int(m.group()) if m else 0
    return n if 1 <= n <= 100 else None


def _language(declared: str | None, sample: str) -> str:
    if declared:
        return "pl" if fold(declared).startswith("pl") else "en"
    return "pl" if _POLISH.search(sample) else "en"


def from_page(page: PageRecipe) -> Draft:
    draft = Draft(
        title=page.name,
        ingredients=page.ingredients,
        instructions=page.instructions,
        servings=servings_from(page.servings),
        language=_language(page.language, " ".join([page.name or "", *page.ingredients])),
    )
    return draft.scrubbed()


def llm_extract(text: str) -> Draft | None:
    """BEDROCK HOOK (Development Plan §2.4, §7.7). Not wired: blocked on the AWS DPA.

    When it is: strip personal data from ``text`` first, call Haiku with
    structured output, no tools and ``max_tokens`` set, validate the result
    strictly, and return only recipe fields. The model's confidence may only
    lower the deterministic match scores, never raise them. Returning None
    falls back to ``split_text``.
    """
    return None


def _header(line: str) -> str | None:
    key = fold(line).strip(" :#*-").rstrip(":")
    if key in _INGREDIENT_HEADERS:
        return "ingredients"
    if key in _STEP_HEADERS:
        return "steps"
    return None


def _servings_line(line: str) -> int | None:
    m = _SERVINGS_LINE.match(fold(line))
    if not m:
        return None
    return servings_from(m.group("a") or m.group("b"))


def _looks_like_ingredient(line: str) -> bool:
    parsed = parse_line(line)
    if parsed.amount is not None or parsed.unit is not None or parsed.optional:
        return True
    return 0 < len(line.split()) <= _MAX_SHORT_INGREDIENT_WORDS


def split_text(text: str) -> Draft:
    """Pasted text to a draft, by section headers when present, else line by line.

    Without headers, the first line is the title when it has no amount, and
    lines read as ingredients until the first long line without an amount,
    which starts the steps.
    """
    raw_lines = text.splitlines()[:_MAX_SCANNED_LINES]
    lines = [" ".join(raw.split())[:MAX_LINE_CHARS] for raw in raw_lines]
    lines = [line for line in lines if line]
    title: str | None = None
    servings: int | None = None
    ingredients: list[str] = []
    steps: list[str] = []
    has_headers = any(_header(line) for line in lines)
    section = None if has_headers else "ingredients"
    for i, line in enumerate(lines):
        if (found := _header(line)) is not None:
            section = found
            continue
        if servings is None and (n := _servings_line(line)) is not None:
            servings = n
            continue
        if section is None or (
            i == 0
            and not has_headers
            and len(line.split()) <= _MAX_TITLE_WORDS
            and parse_line(line).amount is None
            and len(lines) > 1
        ):
            # before any header, or the first line: the title
            title = title or line[:MAX_NAME_CHARS]
            continue
        if section == "ingredients" and (has_headers or _looks_like_ingredient(line)):
            ingredients.append(_BULLET.sub("", line) if line[:1] in "-•*·" else line)
        else:
            section = "steps"
            steps.append(_BULLET.sub("", line))
    return Draft(
        title=title,
        ingredients=ingredients[:MAX_LINES],
        instructions=steps[:MAX_LINES],
        servings=servings,
        language=_language(None, text[:2000]),
    )


def from_text(text: str) -> Draft:
    return (llm_extract(text) or split_text(text)).scrubbed()
