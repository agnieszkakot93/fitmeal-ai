"""Filter, score and solve once, for one profile and set of rules."""

from __future__ import annotations

from collections.abc import Sequence

from app.planner.filter import Screened, screen_all
from app.planner.inputs import Candidate, Profile
from app.planner.score import score
from app.planner.solve import Option, Outcome, Rule, SolverConfig, solve

# The first solve uses only the best options per slot: a smaller model finds
# better plans within the time limit. A miss falls back to every option.
TOP_K = 10


def build_options(
    screened: Sequence[Screened], profile: Profile, limit: int | None = None
) -> list[list[Option]]:
    """Allowed candidates per slot, best score first (ties by id, for determinism)."""
    result = []
    for slot in profile.meals:
        opts = [
            Option(s, score(s, slot, profile))
            for s in screened
            if s.allowed and s.candidate.fits(slot.meal_type)
        ]
        opts.sort(key=lambda o: (-o.score.total, o.screened.candidate.id))
        result.append(opts[:limit])
    return result


def attempt(
    candidates: Sequence[Candidate],
    profile: Profile,
    config: SolverConfig,
    relax: frozenset[Rule] = frozenset(),
    first_solution: bool = False,
    limit: int | None = None,
) -> Outcome:
    options = build_options(screen_all(candidates, profile), profile, limit)
    return solve(options, profile, config, relax, first_solution)
