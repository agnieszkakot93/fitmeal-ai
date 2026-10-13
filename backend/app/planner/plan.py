"""Planner v1: filter, score, assign (PRD §8.5, §8.7; Development Plan §2.3).

:func:`plan` returns a :class:`Plan` or, when no plan satisfies the hard
constraints, an :class:`Infeasible` report saying what blocked it. Hard
constraints are never dropped. The one soft goal that is also a solver
constraint, the variety limit, is relaxed only as a second attempt, and the
plan then carries a notice saying so.

Pure functions only: no database, no I/O.
"""

from __future__ import annotations

from collections.abc import Sequence

from app.nutrition.allergens import Severity
from app.planner.filter import Penalty, screen_all
from app.planner.inputs import Candidate, Profile
from app.planner.pipeline import TOP_K, attempt
from app.planner.report import diagnose
from app.planner.result import DayPlan, Infeasible, Plan, PlannedMeal
from app.planner.solve import (
    DEFAULT_CONFIG,
    MAX_COOKS,
    PORTIONS,
    QUARTER,
    Outcome,
    Rule,
    SolverConfig,
    Status,
    max_run,
)


def _label(penalty: Penalty) -> str:
    e = penalty.exclusion
    what = e.term if e.term else e.category.value
    if e.severity is Severity.INTOLERANCE:
        return f"contains {what} (intolerance, avoid when possible)"
    if e.severity is Severity.DISLIKE:
        return f"contains {what} (you don't like it)"
    return f"contains {what} (you prefer not to eat it)"


def _to_plan(outcome: Outcome, profile: Profile, relaxed: frozenset[Rule]) -> Plan:
    by_day: dict[int, list[PlannedMeal]] = {}
    last_cook: dict[int, int] = {}
    for pick in sorted(outcome.picks, key=lambda p: (p.day, p.slot)):
        c = pick.option.screened.candidate
        cook_day = last_cook[pick.slot] if pick.continues_batch else pick.day
        last_cook[pick.slot] = cook_day
        batch = max_run(pick.option.screened, profile) > 1
        portion = pick.quarters / QUARTER
        by_day.setdefault(pick.day, []).append(
            PlannedMeal(
                day=pick.day,
                slot=profile.meals[pick.slot].name,
                recipe_id=c.id,
                portion=portion,
                nutrition=c.per_serving.scale(portion),
                cook_day=cook_day,
                eat_by_day=cook_day + max(1, c.fridge_days) - 1 if batch else cook_day,
                from_batch=pick.continues_batch,
                leave_out=pick.option.screened.leave_out,
                labels=tuple(_label(p) for p in pick.option.screened.penalties),
            )
        )
    days = tuple(DayPlan(d, tuple(by_day[d])) for d in range(profile.days))
    notices = []
    if Rule.VARIETY in relaxed:
        cooks: dict[str, int] = {}
        for m in (m for d in days for m in d.meals):
            if not m.from_batch:
                cooks[m.recipe_id] = cooks.get(m.recipe_id, 0) + 1
        over = sorted(r for r, n in cooks.items() if n > MAX_COOKS)
        notices.append(
            "Not enough different recipes fit your settings to avoid repeats: "
            f"{', '.join(over)} {'is' if len(over) == 1 else 'are'} cooked more than "
            f"{MAX_COOKS} times. Add or import recipes, loosen a setting, or shorten the "
            "plan for more variety."
        )
    return Plan(days, tuple(notices), relaxed)


def plan(
    candidates: Sequence[Candidate],
    profile: Profile,
    config: SolverConfig = DEFAULT_CONFIG,
) -> Plan | Infeasible:
    ids = [c.id for c in candidates]
    if len(set(ids)) != len(ids):
        raise ValueError("candidate ids must be unique")
    outcome = attempt(candidates, profile, config, limit=TOP_K)
    if outcome.status is not Status.SOLVED:
        outcome = attempt(candidates, profile, config)
    relaxed: frozenset[Rule] = frozenset()
    if outcome.status is Status.INFEASIBLE:
        relaxed = frozenset({Rule.VARIETY})
        outcome = attempt(candidates, profile, config, relaxed)
    if outcome.status is not Status.SOLVED:
        return diagnose(candidates, profile, config, outcome.status)
    result = _to_plan(outcome, profile, relaxed)
    problems = verify(result, candidates, profile)
    if problems:  # a bug in the model, never something to show the user
        raise AssertionError("planner produced an invalid plan: " + "; ".join(problems))
    return result


# float noise only: the solver's integer bounds are exact on a 0.1 grid
TOLERANCE = 1e-6


def verify(result: Plan, candidates: Sequence[Candidate], profile: Profile) -> list[str]:
    """Every hard constraint, rechecked in floats on the finished plan."""
    problems = []
    by_id = {s.candidate.id: s for s in screen_all(candidates, profile)}
    lo, hi = profile.kcal_window
    slots = {m.name: m for m in profile.meals}
    if len(result.days) != profile.days:
        problems.append(f"{len(result.days)} days, expected {profile.days}")
    for day in result.days:
        names = [m.slot for m in day.meals]
        if sorted(names) != sorted(slots):
            problems.append(f"day {day.day}: slots {names}")
        recipes = [m.recipe_id for m in day.meals]
        if len(set(recipes)) != len(recipes):
            problems.append(f"day {day.day}: a recipe twice in one day")
        totals = day.totals
        if not lo - TOLERANCE <= totals.kcal <= hi + TOLERANCE:
            problems.append(f"day {day.day}: {totals.kcal:.1f} kcal outside {lo:.0f}-{hi:.0f}")
        if totals.protein_g < profile.protein_min_g - TOLERANCE:
            problems.append(f"day {day.day}: {totals.protein_g:.1f} g protein")
        for meal in day.meals:
            s = by_id.get(meal.recipe_id)
            if s is None or not s.allowed:
                problems.append(f"day {day.day}: {meal.recipe_id} is not allowed")
                continue
            if not s.candidate.fits(slots[meal.slot].meal_type):
                problems.append(f"day {day.day}: {meal.recipe_id} doesn't fit {meal.slot}")
            if round(meal.portion * QUARTER) not in PORTIONS:
                problems.append(f"day {day.day}: portion {meal.portion}")
            span = meal.day - meal.cook_day + 1
            if meal.from_batch and span > max_run(s, profile):
                problems.append(f"day {day.day}: {meal.recipe_id} batch spans {span} days")
            if meal.eat_by_day < meal.day:
                problems.append(f"day {day.day}: {meal.recipe_id} eaten after its eat-by day")
    problems += _check_batches(result)
    if Rule.VARIETY not in result.relaxed:
        cooks: dict[str, int] = {}
        for m in result.meals:
            if not m.from_batch:
                cooks[m.recipe_id] = cooks.get(m.recipe_id, 0) + 1
        problems += [f"{r} cooked {n} times" for r, n in cooks.items() if n > MAX_COOKS]
    return problems


def _check_batches(result: Plan) -> list[str]:
    """A batch meal follows the same recipe in the same slot the day before, same portion."""
    problems = []
    meals = {(m.day, m.slot): m for m in result.meals}
    for m in result.meals:
        if not m.from_batch:
            continue
        before = meals.get((m.day - 1, m.slot))
        if before is None or before.recipe_id != m.recipe_id or before.portion != m.portion:
            problems.append(f"day {m.day}: {m.recipe_id} batch doesn't follow the day before")
        elif before.cook_day != m.cook_day:
            problems.append(f"day {m.day}: {m.recipe_id} batch cook day mismatch")
    return problems
