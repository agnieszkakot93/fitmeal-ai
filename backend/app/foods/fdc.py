"""Reading USDA FoodData Central CSV downloads.

Supports the "Foundation Foods" and "SR Legacy" CSV zips from
https://fdc.nal.usda.gov/download-datasets (public domain). Each unzipped
directory contains ``food.csv``, ``nutrient.csv`` and ``food_nutrient.csv``.
"""

from __future__ import annotations

import csv
import difflib
import re
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from app.nutrition.nutrients import Nutrients, energy_is_consistent

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
    if kcal is None or protein is None or fat is None:
        return None
    if carbs_total is None:
        # SR Legacy leaves carbohydrate out for many raw meats and fish, where it is 0.
        # Accept that only when protein and fat alone explain the energy.
        carbs_total = 0.0
        if not energy_is_consistent(Nutrients(kcal, protein, fat, 0.0, 0.0)):
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


# FDC appends this to many SR Legacy descriptions; curated names may leave it out.
_SUFFIX = re.compile(r"\s*\(includes foods for usda's food distribution program\)\s*$")


def _key(description: str) -> str:
    return _SUFFIX.sub("", description.casefold()).strip()


def _words(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.casefold()))


class FdcIndex:
    """Foods from one or more FDC directories, looked up by id or description."""

    def __init__(self, foods: Iterable[FdcFood], incomplete: dict[int, str] | None = None) -> None:
        self.by_id: dict[int, FdcFood] = {}
        self._by_description: dict[str, list[FdcFood]] = {}
        # in food.csv, but without the core nutrients: id -> description
        self.incomplete = dict(incomplete or {})
        for food in foods:
            self.by_id[food.fdc_id] = food
            self._by_description.setdefault(_key(food.description), []).append(food)

    def __len__(self) -> int:
        return len(self.by_id)

    def find(self, *, fdc_id: int | None = None, description: str | None = None) -> FdcFood | None:
        if fdc_id is not None:
            return self.by_id.get(fdc_id)
        if description is None:
            return None
        matches = self._by_description.get(_key(description), [])
        # Foundation Foods are the newer analyses; prefer them over SR Legacy.
        matches = sorted(matches, key=lambda f: DATA_TYPES.index(f.data_type))
        return matches[0] if matches else None

    def suggest(self, description: str, n: int = 5) -> list[str]:
        """Closest descriptions, by shared words first, then by spelling."""
        wanted = _words(description)
        if not wanted:
            return []

        def score(key: str) -> tuple[float, float]:
            words = _words(key)
            overlap = len(wanted & words) / len(wanted | words)
            return overlap, difflib.SequenceMatcher(None, _key(description), key).ratio()

        ranked = sorted(self._by_description, key=score, reverse=True)
        return [k for k in ranked[:n] if score(k)[0] > 0]

    def incomplete_matches(self, description: str) -> list[str]:
        """Same-named foods that were skipped because core nutrients are missing."""
        key = _key(description)
        return [f"{i}: {d}" for i, d in self.incomplete.items() if _key(d) == key]


def load_fdc_dirs(dirs: Iterable[Path]) -> FdcIndex:
    foods: list[FdcFood] = []
    incomplete: dict[int, str] = {}
    for d in dirs:
        loaded, skipped = _load_dir(d)
        foods.extend(loaded)
        incomplete.update(skipped)
    return FdcIndex(foods, incomplete)


def _load_dir(directory: Path) -> tuple[list[FdcFood], dict[int, str]]:
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
    incomplete = {}
    for fdc_id, (description, data_type) in meta.items():
        values = amounts.get(fdc_id, {})
        nutrients = to_nutrients(values)
        if nutrients is None:
            incomplete[fdc_id] = description
            continue
        foods.append(FdcFood(fdc_id, description, data_type, nutrients, _first(values, WATER)))
    return foods, incomplete


def write_snapshot(foods: Iterable[FdcFood], directory: Path) -> int:
    """Write ``foods`` as a minimal FDC CSV directory that ``load_fdc_dirs`` reads back.

    Lets the repository carry the few hundred records the curated list uses
    (public domain) instead of the 1.7 GB download. Carbohydrate is written
    "by difference" (available + fiber), so it round-trips through
    :func:`to_nutrients` unchanged.
    """
    directory.mkdir(parents=True, exist_ok=True)
    rows = sorted(foods, key=lambda f: f.fdc_id)
    with (directory / "food.csv").open("w", encoding="utf-8", newline="") as fh:
        out = csv.writer(fh, quoting=csv.QUOTE_ALL)
        out.writerow(["fdc_id", "data_type", "description"])
        for food in rows:
            out.writerow([food.fdc_id, food.data_type, food.description])
    with (directory / "food_nutrient.csv").open("w", encoding="utf-8", newline="") as fh:
        out = csv.writer(fh, quoting=csv.QUOTE_ALL)
        out.writerow(["id", "fdc_id", "nutrient_id", "amount"])
        row_id = 0
        for food in rows:
            n = food.nutrients
            values = {
                ENERGY_KCAL[0]: n.kcal,
                PROTEIN[0]: n.protein_g,
                FAT[0]: n.fat_g,
                CARBS_BY_DIFFERENCE[0]: n.carbs_g + n.fiber_g,
                FIBER[0]: n.fiber_g,
            }
            if food.water_g is not None:
                values[WATER[0]] = food.water_g
            for nutrient_id, amount in values.items():
                row_id += 1
                out.writerow([row_id, food.fdc_id, nutrient_id, round(amount, 4)])
    return len(rows)
