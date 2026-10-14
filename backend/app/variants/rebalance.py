"""Daily rebalancing after a swap (PRD §8.6, Development Plan §2.3).

A small LP over portion multipliers of the day's other meals: each moves by at
most ±20%, meals already eaten or skipped (or ones the client marks as past)
stay as they are, and the day aims for its kcal window (±5%, never below the
1200 kcal floor) with protein at or above the minimum. When ±20% can't get
there, the proposal says how far off the day stays. It is only a proposal:
nothing changes until the user applies it.

Pure functions only.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
from scipy.optimize import linprog

from app.nutrition.nutrients import Nutrients
from app.planner.inputs import KCAL_FLOOR, KCAL_TOLERANCE

MAX_CHANGE = 0.20
# aim inside the window so rounding portions to PORTION_STEP keeps the day in it
AIM = 0.04
PORTION_STEP = 0.01
# smaller changes than this aren't worth proposing
MIN_CHANGE = 0.01

_W_HARD = 1000.0  # per 100% of a target missed; only when ±20% can't reach it


@dataclass(frozen=True, slots=True)
class Meal:
    position: int
    portion: float
    nutrition: Nutrients  # at ``portion``
    adjustable: bool


@dataclass(frozen=True, slots=True)
class Adjustment:
    position: int
    portion_from: float
    portion_to: float
    delta: Nutrients


@dataclass(frozen=True, slots=True)
class Proposal:
    before: Nutrients
    after: Nutrients
    adjustments: list[Adjustment]
    within_tolerance: bool  # after the adjustments
    # kcal above the window (positive) or below it (negative) after the adjustments
    kcal_off: float
    protein_short_g: float

    @property
    def needed(self) -> bool:
        return bool(self.adjustments)


def window(daily_kcal: float) -> tuple[float, float]:
    """The day's allowed kcal: ±5% of the target, never below the floor (PRD §8.5)."""
    return max(KCAL_FLOOR, daily_kcal * (1 - KCAL_TOLERANCE)), daily_kcal * (1 + KCAL_TOLERANCE)


def _status(n: Nutrients, daily_kcal: float, protein_min_g: float) -> tuple[float, float]:
    lo, hi = window(daily_kcal)
    off = n.kcal - hi if n.kcal > hi else (n.kcal - lo if n.kcal < lo else 0.0)
    return off, max(0.0, protein_min_g - n.protein_g)


def _within(n: Nutrients, daily_kcal: float, protein_min_g: float) -> bool:
    off, short = _status(n, daily_kcal, protein_min_g)
    return abs(off) < 1e-6 and short < 1e-6


def propose(meals: Sequence[Meal], daily_kcal: float, protein_min_g: float) -> Proposal:
    """Portion changes to the adjustable meals that bring the day back within its targets."""
    before = Nutrients.total([m.nutrition for m in meals])
    movable = [m for m in meals if m.adjustable and m.portion > 0 and m.nutrition.kcal > 0]
    if _within(before, daily_kcal, protein_min_g) or not movable:
        off, short = _status(before, daily_kcal, protein_min_g)
        return Proposal(before, before, [], _within(before, daily_kcal, protein_min_g), off, short)

    factors = _solve(meals, movable, daily_kcal, protein_min_g)
    adjustments = []
    for meal, factor in zip(movable, factors, strict=True):
        portion = round(meal.portion * factor / PORTION_STEP) * PORTION_STEP
        portion = round(portion, 2)
        if abs(portion / meal.portion - 1) < MIN_CHANGE:
            continue
        scaled = meal.nutrition.scale(portion / meal.portion)
        adjustments.append(
            Adjustment(meal.position, meal.portion, portion, scaled + meal.nutrition.scale(-1))
        )
    after = before + Nutrients.total([a.delta for a in adjustments])
    off, short = _status(after, daily_kcal, protein_min_g)
    return Proposal(
        before, after, adjustments, _within(after, daily_kcal, protein_min_g), off, short
    )


def _solve(
    meals: Sequence[Meal], movable: Sequence[Meal], daily_kcal: float, protein_min_g: float
) -> list[float]:
    """LP over m (multipliers), d+/d- (|m - 1|) and kcal-low, kcal-high and protein slacks."""
    n = len(movable)
    fixed = Nutrients.total([m.nutrition for m in meals if m not in movable])
    kcal = np.array([m.nutrition.kcal for m in movable])
    protein = np.array([m.nutrition.protein_g for m in movable])
    portions = np.array([m.portion for m in movable])
    lo, hi = window(daily_kcal)
    # the most rounding portions to PORTION_STEP can move each total
    kcal_err = float((PORTION_STEP / 2 * kcal / portions).sum())
    protein_err = float((PORTION_STEP / 2 * protein / portions).sum())
    # aim inside the window, never under the floor
    aim_lo = max(lo + kcal_err, daily_kcal * (1 - AIM))
    aim_hi = max(aim_lo, min(hi - kcal_err, daily_kcal * (1 + AIM)))
    protein_aim = protein_min_g + protein_err

    width = 3 * n + 3
    s_lo, s_hi, s_p = 3 * n, 3 * n + 1, 3 * n + 2
    c = np.zeros(width)
    # a bigger meal moving costs more: prefer moving the meals with the kcal to spare
    c[n : 3 * n] = np.tile(kcal / kcal.sum(), 2)
    c[s_lo] = c[s_hi] = _W_HARD / daily_kcal
    c[s_p] = _W_HARD / max(protein_min_g, 1.0)

    a_ub = np.zeros((3, width))
    b_ub = np.zeros(3)
    # fixed + kcal·m + s_lo >= aim_lo
    a_ub[0, :n], a_ub[0, s_lo] = -kcal, -1
    b_ub[0] = fixed.kcal - aim_lo
    # fixed + kcal·m - s_hi <= aim_hi
    a_ub[1, :n], a_ub[1, s_hi] = kcal, -1
    b_ub[1] = aim_hi - fixed.kcal
    # fixed + protein·m + s_p >= protein_aim
    a_ub[2, :n], a_ub[2, s_p] = -protein, -1
    b_ub[2] = fixed.protein_g - protein_aim

    # m - d+ + d- = 1
    a_eq = np.zeros((n, width))
    for i in range(n):
        a_eq[i, i], a_eq[i, n + i], a_eq[i, 2 * n + i] = 1, -1, 1
    b_eq = np.ones(n)

    bounds = [(1 - MAX_CHANGE, 1 + MAX_CHANGE)] * n + [(0, None)] * (2 * n + 3)
    res = linprog(c, A_ub=a_ub, b_ub=b_ub, A_eq=a_eq, b_eq=b_eq, bounds=bounds, method="highs")
    if res.status != 0 or res.x is None:  # the slacks make it always feasible
        return [1.0] * n
    return [float(x) for x in res.x[:n]]
