"""Step 3: assign a recipe and a portion to every meal slot with CP-SAT.

One boolean ``y[d, s, c, k]`` per day, slot, allowed candidate and portion
level (``k`` quarters of a serving, 0.5-2.0). Hard constraints:

* every slot gets exactly one recipe and portion; a recipe at most once a day;
* daily kcal within the window, daily protein at or above the minimum, and
  each meal between 0.5 and 1.6 times its share of the daily kcal;
* meal prep: a recipe repeated in the same slot on consecutive days may be
  one cooked batch (``cont``, otherwise it is cooked fresh again); a batch
  spans at most ``max_run`` days (never more than the recipe's fridge days or
  the user's "cook once for N days") and is eaten in equal portions;
* variety: each recipe is cooked at most ``max_cooks`` times.

Nutrition is scaled to integers (tenths per serving, times quarters), rounded
in the safe direction for each bound so a solution also holds in floats.
Everything soft (meal sizes against the calorie split, portion sizes, repeats,
unique ingredients, meal-prep fit, preferences) is in the objective.
"""

from __future__ import annotations

import math
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from enum import StrEnum

from ortools.sat.python import cp_model

from app.nutrition.nutrients import Nutrients
from app.planner.filter import Screened
from app.planner.inputs import Profile
from app.planner.score import Score

PORTIONS = (2, 3, 4, 5, 6, 7, 8)  # quarters of a serving: 0.5x to 2.0x
QUARTER = 4
SCALE = 10  # nutrition in tenths
EPS = 1e-6  # float noise: 12.7 * 10 is 126.99999999999999
# A batch only makes sense for recipes that store and reheat reasonably.
MIN_PREP_SCORE = 50
MAX_COOKS = 2
# A meal stays between half and 1.6 times its share of the day's calories.
MEAL_SIZE = (0.5, 1.6)

SHARE_WEIGHT = 300  # points lost at 100% off the slot's calorie share
PORTION_STEP_PENALTY = 10  # per quarter away from one serving
REPEAT_PENALTY = 150  # per cook of a recipe after its first
BATCH_BONUS = 60  # per meal eaten from a batch instead of cooked fresh
UNIQUE_PENALTY = 15  # per distinct ingredient across the plan


class Rule(StrEnum):
    """Constraints that the infeasibility diagnosis may switch off one at a time."""

    KCAL = "kcal"  # the daily window and the meal size bounds
    PROTEIN = "protein"
    VARIETY = "variety"


class Status(StrEnum):
    SOLVED = "solved"
    INFEASIBLE = "infeasible"
    TIMEOUT = "timeout"  # no solution found within the limit, none proven impossible


@dataclass(frozen=True, slots=True)
class SolverConfig:
    """Search limits. Deterministic time makes results repeatable; wall time is a backstop."""

    deterministic_time: float = 1.0
    time_limit_s: float = 10.0
    workers: int = 1
    seed: int = 0


DEFAULT_CONFIG = SolverConfig()


@dataclass(frozen=True, slots=True)
class Option:
    """An allowed candidate for one slot, with its score there."""

    screened: Screened
    score: Score


@dataclass(frozen=True, slots=True)
class Pick:
    day: int
    slot: int
    option: Option
    quarters: int
    continues_batch: bool  # same recipe in this slot the day before


@dataclass(frozen=True, slots=True)
class Outcome:
    status: Status
    picks: tuple[Pick, ...] = ()


def max_run(screened: Screened, profile: Profile) -> int:
    """Most consecutive days one batch of this recipe may cover."""
    c = screened.candidate
    if profile.prep_days == 1 or c.meal_prep_score < MIN_PREP_SCORE:
        return 1
    return min(profile.prep_days, max(1, c.fridge_days))


def _total(terms: Iterable[cp_model.LinearExprT]) -> cp_model.LinearExpr:
    return cp_model.LinearExpr.sum(list(terms))


def _levels(kcal: float, target: float, any_size: bool) -> list[int]:
    """Portion levels that keep a meal within its size bounds (all of them if ``any_size``)."""
    if any_size:
        return list(PORTIONS)
    return [
        k for k in PORTIONS if MEAL_SIZE[0] * target <= kcal * k / QUARTER <= MEAL_SIZE[1] * target
    ]


def _row(
    y: dict[tuple[int, int, int, int], cp_model.IntVar], d: int, s: int, c: int
) -> list[cp_model.IntVar]:
    return [y[d, s, c, k] for k in PORTIONS if (d, s, c, k) in y]


def _down(value: float) -> int:
    """Tenths, rounded down: a lower bound on these units holds for the true value."""
    return math.floor(value * SCALE + EPS)


def _up(value: float) -> int:
    return math.ceil(value * SCALE - EPS)


def solve(
    options: Sequence[Sequence[Option]],
    profile: Profile,
    config: SolverConfig = DEFAULT_CONFIG,
    relax: frozenset[Rule] = frozenset(),
    first_solution: bool = False,
) -> Outcome:
    """``options[s]`` are the allowed candidates for ``profile.meals[s]``.

    ``first_solution`` stops at any feasible plan: enough to test feasibility.
    """
    days = range(profile.days)
    slots = range(len(profile.meals))
    if any(not options[s] for s in slots):
        return Outcome(Status.INFEASIBLE)

    m = cp_model.CpModel()
    y: dict[tuple[int, int, int, int], cp_model.IntVar] = {}
    x: dict[tuple[int, int, int], cp_model.IntVar] = {}
    objective: list[cp_model.LinearExprT] = []
    for s in slots:
        target = profile.daily_kcal * profile.meals[s].kcal_share
        for c, opt in enumerate(options[s]):
            kcal = opt.screened.candidate.per_serving.kcal
            for k in _levels(kcal, target, Rule.KCAL in relax):
                share_off = abs(kcal * k / QUARTER - target) / target
                points = (
                    opt.score.total
                    - round(SHARE_WEIGHT * share_off)
                    - PORTION_STEP_PENALTY * abs(k - QUARTER)
                )
                for d in days:
                    var = m.new_bool_var(f"y_{d}_{s}_{c}_{k}")
                    y[d, s, c, k] = var
                    objective.append(points * var)
            for d in days:
                x[d, s, c] = m.new_bool_var(f"x_{d}_{s}_{c}")
                m.add(x[d, s, c] == _total(_row(y, d, s, c)))

    for d in days:
        for s in slots:
            m.add_exactly_one(v for c in range(len(options[s])) for v in _row(y, d, s, c))

    # The same recipe may be offered in several slots; group by id.
    by_recipe: dict[str, list[tuple[int, int]]] = {}
    for s in slots:
        for c, opt in enumerate(options[s]):
            by_recipe.setdefault(opt.screened.candidate.id, []).append((s, c))
    for places in by_recipe.values():
        if len(places) > 1:
            for d in days:
                m.add(_total(x[d, s, c] for s, c in places) <= 1)

    # Meal prep: runs of the same recipe in a slot, bounded and evenly portioned.
    cont: dict[tuple[int, int, int], cp_model.IntVar] = {}
    for s in slots:
        for c, opt in enumerate(options[s]):
            run = max_run(opt.screened, profile)
            if run == 1:
                continue
            for d in days[1:]:
                b = m.new_bool_var(f"cont_{d}_{s}_{c}")
                cont[d, s, c] = b
                m.add(b <= x[d, s, c])
                m.add(b <= x[d - 1, s, c])
                for k in PORTIONS:
                    if (d, s, c, k) in y:
                        m.add(y[d, s, c, k] == y[d - 1, s, c, k]).only_enforce_if(b)
                objective.append(BATCH_BONUS * b)
            # A batch of `run` days has run-1 continuations in a row, never `run`.
            for start in range(1, profile.days - run + 1):
                m.add(_total(cont[d, s, c] for d in range(start, start + run)) <= run - 1)

    # Variety: cooks per recipe = appearances minus batch continuations.
    for rid, places in by_recipe.items():
        cooks = _total(x[d, s, c] for s, c in places for d in days) - _total(
            cont[d, s, c] for s, c in places for d in days if (d, s, c) in cont
        )
        if Rule.VARIETY not in relax:
            m.add(cooks <= MAX_COOKS)
        extra = m.new_int_var(0, profile.days * len(profile.meals), f"extra_{rid}")
        m.add(extra >= cooks - 1)
        objective.append(-REPEAT_PENALTY * extra)

    # Daily totals, in units of 1/(SCALE*QUARTER) kcal or g. Lower bounds use
    # values rounded down and upper bounds values rounded up, so a solution
    # also holds for the unrounded nutrition.
    unit = SCALE * QUARTER
    lo, hi = profile.kcal_window

    def day_sum(d: int, value: Callable[[Nutrients], int]) -> cp_model.LinearExpr:
        return _total(
            value(options[s][c].screened.candidate.per_serving) * k * var
            for (day, s, c, k), var in y.items()
            if day == d
        )

    for d in days:
        if Rule.KCAL not in relax:
            m.add(day_sum(d, lambda n: _down(n.kcal)) >= math.ceil(lo * unit - EPS))
            m.add(day_sum(d, lambda n: _up(n.kcal)) <= math.floor(hi * unit + EPS))
        if Rule.PROTEIN not in relax:
            protein = day_sum(d, lambda n: _down(n.protein_g))
            m.add(protein >= math.ceil(profile.protein_min_g * unit - EPS))

    # Ingredient reuse: fewer distinct ingredients across the plan.
    ingredient_recipes: dict[str, list[str]] = {}
    for s in slots:
        for opt in options[s]:
            for ing in opt.screened.candidate.ingredient_ids:
                ingredient_recipes.setdefault(ing, []).append(opt.screened.candidate.id)
    if ingredient_recipes:
        used = {}
        for rid, places in by_recipe.items():
            u = m.new_bool_var(f"used_{rid}")
            for s, c in places:
                for d in days:
                    m.add(u >= x[d, s, c])
            used[rid] = u
        for ing, rids in ingredient_recipes.items():
            v = m.new_bool_var(f"ing_{ing}")
            for rid in set(rids):
                m.add(v >= used[rid])
            objective.append(-UNIQUE_PENALTY * v)

    m.maximize(_total(objective))

    solver = cp_model.CpSolver()
    solver.parameters.num_workers = config.workers
    solver.parameters.random_seed = config.seed
    solver.parameters.max_time_in_seconds = config.time_limit_s
    solver.parameters.max_deterministic_time = config.deterministic_time
    solver.parameters.stop_after_first_solution = first_solution
    status = solver.solve(m)
    if status == cp_model.INFEASIBLE:
        return Outcome(Status.INFEASIBLE)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        if status == cp_model.MODEL_INVALID:
            raise RuntimeError(f"invalid planner model: {m.validate()}")
        return Outcome(Status.TIMEOUT)

    picks = []
    for d in days:
        for s in slots:
            for c, opt in enumerate(options[s]):
                for k in PORTIONS:
                    if (d, s, c, k) in y and solver.boolean_value(y[d, s, c, k]):
                        link = cont.get((d, s, c))
                        batch = link is not None and bool(solver.boolean_value(link))
                        picks.append(Pick(d, s, opt, k, batch))
    return Outcome(Status.SOLVED, tuple(picks))
