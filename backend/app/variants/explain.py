"""Plain-words explanations of every change ("Why did Donut change this?", PRD §8.3, §9).

Each change gets one sentence with its nutritional effect, e.g. "Reduced olive
oil by 8 g to fit the meal's calories → saves 72 kcal". A left-out ingredient
never says why: the reason can be an exclusion, and saved variants must not
reveal the health profile (D8, D13).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from app.foods.vocab import CulinaryRole
from app.nutrition.nutrients import Nutrients
from app.optimizer.substitute import MATCH_NUTRIENT
from app.optimizer.transform import Reason


class Kind(StrEnum):
    AMOUNT = "amount"  # same food, a different amount
    SWAP = "swap"  # a different food doing the same job
    LEFT_OUT = "left_out"


_WHY: dict[Reason, str] = {
    Reason.RAISE_PROTEIN: "to reach the protein minimum",
    Reason.CUT_CALORIES: "to fit the meal's calories",
    Reason.ADD_CALORIES: "to fit the meal's calories",
    Reason.LOWER_FAT: "to lower the fat",
    Reason.ADJUST_CARBS: "to match the carbs",
    Reason.MORE_VOLUME: "for more volume",
    Reason.REMOVED_OPTIONAL: "as it's optional",
    Reason.ROUNDING: "to a practical amount",
}

_MATCHED = {"protein_g": "protein", "carbs_g": "carbs", "fat_g": "fat"}


@dataclass(frozen=True, slots=True)
class Explanation:
    key: str
    kind: Kind
    message: str
    delta: Nutrients  # the change's effect on one serving
    reason: Reason | None = None


def grams(value: float) -> str:
    return f"{round(value, 1):g} g"


def effect(delta: Nutrients) -> str:
    """'saves 72 kcal', '+40 kcal, +9 g protein'."""
    parts = []
    kcal = round(delta.kcal)
    if kcal < 0:
        parts.append(f"saves {-kcal} kcal")
    elif kcal > 0:
        parts.append(f"+{kcal} kcal")
    protein = round(delta.protein_g)
    if protein:
        parts.append(f"{protein:+d} g protein")
    return ", ".join(parts) or "about the same nutrition"


def amount(
    key: str, name: str, from_g: float, to_g: float, delta: Nutrients, reason: Reason
) -> Explanation:
    verb = "Increased" if to_g > from_g else "Reduced"
    if reason is Reason.ROUNDING:
        message = f"Rounded {name} to {grams(to_g)} → {effect(delta)}"
    else:
        message = f"{verb} {name} by {grams(abs(to_g - from_g))} {_WHY[reason]} → {effect(delta)}"
    return Explanation(key, Kind.AMOUNT, message, delta, reason)


def swap(
    key: str,
    name: str,
    from_g: float,
    new_name: str,
    to_g: float,
    role: CulinaryRole,
    delta: Nutrients,
    missing: bool = False,
) -> Explanation:
    matched = MATCH_NUTRIENT.get(role)
    job = f"to match its {_MATCHED[matched]}" if matched else "at the same weight"
    if missing:
        message = (
            f"You don't have {name}: using {grams(to_g)} {new_name} instead, {job} "
            f"→ {effect(delta)}"
        )
    else:
        message = (
            f"Swapped {name} ({grams(from_g)}) for {new_name} ({grams(to_g)}), {job} "
            f"→ {effect(delta)}"
        )
    return Explanation(key, Kind.SWAP, message, delta)


def left_out(
    key: str, name: str, from_g: float, delta: Nutrients, missing: bool = False
) -> Explanation:
    prefix = f"You don't have {name}: left it out" if missing else f"Left out {name}"
    return Explanation(key, Kind.LEFT_OUT, f"{prefix} ({grams(from_g)}) → {effect(delta)}", delta)
