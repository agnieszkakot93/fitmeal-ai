from __future__ import annotations

import math

from hypothesis import given
from hypothesis import strategies as st

from app.foods.curated import load_curated
from app.foods.vocab import FoodCategory
from app.nutrition.nutrients import Nutrients
from app.nutrition.units import FoodUnitData, to_grams
from app.planner.result import DayPlan, Plan, PlannedMeal
from app.recipes.catalog import load_catalog
from app.shopping.aggregate import (
    CATEGORY_ORDER,
    FoodInfo,
    IngredientLine,
    Need,
    Packages,
    ShoppingList,
    best_packages,
    build_list,
    foods_from_curated,
    needs_from_plan,
)
from app.shopping.merge import check, merge, uncheck
from tests.test_foods_db import CURATED
from tests.test_planner_catalog import CATALOG, TYPICAL, _solve

FOODS = {
    "egg": FoodInfo("egg", "Egg", "Jajko", FoodCategory.DAIRY_EGGS, portions_g={"piece": 50}),
    "milk": FoodInfo(
        "milk", "Milk", "Mleko", FoodCategory.DAIRY_EGGS, 1.03, packages_g=(1000.0,), liquid=True
    ),
    "beans": FoodInfo("beans", "Beans", "Fasola", FoodCategory.LEGUMES, portions_g={"can": 240}),
    "chicken": FoodInfo(
        "chicken", "Chicken", "Kurczak", FoodCategory.MEAT_FISH, packages_g=(400, 500, 1000)
    ),
    "tomato": FoodInfo("tomato", "Tomato", "Pomidor", FoodCategory.VEGETABLES),
    "water": FoodInfo("water", "Water", "Woda", FoodCategory.BEVERAGES),
}


def _meal(day: int, recipe: str, portion: float, leave_out: tuple[str, ...] = ()) -> PlannedMeal:
    return PlannedMeal(day, "lunch", recipe, portion, Nutrients(), day, day, False, leave_out, ())


def test_sums_groups_and_annotates() -> None:
    needs = [
        Need("egg", 100),
        Need("egg", 60),
        Need("tomato", 150),
        Need("chicken", 450),
        Need("beans", 300),
        Need("milk", 250),
        Need("water", 500),
    ]
    lst = build_list(needs, FOODS)
    assert [s.category for s in lst.sections] == [
        FoodCategory.VEGETABLES,
        FoodCategory.MEAT_FISH,
        FoodCategory.DAIRY_EGGS,
        FoodCategory.LEGUMES,
    ]
    items = {i.food: i for i in lst.items}
    assert "water" not in items
    assert items["egg"].grams == 160
    assert items["egg"].count is not None and items["egg"].count.count == 4
    assert items["beans"].count is not None and items["beans"].count.unit == "can"
    assert items["beans"].count.count == 2
    assert items["milk"].ml == 243
    assert items["milk"].packages == Packages(1000.0, 1, 750)
    assert items["chicken"].packages == Packages(500, 1, 50)
    assert items["tomato"].count is None and items["tomato"].packages is None


def test_rounding_ignores_float_noise() -> None:
    lst = build_list([Need("tomato", 0.1)] * 10 + [Need("tomato", 199)], FOODS)
    assert lst.items[0].grams == 200


def test_best_packages_prefers_fewer_on_tie() -> None:
    assert best_packages(1000, [500, 1000]) == Packages(1000, 1, 0)
    assert best_packages(10, []) is None


def test_needs_from_plan_scales_and_leaves_out() -> None:
    lines = {"r": [IngredientLine("0:egg", "egg", 50), IngredientLine("1:milk", "milk", 100)]}
    plan = Plan(
        (DayPlan(0, (_meal(0, "r", 1.5, ("1:milk",)),)), DayPlan(1, (_meal(1, "r", 1),))), ()
    )
    needs = needs_from_plan(plan, lines)
    assert needs == [Need("egg", 75), Need("egg", 50), Need("milk", 100)]


def test_merge_keeps_checks_and_marks_extra() -> None:
    old = check(build_list([Need("egg", 100), Need("tomato", 100)], FOODS), "egg")
    new = build_list([Need("egg", 150), Need("chicken", 300)], FOODS)
    merged = {i.food: i for i in merge(old, new).items}
    assert not merged["egg"].checked and merged["egg"].still_to_buy_g == 50
    assert merged["chicken"].checked_g == 0
    shrunk = merge(old, build_list([Need("egg", 50)], FOODS))
    assert shrunk.items[0].checked
    assert uncheck(old, "egg").items[0].checked_g == 0


needs_st = st.lists(
    st.builds(
        Need,
        st.sampled_from(sorted(FOODS)),
        st.floats(min_value=0, max_value=5000, allow_nan=False),
    ),
    max_size=30,
)


@given(needs_st)
def test_totals_equal_sum_and_never_under_buy(needs: list[Need]) -> None:
    lst = build_list(needs, FOODS)
    order = [CATEGORY_ORDER.index(s.category) for s in lst.sections]
    assert order == sorted(order)
    for item in lst.items:
        exact = math.fsum(n.grams for n in needs if n.food == item.food)
        assert exact - 1e-6 <= item.grams < exact + 1
        food = FOODS[item.food]
        if item.packages:
            assert item.packages.count * item.packages.size_g >= exact - 1e-6
            assert (
                item.packages.leftover_g
                <= item.packages.count * item.packages.size_g - exact + 1e-6
            )
        if item.count and food.portions_g:
            assert item.count.count * food.portions_g[item.count.unit] >= exact - 1e-6
        if item.ml is not None:
            assert food.density_g_per_ml is not None
            assert item.ml * food.density_g_per_ml >= exact - 1e-3
    assert build_list(needs, FOODS) == lst


def _ticked(lst: ShoppingList, foods: list[str]) -> ShoppingList:
    for f in foods:
        if any(i.food == f for i in lst.items):
            lst = check(lst, f)
    return lst


@given(needs_st, needs_st, st.lists(st.sampled_from(sorted(FOODS))))
def test_merge_is_idempotent_and_never_loses_need(
    old_needs: list[Need], new_needs: list[Need], ticks: list[str]
) -> None:
    old = _ticked(build_list(old_needs, FOODS), ticks)
    new = build_list(new_needs, FOODS)
    once = merge(old, new)
    assert merge(once, new) == once
    assert merge(old, once) == once
    before = {i.food: i.checked_g for i in old.items}
    for item in once.items:
        assert item.checked_g == before.get(item.food, 0)
        assert item.checked_g + item.still_to_buy_g >= item.grams


def test_list_from_real_plan() -> None:
    curated = load_curated(CURATED)
    foods = foods_from_curated(curated)
    lines: dict[str, list[IngredientLine]] = {}
    for recipe in load_catalog(CATALOG).recipes:
        out = []
        for pos, line in enumerate(recipe.ingredients):
            f = foods[line.food]
            grams = to_grams(line.amount, line.unit, FoodUnitData(f.density_g_per_ml, f.portions_g))
            out.append(IngredientLine(f"{pos}:{line.food}", line.food, grams / recipe.servings))
        lines[recipe.slug] = out
    plan = _solve(TYPICAL)
    needs = needs_from_plan(plan, lines)
    lst = build_list(needs, foods)
    assert lst == build_list(needs_from_plan(_solve(TYPICAL), lines), foods)
    assert len(lst.items) == len({i.food for i in lst.items}) > 5
    for item in lst.items:
        exact = math.fsum(n.grams for n in needs if n.food == item.food)
        assert item.grams >= exact - 1e-6
