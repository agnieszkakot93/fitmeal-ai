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
from app.imports.parse import ParsedLine
from app.nutrition.units import FoodUnitData, UnitConversionError, to_grams

CLARIFY_BELOW = 0.7
MIN_NAME_SCORE = 0.3
# Polish case endings ("mleka", "kaszy gryczanej") keep trigram scores moderate even
# for the right food. A moderate score that is well clear of every other food is
# as good as a strong one.
CLEAR_WINNER_SCORE = 0.45
CLEAR_WINNER_MARGIN = 0.15
CLEAR_WINNER_CONFIDENCE = 0.8

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
    """The name, plus word stems so Polish case endings still hit prefixes."""
    folded = fold(name)
    words = folded.split()
    variants = [folded]
    if len(words) == 1 and len(folded) > 5:
        variants.append(folded[: max(4, len(folded) - 2)])  # czosnku -> czosn
    return variants


async def _find(session: AsyncSession, name: str) -> list[tuple[FoodItem, float, float]]:
    """Foods with (best score over name variants, score of the full name), best first.

    The full-name score breaks ties between stems: "czosnku" -> "czosn" prefixes both
    garlic and garlic powder, but the full word is closer to garlic.
    """
    found: dict[str, tuple[FoodItem, float, float]] = {}
    for i, query in enumerate(_variants(name)):
        for food, score in await foods_repo.search(session, query, limit=5):
            _, best, full = found.get(food.slug, (food, 0.0, 0.0))
            found[food.slug] = (food, max(best, score), score if i == 0 else full)
    return sorted(found.values(), key=lambda f: (-f[1], -f[2], f[0].slug))


def _grams(line: ParsedLine, food: FoodItem) -> tuple[float | None, float, str | None]:
    units = FoodUnitData(food.density_g_per_ml, {p.unit: p.grams for p in food.portions})
    seasoning = CulinaryRole.SEASONING.value in food.culinary_roles
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


async def match_line(session: AsyncSession, line: ParsedLine) -> Match:
    """Needs foods with ``portions`` loaded; ``search`` returns them."""
    if not line.name:
        return Match(line, None, None, 0.0, reason="no ingredient name")
    if line.several:
        return Match(line, None, None, 0.0, reason="several ingredients in one line")
    found = await _find(session, line.name)
    candidates = [(f.slug, round(best, 3)) for f, best, _ in found[:5]]
    if not found or found[0][1] < MIN_NAME_SCORE:
        return Match(line, None, None, 0.0, candidates, reason="unknown ingredient")
    food, name_score, full = found[0]
    runner_up = found[1] if len(found) > 1 else None
    if runner_up and runner_up[1] >= name_score - 0.02 and runner_up[2] >= full - 0.02:
        # can't tell two foods apart
        name_score = min(name_score, CLARIFY_BELOW - 0.01)
    elif name_score >= CLEAR_WINNER_SCORE and (
        runner_up is None or name_score - runner_up[1] >= CLEAR_WINNER_MARGIN
    ):
        name_score = max(name_score, CLEAR_WINNER_CONFIDENCE)
    grams, unit_score, reason = _grams(line, food)
    confidence = round(min(name_score, unit_score), 3)
    if reason is None and confidence < CLARIFY_BELOW:
        reason = "which ingredient?"
    return Match(line, food.slug, grams, confidence, candidates, reason)
