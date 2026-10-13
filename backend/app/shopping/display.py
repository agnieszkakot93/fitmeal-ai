"""Friendly amounts for a shopping list line: "3 pieces", "450 g", "1.3 kg", "1.5 l".

Every amount is rounded up, so the list never under-buys. Wording and
plurals are the client's job; this returns a number and a unit code.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import StrEnum

from app.shopping.packages import EPS


class DisplayUnit(StrEnum):
    G = "g"
    KG = "kg"
    ML = "ml"
    L = "l"
    PIECE = "piece"
    CAN = "can"


@dataclass(frozen=True, slots=True)
class Amount:
    value: float  # a whole number except for kg and l, which have one decimal
    unit: DisplayUnit


def round_up(x: float, step: float) -> float:
    return math.ceil(x / step - EPS) * step


def _metric(x: float, small: DisplayUnit, large: DisplayUnit) -> Amount:
    """Grams or millilitres: 1 g steps below 10, 5 below 100, 10 below 1000, then 0.1 kg."""
    if x >= 1000 - EPS:
        return Amount(round(round_up(x / 1000, 0.1), 1), large)
    step = 1 if x < 10 else 5 if x < 100 else 10
    value = max(1, round(round_up(x, step)))
    if value >= 1000:  # e.g. 995 g rounds up to 1000 g
        return Amount(1.0, large)
    return Amount(value, small)


def mass(grams: float) -> Amount:
    return _metric(grams, DisplayUnit.G, DisplayUnit.KG)


def volume(ml: float) -> Amount:
    return _metric(ml, DisplayUnit.ML, DisplayUnit.L)


def count(grams: float, each_g: float, unit: DisplayUnit) -> Amount:
    return Amount(max(1, math.ceil(grams / each_g - EPS)), unit)


def to_grams(amount: Amount, *, density_g_per_ml: float | None, each_g: float | None) -> float:
    """What a displayed amount weighs: the inverse used to check nothing is under-bought."""
    factor = {
        DisplayUnit.G: 1.0,
        DisplayUnit.KG: 1000.0,
        DisplayUnit.ML: density_g_per_ml,
        DisplayUnit.L: None if density_g_per_ml is None else density_g_per_ml * 1000,
        DisplayUnit.PIECE: each_g,
        DisplayUnit.CAN: each_g,
    }[amount.unit]
    if factor is None:
        raise ValueError(f"{amount.unit} needs a density or a unit weight")
    return amount.value * factor
