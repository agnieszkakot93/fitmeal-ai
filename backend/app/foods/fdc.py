"""Reading USDA FoodData Central CSV downloads.

Supports the "Foundation Foods" and "SR Legacy" CSV zips from
https://fdc.nal.usda.gov/download-datasets (public domain). Each unzipped
directory contains ``food.csv``, ``nutrient.csv`` and ``food_nutrient.csv``.
"""

from __future__ import annotations

import csv
import difflib
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from app.nutrition.nutrients import Nutrients

DATA_TYPES = ("foundation_food", "sr_legacy_food")

# FDC nutrient ids, in order of preference where there are alternatives.
ENERGY_KCAL = (1008, 2048, 2047)  # Energy; Atwater specific; Atwater general
PROTEIN = (1003,)
FAT = (1004, 1085)  # Total lipid; Total fat (NLEA)
CARBS_BY_DIFFERENCE = (1005, 1050)  # by difference; by summation
FIBER = (1079,)
WATER = (1051,)
WANTED = {*ENERGY_KCAL, *PROTEIN, *FAT, *CARBS_BY_DIFFERENCE, *FIBER, *WATER}


@dataclass(frozen=True, slots=True)
class FdcFood:
    fdc_id: int
    description: str
    data_type: str
    nutrients: Nutrients
    water_g: float | None


class FdcDataError(ValueError):
    pass


def _first(values: dict[int, float], ids: tuple[int, ...]) -> float | None:
    for nid in ids:
        if nid in values:
            return values[nid]
    return None


def to_nutrients(values: dict[int, float]) -> Nutrients | None:
    """Build per-100 g nutrients from FDC amounts; None when a core value is missing."""
    kcal = _first(values, ENERGY_KCAL)
    protein = _first(values, PROTEIN)
    fat = _first(values, FAT)
    carbs_total = _first(values, CARBS_BY_DIFFERENCE)
    if kcal is None or protein is None or fat is None or carbs_total is None:
        return None
    fiber = _first(values, FIBER) or 0.0
    # FDC carbohydrate includes fiber; the engine uses EU "available" carbs.
    return Nutrients(
        kcal=kcal,
        protein_g=protein,
        fat_g=fat,
        carbs_g=max(0.0, carbs_total - fiber),
        fiber_g=fiber,
    )


class FdcIndex:
    """Foods from one or more FDC directories, looked up by id or description."""

    def __init__(self, foods: Iterable[FdcFood]) -> None:
        self.by_id: dict[int, FdcFood] = {}
        self._by_description: dict[str, list[FdcFood]] = {}
        for food in foods:
            self.by_id[food.fdc_id] = food
            self._by_description.setdefault(food.description.casefold(), []).append(food)

    def __len__(self) -> int:
        return len(self.by_id)

    def find(self, *, fdc_id: int | None = None, description: str | None = None) -> FdcFood | None:
        if fdc_id is not None:
            return self.by_id.get(fdc_id)
        if description is None:
            return None
        matches = self._by_description.get(description.casefold(), [])
        # Foundation Foods are the newer analyses; prefer them over SR Legacy.
        matches = sorted(matches, key=lambda f: DATA_TYPES.index(f.data_type))
        return matches[0] if matches else None

    def suggest(self, description: str, n: int = 5) -> list[str]:
        return difflib.get_close_matches(
            description.casefold(), list(self._by_description), n=n, cutoff=0.6
        )


def load_fdc_dirs(dirs: Iterable[Path]) -> FdcIndex:
    foods: list[FdcFood] = []
    for d in dirs:
        foods.extend(_load_dir(d))
    return FdcIndex(foods)


def _load_dir(directory: Path) -> list[FdcFood]:
    for name in ("food.csv", "food_nutrient.csv"):
        if not (directory / name).is_file():
            raise FdcDataError(f"{directory} has no {name}; is this an unzipped FDC CSV download?")

    meta: dict[int, tuple[str, str]] = {}
    with (directory / "food.csv").open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            if row["data_type"] in DATA_TYPES:
                meta[int(row["fdc_id"])] = (row["description"], row["data_type"])

    amounts: dict[int, dict[int, float]] = {}
    with (directory / "food_nutrient.csv").open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            fdc_id = int(row["fdc_id"])
            nutrient_id = int(row["nutrient_id"])
            if fdc_id not in meta or nutrient_id not in WANTED or not row["amount"]:
                continue
            amounts.setdefault(fdc_id, {})[nutrient_id] = float(row["amount"])

    foods = []
    for fdc_id, (description, data_type) in meta.items():
        values = amounts.get(fdc_id, {})
        nutrients = to_nutrients(values)
        if nutrients is None:
            continue
        foods.append(FdcFood(fdc_id, description, data_type, nutrients, _first(values, WATER)))
    return foods
