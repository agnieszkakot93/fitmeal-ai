"""Converting recipe quantities ("2 łyżki", "1 cup", "3 cloves") to grams.

Three kinds of units:

* **mass** units convert directly (g, kg, oz, dag ...).
* **volume** units need the food's density (ml, tbsp, szklanka ...).
* **portion** units are food-specific weights (piece, clove, slice, scoop,
  handful ...) looked up in the food's portion table.

Anything we cannot convert raises :class:`UnitConversionError`; the import
pipeline turns that into a clarification question instead of guessing.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum

from app.core.text import fold


class UnitKind(StrEnum):
    MASS = "mass"
    VOLUME = "volume"
    PORTION = "portion"


@dataclass(frozen=True, slots=True)
class Unit:
    code: str
    kind: UnitKind
    # grams per unit for MASS, millilitres per unit for VOLUME, unused for PORTION
    factor: float = 1.0


UNITS: dict[str, Unit] = {
    u.code: u
    for u in [
        Unit("g", UnitKind.MASS, 1.0),
        Unit("dag", UnitKind.MASS, 10.0),
        Unit("kg", UnitKind.MASS, 1000.0),
        Unit("oz", UnitKind.MASS, 28.3495),
        Unit("lb", UnitKind.MASS, 453.592),
        Unit("ml", UnitKind.VOLUME, 1.0),
        Unit("l", UnitKind.VOLUME, 1000.0),
        Unit("tsp", UnitKind.VOLUME, 5.0),
        Unit("tbsp", UnitKind.VOLUME, 15.0),
        # US cup; Polish "szklanka" is its own unit below
        Unit("cup", UnitKind.VOLUME, 240.0),
        Unit("szklanka", UnitKind.VOLUME, 250.0),
        Unit("fl_oz", UnitKind.VOLUME, 29.5735),
        Unit("pinch", UnitKind.PORTION),
        Unit("piece", UnitKind.PORTION),
        Unit("clove", UnitKind.PORTION),
        Unit("slice", UnitKind.PORTION),
        Unit("scoop", UnitKind.PORTION),
        Unit("handful", UnitKind.PORTION),
        Unit("can", UnitKind.PORTION),
        Unit("bunch", UnitKind.PORTION),
        Unit("stalk", UnitKind.PORTION),
        Unit("pack", UnitKind.PORTION),
    ]
}

# Lower-cased, diacritics-stripped spelling → unit code. Polish declensions are
# listed explicitly; that is simpler and more predictable than stemming.
UNIT_ALIASES: dict[str, str] = {
    # mass
    "g": "g", "gr": "g", "gram": "g", "grams": "g", "gramy": "g", "gramow": "g", "grama": "g",
    "dag": "dag", "dkg": "dag", "deko": "dag",
    "kg": "kg", "kilo": "kg", "kilogram": "kg", "kilograms": "kg", "kilogramy": "kg",
    "oz": "oz", "ounce": "oz", "ounces": "oz",
    "lb": "lb", "lbs": "lb", "pound": "lb", "pounds": "lb",
    # volume
    "ml": "ml", "millilitre": "ml", "milliliter": "ml", "milliliters": "ml", "mililitr": "ml",
    "mililitrow": "ml",
    "l": "l", "litre": "l", "liter": "l", "liters": "l", "litr": "l", "litry": "l", "litrow": "l",
    "tsp": "tsp", "teaspoon": "tsp", "teaspoons": "tsp", "lyzeczka": "tsp", "lyzeczki": "tsp",
    "lyzeczek": "tsp", "lyzeczke": "tsp", "lyz.": "tsp",
    "tbsp": "tbsp", "tablespoon": "tbsp", "tablespoons": "tbsp", "tbs": "tbsp", "lyzka": "tbsp",
    "lyzki": "tbsp", "lyzek": "tbsp", "lyzke": "tbsp",
    "cup": "cup", "cups": "cup",
    "szklanka": "szklanka", "szklanki": "szklanka", "szklanek": "szklanka", "szklanke": "szklanka",
    "fl oz": "fl_oz",
    # portions
    "pinch": "pinch", "szczypta": "pinch", "szczypty": "pinch", "szczypte": "pinch",
    "piece": "piece", "pieces": "piece", "pc": "piece", "pcs": "piece", "szt": "piece",
    "szt.": "piece", "sztuka": "piece", "sztuki": "piece", "sztuk": "piece", "whole": "piece",
    "clove": "clove", "cloves": "clove", "zabek": "clove", "zabki": "clove", "zabkow": "clove",
    "slice": "slice", "slices": "slice", "plaster": "slice", "plastry": "slice",
    "plastrow": "slice", "kromka": "slice", "kromki": "slice", "kromek": "slice",
    "scoop": "scoop", "scoops": "scoop", "miarka": "scoop", "miarki": "scoop", "miarek": "scoop",
    "handful": "handful", "handfuls": "handful", "garsc": "handful", "garscie": "handful",
    "can": "can", "cans": "can", "tin": "can", "puszka": "can", "puszki": "can",
    "bunch": "bunch", "peczek": "bunch", "peczki": "bunch",
    "stalk": "stalk", "stalks": "stalk", "lodyga": "stalk", "lodygi": "stalk",
    "pack": "pack", "package": "pack", "opakowanie": "pack", "opakowania": "pack",
}  # fmt: skip


class UnitConversionError(ValueError):
    """The quantity cannot be converted to grams without more information."""


def resolve_unit(raw: str) -> Unit:
    folded = fold(raw)
    code = UNIT_ALIASES.get(folded) or UNIT_ALIASES.get(folded.rstrip("."))
    if code is None:
        raise UnitConversionError(f"unknown unit: {raw!r}")
    return UNITS[code]


@dataclass(frozen=True, slots=True)
class FoodUnitData:
    """The per-food facts needed to convert volume and portion units."""

    density_g_per_ml: float | None = None
    portions_g: Mapping[str, float] | None = None


def to_grams(amount: float, unit: str | Unit, food: FoodUnitData) -> float:
    if amount < 0:
        raise ValueError("amount must be non-negative")
    u = unit if isinstance(unit, Unit) else resolve_unit(unit)

    if u.kind is UnitKind.MASS:
        return amount * u.factor

    if u.kind is UnitKind.VOLUME:
        # A food may define its own weight for a volume unit (e.g. 1 szklanka
        # of flour is weighed, not derived from density). Prefer that.
        if food.portions_g and u.code in food.portions_g:
            return amount * food.portions_g[u.code]
        if food.density_g_per_ml is None:
            raise UnitConversionError(f"no density known to convert {u.code} to grams")
        return amount * u.factor * food.density_g_per_ml

    grams = (food.portions_g or {}).get(u.code)
    if grams is None:
        raise UnitConversionError(f"no portion weight known for {u.code}")
    return amount * grams
