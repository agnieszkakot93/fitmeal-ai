"""Sum ingredient needs over a plan and shape them into a shopping list.

Rounding never under-buys: every displayed amount is rounded up.
"""

from __future__ import annotations

import math
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field

from app.foods.curated import CuratedFile
from app.foods.vocab import CulinaryRole, FoodCategory
from app.planner.result import Plan

# FoodCategory is declared in store-walk order; that is the section order
CATEGORY_ORDER: tuple[FoodCategory, ...] = tuple(FoodCategory)

# portion units that read naturally on a shopping list, most natural first
COUNT_UNITS = ("piece", "can", "bunch", "head", "clove", "stalk", "slice", "pack")

# categories where a liquid is bought by volume
ML_CATEGORIES = frozenset({FoodCategory.DAIRY_EGGS, FoodCategory.BEVERAGES, FoodCategory.OILS_FATS})

# never on a shopping list
NOT_BOUGHT = frozenset({"water"})

# absorbs float noise from summing, so 200.0000000001 g is not shown as 201 g
_EPS = 1e-6


def round_up(x: float) -> int:
    return max(0, math.ceil(x - _EPS))


@dataclass(frozen=True, slots=True)
class FoodInfo:
    key: str  # food slug
    name_en: str
    name_pl: str
    category: FoodCategory
    density_g_per_ml: float | None = None
    portions_g: Mapping[str, float] = field(default_factory=dict)
    packages_g: tuple[float, ...] = ()
    liquid: bool = False


def foods_from_curated(curated: CuratedFile) -> dict[str, FoodInfo]:
    return {
        f.slug: FoodInfo(
            key=f.slug,
            name_en=f.name.en,
            name_pl=f.name.pl,
            category=f.category,
            density_g_per_ml=f.density_g_per_ml,
            portions_g=dict(f.portions),
            packages_g=tuple(f.packages_g),
            liquid=CulinaryRole.LIQUID in f.culinary_roles,
        )
        for f in curated.foods
    }


@dataclass(frozen=True, slots=True)
class IngredientLine:
    """One recipe ingredient, per serving."""

    key: str  # "<position>:<food slug>", as in PlannedMeal.leave_out
    food: str
    grams: float


@dataclass(frozen=True, slots=True)
class Need:
    food: str
    grams: float


def needs_from_plan(plan: Plan, recipe_lines: Mapping[str, Sequence[IngredientLine]]) -> list[Need]:
    """Grams of each ingredient eaten in the plan, left-out optional ones excluded.

    Batch meals count once per portion eaten: cooking two portions on day 1 for
    days 1 and 2 needs the same food as cooking one each day.
    """
    needs = []
    for meal in plan.meals:
        skip = set(meal.leave_out)
        for line in recipe_lines[meal.recipe_id]:
            if line.key not in skip:
                needs.append(Need(line.food, line.grams * meal.portion))
    return needs


@dataclass(frozen=True, slots=True)
class CountUnit:
    unit: str
    count: int  # rounded up


@dataclass(frozen=True, slots=True)
class Packages:
    size_g: float
    count: int
    leftover_g: int  # bought minus needed, rounded down so it is never overstated


@dataclass(frozen=True, slots=True)
class ShoppingItem:
    food: str
    name_en: str
    name_pl: str
    category: FoodCategory
    grams: int  # needed, rounded up
    ml: int | None = None  # liquids with a known density, rounded up
    count: CountUnit | None = None
    packages: Packages | None = None
    checked_g: int = 0  # already bought (ticked) on this or an earlier version of the list

    @property
    def still_to_buy_g(self) -> int:
        return max(0, self.grams - self.checked_g)

    @property
    def checked(self) -> bool:
        return self.checked_g > 0 and self.still_to_buy_g == 0


@dataclass(frozen=True, slots=True)
class Section:
    category: FoodCategory
    items: tuple[ShoppingItem, ...]


@dataclass(frozen=True, slots=True)
class ShoppingList:
    sections: tuple[Section, ...]

    @property
    def items(self) -> tuple[ShoppingItem, ...]:
        return tuple(i for s in self.sections for i in s.items)


def sum_needs(needs: Iterable[Need]) -> dict[str, float]:
    totals: dict[str, float] = {}
    for n in needs:
        if n.grams < 0:
            raise ValueError(f"{n.food}: negative grams")
        totals[n.food] = totals.get(n.food, 0.0) + n.grams
    return totals


def count_unit(grams: float, food: FoodInfo) -> CountUnit | None:
    for unit in COUNT_UNITS:
        size = food.portions_g.get(unit)
        if size:
            return CountUnit(unit, max(1, round_up(grams / size)))
    return None


def best_packages(grams: float, sizes: Sequence[float]) -> Packages | None:
    """The single package size that covers ``grams`` with the least left over.

    Ties go to fewer packages, then the smaller size, so the choice is stable.
    """
    best: tuple[float, int, float] | None = None
    for size in sizes:
        n = max(1, round_up(grams / size))
        key = (n * size - grams, n, size)
        if best is None or key < best:
            best = key
    if best is None:
        return None
    leftover, n, size = best
    return Packages(size, n, max(0, math.floor(leftover + _EPS)))


def make_item(food: FoodInfo, grams: float) -> ShoppingItem:
    ml = None
    if food.liquid and food.density_g_per_ml and food.category in ML_CATEGORIES:
        ml = round_up(grams / food.density_g_per_ml)
    return ShoppingItem(
        food=food.key,
        name_en=food.name_en,
        name_pl=food.name_pl,
        category=food.category,
        grams=round_up(grams),
        ml=ml,
        count=count_unit(grams, food),
        packages=best_packages(grams, food.packages_g),
    )


def build_list(needs: Iterable[Need], foods: Mapping[str, FoodInfo]) -> ShoppingList:
    """Sum the same food across meals and group by section in store-walk order."""
    totals = sum_needs(needs)
    unknown = sorted(k for k in totals if k not in foods)
    if unknown:
        raise KeyError(f"unknown foods: {unknown}")
    by_cat: dict[FoodCategory, list[ShoppingItem]] = {}
    for key, grams in totals.items():
        if key in NOT_BOUGHT or grams <= 0:
            continue
        food = foods[key]
        by_cat.setdefault(food.category, []).append(make_item(food, grams))
    return ShoppingList(
        tuple(
            Section(c, tuple(sorted(by_cat[c], key=lambda i: (i.name_en.casefold(), i.food))))
            for c in CATEGORY_ORDER
            if c in by_cat
        )
    )
