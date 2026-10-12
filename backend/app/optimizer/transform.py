"""Recipe Transformation Engine v1 (PRD §8.3, Development Plan §2.3).

Adjusts ingredient amounts so one serving hits a meal target, as a linear
program solved with HiGHS:

* variables: grams per serving of each ingredient, bounded by its culinary
  role (oil may shrink but never grow, protein moves ±60%, vegetables may
  double, seasonings stay put);
* hard: protein ≥ minimum, kcal within ±3% of the target;
* soft (weighted): fat and carb targets, and staying close to the original.

The hard constraints carry penalised slack, so the LP always solves; slack
left over means the target can't be reached and is reported as a miss.
The solution is then rounded to practical amounts and re-verified (kcal
±5%, protein still ≥ minimum). If rounding breaks a target, a greedy repair
moves single rounding steps; the result is never called on target unless it
passes the post-rounding check.

Pure functions only: no database, no I/O. Substitutions (step 2 of §8.3) are
the Substitution Engine's job and are not done here.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import StrEnum

import numpy as np
from scipy.optimize import linprog

from app.foods.vocab import CulinaryRole
from app.nutrition.nutrients import Nutrients, for_grams

KCAL_TOLERANCE_LP = 0.03
# The LP aims inside the tolerances so rounding to practical amounts has room:
# kcal within ±2% (the spec allows ±3%) and protein a little above the minimum.
KCAL_AIM_LP = 0.02
PROTEIN_MARGIN = 0.02
PROTEIN_MARGIN_G = 0.5
# Countable ingredients round to pieces; the rest round in grams.
_PIECE_ROLES = {CulinaryRole.MAIN_PROTEIN, CulinaryRole.CARB_BASE, CulinaryRole.VEGETABLE,
                CulinaryRole.FRUIT}  # fmt: skip
_HALF_PIECE_ROLES = {CulinaryRole.CARB_BASE, CulinaryRole.VEGETABLE, CulinaryRole.FRUIT}
# Bigger pieces (a salmon fillet, a sweet potato) are bought and portioned by weight.
MAX_PIECE_G = 60
KCAL_TOLERANCE_ROUNDED = 0.05

# (min, max) multiple of the original amount, per culinary role
ROLE_BOUNDS: dict[CulinaryRole, tuple[float, float]] = {
    CulinaryRole.MAIN_PROTEIN: (0.4, 1.6),
    CulinaryRole.CARB_BASE: (0.3, 1.6),
    CulinaryRole.VEGETABLE: (0.5, 2.0),
    CulinaryRole.FRUIT: (0.5, 1.5),
    CulinaryRole.COOKING_FAT: (0.3, 1.0),
    CulinaryRole.CREAMY_BASE: (0.4, 1.5),
    CulinaryRole.CHEESE: (0.3, 1.2),
    CulinaryRole.SAUCE_BASE: (0.6, 1.4),
    CulinaryRole.TOPPING: (0.3, 1.2),
    CulinaryRole.SWEETENER: (0.3, 1.0),
    CulinaryRole.LIQUID: (0.6, 1.4),
    CulinaryRole.BINDER: (1.0, 1.0),
    CulinaryRole.AROMATIC: (1.0, 1.0),
    CulinaryRole.SEASONING: (1.0, 1.0),
    CulinaryRole.LEAVENING: (1.0, 1.0),
    CulinaryRole.ACID: (1.0, 1.0),
}

# rounding step in grams when the ingredient has no piece weight
ROLE_STEP_G: dict[CulinaryRole, float] = {
    CulinaryRole.MAIN_PROTEIN: 5,
    CulinaryRole.CARB_BASE: 5,
    CulinaryRole.VEGETABLE: 10,
    CulinaryRole.FRUIT: 10,
    CulinaryRole.CREAMY_BASE: 10,
    CulinaryRole.LIQUID: 10,
    CulinaryRole.SAUCE_BASE: 10,
    CulinaryRole.CHEESE: 5,
}
DEFAULT_STEP_G = 1.0

# objective weights
_W_DEVIATION = 0.3  # per 100% change of one ingredient
_W_VEG_INCREASE = 0.05  # vegetables are cheap to add (§8.3 step 7)
_W_FAT_DECREASE = 0.1  # cooking fat is the first thing to trim
_W_MACRO = 1.0  # per 100% miss of the fat or carb target
_W_HARD = 1000.0  # per 100% miss of a hard target; only used when infeasible


@dataclass(frozen=True, slots=True)
class Line:
    key: str
    per_100g: Nutrients
    grams: float  # per serving, original
    role: CulinaryRole
    optional: bool = False
    # weight of one piece; rounds to whole pieces (half for vegetables and fruit)
    piece_g: float | None = None
    # the user rejected changing this line: it stays at the original amount
    locked: bool = False


@dataclass(frozen=True, slots=True)
class Target:
    """Per serving."""

    kcal: float
    protein_min_g: float
    fat_g: float | None = None
    carbs_g: float | None = None


class Reason(StrEnum):
    RAISE_PROTEIN = "raise_protein"
    CUT_CALORIES = "cut_calories"
    ADD_CALORIES = "add_calories"
    LOWER_FAT = "lower_fat"
    ADJUST_CARBS = "adjust_carbs"
    MORE_VOLUME = "more_volume"
    REMOVED_OPTIONAL = "removed_optional"
    ROUNDING = "rounding"


@dataclass(frozen=True, slots=True)
class Change:
    key: str
    original_g: float
    grams: float
    reason: Reason


class Metric(StrEnum):
    KCAL = "kcal"
    PROTEIN = "protein"


@dataclass(frozen=True, slots=True)
class Miss:
    metric: Metric
    target: float
    actual: float


@dataclass(frozen=True, slots=True)
class Result:
    grams: dict[str, float]  # per serving, rounded
    nutrition: Nutrients  # per serving, after rounding
    changes: list[Change]
    on_target: bool
    misses: list[Miss] = field(default_factory=list)


def bounds(line: Line) -> tuple[float, float]:
    if line.locked:
        return line.grams, line.grams
    lo, hi = ROLE_BOUNDS[line.role]
    return (0.0 if line.optional else lo * line.grams), hi * line.grams


def nutrition(lines: list[Line], grams: dict[str, float]) -> Nutrients:
    return Nutrients.total([for_grams(line.per_100g, grams[line.key]) for line in lines])


def misses(target: Target, n: Nutrients, kcal_tolerance: float) -> list[Miss]:
    found = []
    if abs(n.kcal - target.kcal) > kcal_tolerance * target.kcal + 1e-6:
        found.append(Miss(Metric.KCAL, target.kcal, n.kcal))
    if n.protein_g < target.protein_min_g - 1e-6:
        found.append(Miss(Metric.PROTEIN, target.protein_min_g, n.protein_g))
    return found


def transform(lines: list[Line], target: Target) -> Result:
    if not lines:
        raise ValueError("a recipe needs at least one ingredient")
    if target.kcal <= 0 or target.protein_min_g < 0:
        raise ValueError("target kcal must be positive and protein non-negative")
    keys = [line.key for line in lines]
    if len(set(keys)) != len(keys):
        raise ValueError("ingredient keys must be unique")

    solved = _solve(lines, target)
    rounded = _repair(lines, target, {ln.key: _round(ln, solved[ln.key]) for ln in lines})
    n = nutrition(lines, rounded)
    found = misses(target, n, KCAL_TOLERANCE_ROUNDED)
    original = nutrition(lines, {line.key: line.grams for line in lines})
    return Result(
        grams=rounded,
        nutrition=n,
        changes=_explain(lines, rounded, original, target),
        on_target=not found,
        misses=found,
    )


def _solve(lines: list[Line], target: Target) -> dict[str, float]:
    """LP over x (grams), d+/d- (deviation) and macro and hard-target slacks."""
    n = len(lines)
    # column layout: x[n], dp[n], dn[n], then 7 slacks
    fat_p, fat_n, carb_p, carb_n, kcal_lo, kcal_hi, prot = range(3 * n, 3 * n + 7)
    size = 3 * n + 7
    c = np.zeros(size)
    for i, line in enumerate(lines):
        scale = 1.0 / max(line.grams, 1.0)
        up = _W_VEG_INCREASE if line.role is CulinaryRole.VEGETABLE else _W_DEVIATION
        c[n + i] = up * scale
        down = _W_FAT_DECREASE if line.role is CulinaryRole.COOKING_FAT else _W_DEVIATION
        c[2 * n + i] = down * scale
    if target.fat_g is not None:
        c[fat_p] = c[fat_n] = _W_MACRO / max(target.fat_g, 1.0)
    if target.carbs_g is not None:
        c[carb_p] = c[carb_n] = _W_MACRO / max(target.carbs_g, 1.0)
    c[kcal_lo] = c[kcal_hi] = _W_HARD / target.kcal
    c[prot] = _W_HARD / max(target.protein_min_g, 1.0)

    per_g = {attr: np.array([getattr(line.per_100g, attr) / 100 for line in lines])
             for attr in ("kcal", "protein_g", "fat_g", "carbs_g")}  # fmt: skip

    a_eq, b_eq = [], []
    for i, line in enumerate(lines):  # x - dp + dn = original
        row = np.zeros(size)
        row[i], row[n + i], row[2 * n + i] = 1, -1, 1
        a_eq.append(row)
        b_eq.append(line.grams)
    for attr, plus, minus, goal in (
        ("fat_g", fat_p, fat_n, target.fat_g),
        ("carbs_g", carb_p, carb_n, target.carbs_g),
    ):
        if goal is not None:  # macro - s+ + s- = goal
            row = np.zeros(size)
            row[:n] = per_g[attr]
            row[plus], row[minus] = -1, 1
            a_eq.append(row)
            b_eq.append(goal)

    a_ub, b_ub = [], []
    # kcal <= hi + slack ; -kcal <= -lo + slack ; -protein <= -min + slack
    row = np.zeros(size)
    row[:n], row[kcal_hi] = per_g["kcal"], -1
    a_ub.append(row)
    b_ub.append(target.kcal * (1 + KCAL_AIM_LP))
    row = np.zeros(size)
    row[:n], row[kcal_lo] = -per_g["kcal"], -1
    a_ub.append(row)
    b_ub.append(-target.kcal * (1 - KCAL_AIM_LP))
    row = np.zeros(size)
    row[:n], row[prot] = -per_g["protein_g"], -1
    a_ub.append(row)
    b_ub.append(-_protein_aim(target))

    var_bounds = [bounds(line) for line in lines] + [(0, None)] * (2 * n + 7)
    res = linprog(c, A_ub=a_ub, b_ub=b_ub, A_eq=a_eq, b_eq=b_eq, bounds=var_bounds,
                  method="highs")  # fmt: skip
    if res.status != 0 or res.x is None:  # cannot happen with the slacks; kept as a guard
        raise RuntimeError(f"transformation LP failed: {res.message}")
    x = res.x
    return {line.key: float(x[i]) for i, line in enumerate(lines)}


def _protein_aim(target: Target) -> float:
    if target.protein_min_g == 0:
        return 0.0
    return target.protein_min_g * (1 + PROTEIN_MARGIN) + PROTEIN_MARGIN_G


def _step(line: Line) -> float:
    if line.piece_g and line.piece_g <= MAX_PIECE_G and line.role in _PIECE_ROLES:
        return line.piece_g * (0.5 if line.role in _HALF_PIECE_ROLES else 1.0)
    return ROLE_STEP_G.get(line.role, DEFAULT_STEP_G)


def _round(line: Line, grams: float) -> float:
    if line.locked or math.isclose(grams, line.grams, rel_tol=0.02):
        return line.grams
    step = _step(line)
    lo, hi = bounds(line)
    rounded = round(grams / step) * step
    if rounded > hi + 1e-9:
        rounded = math.floor(hi / step) * step
    if rounded < lo - 1e-9:
        rounded = math.ceil(lo / step) * step
    # no whole step fits inside the bounds: keep the solver's amount
    return rounded if lo - 1e-9 <= rounded <= hi + 1e-9 else grams


def _score(lines: list[Line], target: Target, grams: dict[str, float]) -> float:
    n = nutrition(lines, grams)
    kcal_gap = max(0.0, abs(n.kcal - target.kcal) - KCAL_TOLERANCE_ROUNDED * target.kcal)
    protein_gap = max(0.0, target.protein_min_g - n.protein_g)
    return kcal_gap / target.kcal + protein_gap / max(target.protein_min_g, 1.0)


def _repair(lines: list[Line], target: Target, grams: dict[str, float]) -> dict[str, float]:
    """Greedy: while rounding broke a hard target, apply the single step that helps most."""
    grams = dict(grams)
    for _ in range(4 * len(lines)):
        current = _score(lines, target, grams)
        if current == 0:
            break
        best: tuple[float, str, float] | None = None
        for line in lines:
            if line.locked:
                continue
            lo, hi = bounds(line)
            for move in (_step(line), -_step(line)):
                value = grams[line.key] + move
                if value < lo - 1e-9 or value > hi + 1e-9:
                    continue
                score = _score(lines, target, {**grams, line.key: value})
                if score < current and (best is None or score < best[0]):
                    best = (score, line.key, value)
        if best is None:
            break
        grams[best[1]] = best[2]
    return grams


def _explain(
    lines: list[Line], grams: dict[str, float], original: Nutrients, target: Target
) -> list[Change]:
    changes = []
    for line in lines:
        new = grams[line.key]
        if math.isclose(new, line.grams, abs_tol=0.5):
            continue
        changes.append(Change(line.key, line.grams, new, _reason(line, new, original, target)))
    return changes


def _reason(line: Line, new: float, original: Nutrients, target: Target) -> Reason:
    up = new > line.grams
    p = line.per_100g
    protein_rich = p.kcal > 0 and p.protein_g * 4 / p.kcal >= 0.4
    if line.optional and new == 0:
        return Reason.REMOVED_OPTIONAL
    if up and protein_rich and original.protein_g < target.protein_min_g:
        return Reason.RAISE_PROTEIN
    if up and line.role is CulinaryRole.VEGETABLE:
        return Reason.MORE_VOLUME
    if abs(new - line.grams) <= _step(line) and math.isclose(
        original.kcal, target.kcal, rel_tol=KCAL_TOLERANCE_ROUNDED
    ):
        return Reason.ROUNDING
    if not up and p.fat_g * 9 > p.kcal * 0.5 and target.fat_g is not None:
        return Reason.LOWER_FAT
    if p.carbs_g * 4 > p.kcal * 0.5 and target.carbs_g is not None:
        return Reason.ADJUST_CARBS
    return Reason.ADD_CALORIES if up else Reason.CUT_CALORIES
