"""Step 1: drop candidates that break a hard constraint (PRD §8.5).

Hard constraints are the user's allergies and strict intolerances (via the
recipe exclusion check), the max cooking time and the equipment. Meal-type fit
is per slot and checked with :meth:`Candidate.fits`. Each rejection keeps its
reasons so an infeasible plan can say what blocked it.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from enum import StrEnum

from app.nutrition.allergens import Exclusion, Verdict
from app.planner.inputs import BASIC_TOOLS, Candidate, Profile
from app.recipes.safety import check


class Reason(StrEnum):
    EXCLUSION = "exclusion"  # an allergy or strict intolerance
    UNCHECKED = "unchecked"  # no ingredient data, so no exclusion check possible
    TIME = "time"
    EQUIPMENT = "equipment"


@dataclass(frozen=True, slots=True)
class Penalty:
    """A soft exclusion the recipe touches: dislike, prefer-not or relaxed intolerance."""

    exclusion: Exclusion
    keys: tuple[str, ...]  # the ingredient lines it hits


@dataclass(frozen=True, slots=True)
class Screened:
    candidate: Candidate
    reasons: frozenset[Reason]
    blocked_by: tuple[Exclusion, ...]  # the hard exclusions behind Reason.EXCLUSION
    missing_equipment: frozenset[str]
    leave_out: tuple[str, ...]  # excluded optional ingredients: plan without them
    penalties: tuple[Penalty, ...]

    @property
    def allowed(self) -> bool:
        return not self.reasons


def missing_equipment(candidate: Candidate, available: frozenset[str]) -> frozenset[str]:
    return candidate.equipment - BASIC_TOOLS - available


def screen(candidate: Candidate, profile: Profile) -> Screened:
    reasons: set[Reason] = set()
    hard = profile.hard_exclusions
    blocked_by: tuple[Exclusion, ...] = ()
    leave_out: tuple[str, ...] = ()
    lines = candidate.allergen_lines
    if not lines:
        if hard:
            reasons.add(Reason.UNCHECKED)
    else:
        blocked_by = tuple(e for e in hard if check(lines, [e]).blocked)
        if blocked_by:
            reasons.add(Reason.EXCLUSION)
        leave_out = tuple(check(lines, hard).must_remove)
    if profile.max_minutes is not None and candidate.total_minutes > profile.max_minutes:
        reasons.add(Reason.TIME)
    missing = missing_equipment(candidate, profile.equipment)
    if missing:
        reasons.add(Reason.EQUIPMENT)
    penalties = []
    for exclusion in profile.exclusions:
        if exclusion in hard:
            continue
        conflicts = check(lines, [exclusion]).conflicts
        hits = [c.key for c in conflicts if c.verdict is Verdict.PENALISED]
        if hits:
            penalties.append(Penalty(exclusion, tuple(hits)))
    return Screened(
        candidate,
        frozenset(reasons),
        blocked_by,
        missing,
        leave_out,
        tuple(penalties),
    )


def screen_all(candidates: Sequence[Candidate], profile: Profile) -> list[Screened]:
    return [screen(c, profile) for c in candidates]
