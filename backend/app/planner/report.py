"""Step 4: when no plan exists, say what blocked it, in plain words (PRD §8.5).

The diagnosis first looks for meal slots with no allowed recipe and names
the filters that emptied them. If every slot has options, it re-solves with
one daily target switched off at a time to find which one can't be met.
Suggestions are tested, not guessed: each is a changed profile that was
re-solved and found to give a plan. Allergies are never offered for
relaxing; an intolerance only as "avoid when possible", as PRD §7 allows.
"""

from __future__ import annotations

import dataclasses
from collections.abc import Sequence

from app.nutrition.allergens import Exclusion, Severity
from app.planner.filter import Reason, Screened, screen_all
from app.planner.inputs import PLAN_LENGTHS, Candidate, MealSlot, MealType, Profile
from app.planner.pipeline import attempt, build_options
from app.planner.result import Action, Blocker, BlockerKind, Infeasible, Suggestion
from app.planner.solve import PORTIONS, QUARTER, Option, Rule, SolverConfig, Status

# The onboarding choices for max cooking time (PRD §7); None is "60+".
MINUTE_STEPS: tuple[int | None, ...] = (15, 30, 45, 60, None)

_PLURAL = {
    MealType.BREAKFAST: "breakfasts",
    MealType.LUNCH: "lunches",
    MealType.DINNER: "dinners",
    MealType.SNACK: "snacks",
}
# Diagnosis re-solves only need to know whether a plan exists. Repeats are
# allowed there: they are a soft goal, relaxed with a notice.
_ANY = frozenset({Rule.VARIETY})


def _join(parts: Sequence[str]) -> str:
    if len(parts) <= 1:
        return "".join(parts)
    return ", ".join(parts[:-1]) + " and " + parts[-1]


def _category(e: Exclusion) -> str:
    return e.term if e.term else e.category.value.replace("_", " ")


def _filter_phrase(fitting: Sequence[Screened], profile: Profile) -> str:
    reasons = set().union(*(s.reasons for s in fitting))
    parts = []
    if reasons & {Reason.EXCLUSION, Reason.UNCHECKED}:
        blocking = {e for s in fitting for e in s.blocked_by}
        names = sorted({_category(e) for e in blocking})
        parts.append(f"your exclusions ({', '.join(names)})" if names else "your exclusions")
    if Reason.TIME in reasons:
        parts.append(f"the {profile.max_minutes}-minute limit")
    if Reason.EQUIPMENT in reasons:
        missing = sorted(set().union(*(s.missing_equipment for s in fitting)))
        parts.append(f"your equipment (no {', '.join(missing)})")
    return _join(parts)


def _slot_blockers(screened: Sequence[Screened], profile: Profile) -> list[Blocker]:
    blockers = []
    for slot in profile.meals:
        fitting = [s for s in screened if s.candidate.fits(slot.meal_type)]
        if any(s.allowed for s in fitting):
            continue
        plural = _PLURAL[slot.meal_type]
        if not fitting:
            blockers.append(
                Blocker(BlockerKind.NO_RECIPES, f"There are no {plural} to choose from.", slot.name)
            )
        else:
            phrase = _filter_phrase(fitting, profile)
            blockers.append(
                Blocker(BlockerKind.FILTERED, f"No {plural} match {phrase}.", slot.name)
            )
    return blockers


def _kcal_range(options: Sequence[Sequence[Option]]) -> tuple[float, float]:
    """Smallest and largest day the allowed recipes can add up to, ignoring all else."""
    lo = sum(min(o.screened.candidate.per_serving.kcal for o in opts) for opts in options)
    hi = sum(max(o.screened.candidate.per_serving.kcal for o in opts) for opts in options)
    return lo * min(PORTIONS) / QUARTER, hi * max(PORTIONS) / QUARTER


def _weakest_protein_slot(options: Sequence[Sequence[Option]], profile: Profile) -> MealSlot | None:
    """The slot whose best recipe has the lowest protein per kcal, if below the day's need."""
    needed = profile.protein_min_g / profile.daily_kcal

    def best(opts: Sequence[Option]) -> float:
        per_serving = [o.screened.candidate.per_serving for o in opts]
        return max((n.protein_g / n.kcal for n in per_serving if n.kcal > 0), default=0.0)

    density, index = min((best(opts), i) for i, opts in enumerate(options))
    return profile.meals[index] if density < needed else None


def _target_blocker(
    candidates: Sequence[Candidate],
    profile: Profile,
    config: SolverConfig,
    options: Sequence[Sequence[Option]],
) -> Blocker:
    lo, hi = profile.kcal_window
    window = f"{lo:.0f}-{hi:.0f} kcal"
    protein = f"{profile.protein_min_g:.0f} g protein"
    without_protein = attempt(candidates, profile, config, _ANY | {Rule.PROTEIN}, True)
    if without_protein.status is Status.SOLVED:
        message = f"The recipes that fit your settings can't reach {protein} a day within {window}."
        weak = _weakest_protein_slot(options, profile)
        if weak is not None:
            message += f" The {_PLURAL[weak.meal_type]} that fit are low in protein."
        return Blocker(BlockerKind.PROTEIN, message)
    day_lo, day_hi = _kcal_range(options)
    if day_hi < lo:
        detail = f" Even the largest portions add up to only about {day_hi:.0f} kcal a day."
    elif day_lo > hi:
        detail = f" Even the smallest portions add up to about {day_lo:.0f} kcal a day."
    else:
        detail = ""
    without_kcal = attempt(candidates, profile, config, _ANY | {Rule.KCAL}, True)
    if without_kcal.status is Status.SOLVED:
        with_protein = f" with at least {protein}" if profile.protein_min_g > 0 else ""
        return Blocker(
            BlockerKind.KCAL,
            f"The recipes that fit your settings can't add up to {window} a day"
            f"{with_protein}.{detail}",
        )
    return Blocker(
        BlockerKind.KCAL_AND_PROTEIN,
        f"The recipes that fit your settings can't reach {window} and {protein} a day.{detail}",
    )


def _works(candidates: Sequence[Candidate], profile: Profile, config: SolverConfig) -> bool:
    return attempt(candidates, profile, config, _ANY, True).status is Status.SOLVED


def _suggestions(
    candidates: Sequence[Candidate],
    profile: Profile,
    config: SolverConfig,
    screened: Sequence[Screened],
    blockers: Sequence[Blocker],
) -> list[Suggestion]:
    found = []
    if profile.max_minutes is not None:
        for step in MINUTE_STEPS:
            if step is not None and step <= profile.max_minutes:
                continue
            if _works(candidates, dataclasses.replace(profile, max_minutes=step), config):
                message = (
                    f"Raise your max cooking time to {step} minutes"
                    if step is not None
                    else "Remove the cooking time limit"
                )
                found.append(Suggestion(Action.MAX_MINUTES, message, step))
                break
    for appliance in sorted(set().union(*(s.missing_equipment for s in screened))):
        changed = dataclasses.replace(profile, equipment=profile.equipment | {appliance})
        if _works(candidates, changed, config):
            message = f"If you have a {appliance.replace('_', ' ')}, add it to your equipment"
            found.append(Suggestion(Action.ADD_EQUIPMENT, message, appliance))
    for i, e in enumerate(profile.exclusions):
        if e.severity is not Severity.INTOLERANCE or e.relaxed:
            continue  # allergies are never relaxed
        exclusions = list(profile.exclusions)
        exclusions[i] = dataclasses.replace(e, relaxed=True)
        if _works(candidates, dataclasses.replace(profile, exclusions=tuple(exclusions)), config):
            message = f'Change your {_category(e)} intolerance to "avoid when possible"'
            found.append(Suggestion(Action.RELAX_INTOLERANCE, message, e.category.value))
    for days in PLAN_LENGTHS:
        if days < profile.days and _works(
            candidates, dataclasses.replace(profile, days=days), config
        ):
            found.append(Suggestion(Action.SHORTEN_PLAN, f"Shorten the plan to {days} days", days))
            break
    kinds = {b.kind for b in blockers}
    if kinds & {BlockerKind.PROTEIN, BlockerKind.KCAL_AND_PROTEIN}:
        found.append(Suggestion(Action.LOWER_PROTEIN, "Lower your daily protein minimum"))
    if kinds & {BlockerKind.KCAL, BlockerKind.KCAL_AND_PROTEIN}:
        found.append(Suggestion(Action.CHANGE_KCAL, "Adjust your daily calorie target"))
    slot_types = [m.meal_type for m in profile.meals if m.name in {b.meal for b in blockers}]
    for meal_type in dict.fromkeys(slot_types):
        found.append(
            Suggestion(Action.ADD_RECIPES, f"Add or import more {_PLURAL[meal_type]}", meal_type)
        )
    if not slot_types:
        found.append(Suggestion(Action.ADD_RECIPES, "Add or import more recipes"))
    return found


def diagnose(
    candidates: Sequence[Candidate],
    profile: Profile,
    config: SolverConfig,
    status: Status,
) -> Infeasible:
    screened = screen_all(candidates, profile)
    if status is Status.TIMEOUT:
        suggestions = [Suggestion(Action.RETRY, "Try again")]
        if profile.days > min(PLAN_LENGTHS):
            suggestions.append(
                Suggestion(Action.SHORTEN_PLAN, "Shorten the plan", min(PLAN_LENGTHS))
            )
        blocker = Blocker(BlockerKind.TIMEOUT, "Donut couldn't finish building this plan in time.")
        return Infeasible(status, (blocker,), tuple(suggestions))
    blockers = _slot_blockers(screened, profile)
    if not blockers:
        options = build_options(screened, profile)
        blockers = [_target_blocker(candidates, profile, config, options)]
    suggestions = _suggestions(candidates, profile, config, screened, blockers)
    return Infeasible(status, tuple(blockers), tuple(suggestions))
