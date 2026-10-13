"""Sum a plan's ingredients into a shopping list grouped by store section (PRD §8.10)."""

from __future__ import annotations

import math
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Literal

from app.core.text import fold
from app.foods.curated import CuratedFile
from app.foods.vocab import CulinaryRole, FoodCategory
from app.planner.result import Plan
from app.shopping import display
from app.shopping.display import Amount, DisplayUnit
from app.shopping.packages import EPS, Packages, choose_packages

# FoodCategory is declared in store-walk order; that is the section order
SECTION_ORDER: tuple[FoodCategory, ...] = tuple(FoodCategory)

# sections where a food with a whole-piece weight is bought by the piece (eggs, onions,
# apples); meat breasts and fillets are weighed even though they have a piece weight
COUNTED_SECTIONS = frozenset({FoodCategory.VEGETABLES, FoodCategory.FRUIT, FoodCategory.DAIRY_EGGS})
# below this a "piece" is too small to count on a list (olives, sprouts, chillies)
MIN_PIECE_G = 20.0

# tap water and the like: in recipes, never on a shopping list
NOT_BOUGHT = frozenset({"water"})

Lang = Literal["en", "pl"]


@dataclass(frozen=True, slots=True)
class FoodFacts:
    """What the list needs to know about a food besides how much of it."""

    key: str  # slug or id, the same key the needs use
    name_en: str
    name_pl: str
    category: FoodCategory
    packages_g: tuple[float, ...] = ()
    portions_g: Mapping[str, float] = field(default_factory=dict)
    density_g_per_ml: float | None = None
    liquid: bool = False  # shown in ml / l when the density is known
    bought: bool = True

    def name(self, lang: Lang) -> str:
        return self.name_pl if lang == "pl" else self.name_en

    @property
    def count_unit(self) -> tuple[DisplayUnit, float] | None:
        """The unit this food is counted in on a list, with its weight, if any."""
        can = self.portions_g.get("can")
        if can:
            return DisplayUnit.CAN, can
        piece = self.portions_g.get("piece")
        if piece and piece >= MIN_PIECE_G and self.category in COUNTED_SECTIONS:
            return DisplayUnit.PIECE, piece
        return None


def facts_from_curated(curated: CuratedFile) -> dict[str, FoodFacts]:
    return {
        f.slug: FoodFacts(
            key=f.slug,
            name_en=f.name.en,
            name_pl=f.name.pl,
            category=f.category,
            packages_g=tuple(f.packages_g),
            portions_g=dict(f.portions),
            density_g_per_ml=f.density_g_per_ml,
            liquid=CulinaryRole.LIQUID in f.culinary_roles,
            bought=f.slug not in NOT_BOUGHT,
        )
        for f in curated.foods
    }


@dataclass(frozen=True, slots=True)
class Need:
    food: str
    grams: float


@dataclass(frozen=True, slots=True)
class RecipeLine:
    """One recipe ingredient in grams per serving."""

    key: str  # "<position>:<food>", as in PlannedMeal.leave_out
    food: str
    grams: float


def needs_from_plan(plan: Plan, recipes: Mapping[str, Sequence[RecipeLine]]) -> list[Need]:
    """What every meal in the plan uses, optional ingredients left out by the planner excluded.

    Each eaten portion counts once, so a batch cooked on day 1 for days 1 and 2
    needs the same food as cooking on each day.
    """
    needs = []
    for meal in plan.meals:
        skip = set(meal.leave_out)
        needs += [
            Need(line.food, line.grams * meal.portion)
            for line in recipes[meal.recipe_id]
            if line.key not in skip
        ]
    return needs


def sum_needs(needs: Iterable[Need]) -> dict[str, float]:
    """Grams per food; fsum makes the total independent of the order of the needs."""
    parts: dict[str, list[float]] = {}
    for n in needs:
        if n.grams < 0:
            raise ValueError(f"{n.food}: negative grams")
        parts.setdefault(n.food, []).append(n.grams)
    return {food: math.fsum(g) for food, g in parts.items()}


@dataclass(frozen=True, slots=True)
class ShoppingItem:
    food: str  # the key checkbox state is stored under
    name: str
    category: FoodCategory
    grams: float  # the exact total over the plan
    amount: Amount  # rounded up for display
    packages: Packages | None  # None when the food has no known package sizes


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


def display_amount(food: FoodFacts, grams: float) -> Amount:
    counted = food.count_unit
    if counted is not None:
        return display.count(grams, counted[1], counted[0])
    if food.liquid and food.density_g_per_ml:
        return display.volume(grams / food.density_g_per_ml)
    return display.mass(grams)


def make_item(food: FoodFacts, grams: float, lang: Lang = "en") -> ShoppingItem:
    return ShoppingItem(
        food=food.key,
        name=food.name(lang),
        category=food.category,
        grams=grams,
        amount=display_amount(food, grams),
        packages=choose_packages(grams, food.packages_g),
    )


def build_list(
    needs: Iterable[Need], foods: Mapping[str, FoodFacts], lang: Lang = "en"
) -> ShoppingList:
    """Sum each food over all meals and group it by section in store-walk order.

    Items within a section are sorted by their name in ``lang``, so the same
    needs in any order give the same list.
    """
    totals = sum_needs(needs)
    unknown = sorted(k for k in totals if k not in foods)
    if unknown:
        raise KeyError(f"no facts for foods: {unknown}")
    by_section: dict[FoodCategory, list[ShoppingItem]] = {}
    for key, grams in totals.items():
        food = foods[key]
        if not food.bought or grams <= EPS:
            continue
        by_section.setdefault(food.category, []).append(make_item(food, grams, lang))
    return ShoppingList(
        tuple(
            Section(c, tuple(sorted(by_section[c], key=lambda i: (fold(i.name), i.food))))
            for c in SECTION_ORDER
            if c in by_section
        )
    )
