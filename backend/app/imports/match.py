"""Matching parsed ingredient lines to foods, with a confidence score (PRD §8.1).

Every line gets a confidence in [0, 1]: the lower of how well the name matched
a food alias and how sure we are about the amount in grams. Below
``CLARIFY_BELOW`` the import asks the user instead of guessing. An LLM step
added later may only lower these scores, never raise them (Development Plan §7.7).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.text import fold
from app.foods import repository as foods_repo
from app.foods.models import FoodItem
from app.foods.vocab import CulinaryRole
from app.imports import words
from app.imports.parse import ParsedLine
from app.nutrition.units import FoodUnitData, UnitConversionError, to_grams

CLARIFY_BELOW = 0.7
MIN_NAME_SCORE = 0.3
_SEARCH_LIMIT = 15
# name scores below a whole-word match: they always ask
_EXTRA_WORD = 0.5  # every alias word found, plus a word the food doesn't know
_PARTIAL = 0.6  # times the share of an alias' words found
# trigram-only matches (no whole word in common, e.g. a typo) never pass unasked
_TRIGRAM_CAP = CLARIFY_BELOW - 0.01

# unit certainty
_SURE = 1.0
_ASSUMED_PIECE = 0.85  # "3 eggs": a piece is the obvious unit
_PINCH_TO_TASTE = 0.9  # "salt to taste" on a seasoning
_UNKNOWN = 0.4  # amount or unit we can't turn into grams


@dataclass(frozen=True, slots=True)
class Match:
    line: ParsedLine
    slug: str | None
    grams: float | None
    confidence: float
    candidates: list[tuple[str, float]] = field(default_factory=list)
    reason: str | None = None  # why the user is asked, when needs_clarification

    @property
    def needs_clarification(self) -> bool:
        return self.slug is None or self.grams is None or self.confidence < CLARIFY_BELOW


def _variants(name: str) -> list[str]:
    """Search queries: the whole name, plus each word's shortest stem.

    The stems pull in foods whose aliases share a word in another case
    ("oliwy" -> "oliw" finds "oliwa"); ``_name_score`` then judges them word by word.
    """
    variants = [fold(name)]
    for word in words.tokens(name):
        for stem in sorted(fold(s) for s in words.stems(word)):
            if len(stem) >= 3 and stem not in variants:
                variants.append(stem)
    return variants


async def _find(session: AsyncSession, name: str) -> list[tuple[FoodItem, float, float]]:
    """Candidate foods with (best trigram score over variants, score of the full name)."""
    found: dict[str, tuple[FoodItem, float, float]] = {}
    for i, query in enumerate(_variants(name)):
        for food, score in await foods_repo.search(session, query, limit=_SEARCH_LIMIT):
            _, best, full = found.get(food.slug, (food, 0.0, 0.0))
            found[food.slug] = (food, max(best, score), score if i == 0 else full)
    return sorted(found.values(), key=lambda f: (-f[1], -f[2], f[0].slug))


def _name_score(name_words: list[str], food: FoodItem) -> tuple[float, int]:
    """How well the line's words name this food, by whole words in any case.

    1.0: some alias has all its words in the line, and every other word of the
    line is a descriptor ("ciepłego") or a word of another alias of the same
    food ("płatków owsianych górskich"). An extra unknown word ("oat flour" vs
    "flour", "sesame oil" vs "sesame") means it may be another food: ask.
    The second number, the line words the best alias covers, ranks equal scores.
    """
    if not name_words:
        return 0.0, 0
    aliases = [words.tokens(a.alias) for a in food.aliases]
    vocabulary = {w for alias in aliases for w in alias}
    unknown = [
        q
        for q in name_words
        if not words.is_descriptor(q) and not any(words.same_word(q, v) for v in vocabulary)
    ]
    best = (0.0, 0)
    for alias in aliases:
        if not alias:
            continue
        covered = sum(any(words.same_word(a, q) for q in name_words) for a in alias)
        coverage = covered / len(alias)
        full = 1.0 if not unknown else _EXTRA_WORD
        best = max(best, (full if coverage == 1.0 else _PARTIAL * coverage, covered))
    return best


def _grams(line: ParsedLine, food: FoodItem) -> tuple[float | None, float, str | None]:
    units = FoodUnitData(food.density_g_per_ml, {p.unit: p.grams for p in food.portions})
    seasoning = CulinaryRole.SEASONING.value in food.culinary_roles
    if line.weight_g is not None:
        return line.weight_g, _SURE, None
    if line.amount is None:
        if seasoning and "pinch" in units.portions_g:  # type: ignore[operator]
            return to_grams(1, "pinch", units), _PINCH_TO_TASTE, None
        return None, _UNKNOWN, "how much?"
    if line.unit is None:
        if units.portions_g and "piece" in units.portions_g:
            return to_grams(line.amount, "piece", units), _ASSUMED_PIECE, None
        return None, _UNKNOWN, "which unit?"
    try:
        return to_grams(line.amount, line.unit, units), _SURE, None
    except UnitConversionError:
        return None, _UNKNOWN, f"how many grams is {line.amount:g} {line.unit}?"


def _pick(
    line: ParsedLine, scored: list[tuple[FoodItem, tuple[float, int]]]
) -> tuple[FoodItem, float]:
    """The best food and its name score; a tie between whole-word matches asks.

    "1 can crushed tomatoes" names both fresh and canned tomatoes; the unit
    settles it when only one of them comes in that unit.
    """
    food, (score, covered) = scored[0]
    # equal scores: the alias naming more of the line wins ("imbir mielony" over "imbir")
    tied = [f for f, (s, c) in scored if s >= score - 0.02 and c == covered]
    if line.unit is not None and len(tied) > 1:
        with_unit = [f for f in tied if any(p.unit == line.unit for p in f.portions)]
        if len(with_unit) == 1:
            return with_unit[0], score
    if line.unit == "can" and not any(p.unit == "can" for p in food.portions):
        # "1 puszka pomidorów": a canned food whose every line word is known wins
        canned = [
            f
            for f, (s, _) in scored
            if s >= _PARTIAL / 2 and any(p.unit == "can" for p in f.portions)
        ]
        if len(canned) == 1 and _knows_all(line.name, canned[0]):
            return canned[0], score
    if len(tied) > 1:
        return food, min(score, CLARIFY_BELOW - 0.01)
    return food, score


def _knows_all(name: str, food: FoodItem) -> bool:
    vocabulary = {w for a in food.aliases for w in words.tokens(a.alias)}
    return all(
        words.is_descriptor(q) or any(words.same_word(q, v) for v in vocabulary)
        for q in words.tokens(name)
    )


async def match_line(session: AsyncSession, line: ParsedLine) -> Match:
    """Needs foods with ``aliases`` and ``portions`` loaded; ``search`` returns them."""
    if not line.name:
        return Match(line, None, None, 0.0, reason="no ingredient name")
    if line.several:
        return Match(line, None, None, 0.0, reason="several ingredients in one line")
    found = await _find(session, line.name)
    name_words = words.tokens(line.name)
    scored = sorted(
        ((f, _name_score(name_words, f)) for f, _, _ in found),
        key=lambda fs: (-fs[1][0], -fs[1][1]),  # stable: trigram order breaks ties
    )
    candidates = [(f.slug, round(s, 3)) for f, (s, _) in scored[:5]]
    if scored and scored[0][1][0] >= MIN_NAME_SCORE:
        food, name_score = _pick(line, scored)
    elif found and found[0][1] >= MIN_NAME_SCORE:
        food, name_score = found[0][0], min(found[0][1], _TRIGRAM_CAP)
        candidates = [(f.slug, round(best, 3)) for f, best, _ in found[:5]]
    else:
        return Match(line, None, None, 0.0, candidates, reason="unknown ingredient")
    grams, unit_score, reason = _grams(line, food)
    confidence = round(min(name_score, unit_score), 3)
    if reason is None and confidence < CLARIFY_BELOW:
        reason = "which ingredient?"
    return Match(line, food.slug, grams, confidence, candidates, reason)
