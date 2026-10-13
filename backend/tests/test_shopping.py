"""Shopping list aggregation (PRD §8.10)."""

from __future__ import annotations

import itertools
import math
import random
from functools import cache
from typing import Any

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from app.foods.curated import load_curated
from app.foods.vocab import FoodCategory
from app.nutrition.units import FoodUnitData, to_grams
from app.planner.plan import plan
from app.planner.result import Plan
from app.recipes.catalog import load_catalog
from app.shopping import display
from app.shopping.aggregate import (
    FoodFacts,
    Need,
    RecipeLine,
    build_list,
    display_amount,
    facts_from_curated,
    needs_from_plan,
)
from app.shopping.display import Amount, DisplayUnit
from app.shopping.packages import EPS, PackageCount, choose_packages
from tests.test_foods_db import CURATED
from tests.test_planner_catalog import CATALOG, CONFIG, TYPICAL, load_extract


@cache
def curated_facts() -> dict[str, FoodFacts]:
    return facts_from_curated(load_curated(CURATED))


def _facts(key: str, category: FoodCategory = FoodCategory.OTHER, **kw: Any) -> FoodFacts:
    return FoodFacts(key, key.title(), key.upper(), category, **kw)


# --- packages ---


def test_single_size_rounds_up() -> None:
    p = choose_packages(1200, [500])
    assert p is not None
    assert p.buy == (PackageCount(500, 3),)
    assert p.leftover_g == 300


def test_fewest_packages_then_least_leftover() -> None:
    p = choose_packages(1200, [400, 500, 1000])
    assert p is not None
    # 2 packages is the fewest; 1000 + 400 wastes less than 1000 + 500
    assert p.buy == (PackageCount(1000, 1), PackageCount(400, 1))
    assert p.leftover_g == 200


def test_one_big_package_is_not_bought_for_a_small_need() -> None:
    # 1 x 1000 g would leave a whole 400 g package unused
    p = choose_packages(600, [400, 1000])
    assert p is not None
    assert p.buy == (PackageCount(400, 2),)


def test_exact_fit_and_float_noise() -> None:
    p = choose_packages(150 * 3 + 1e-9, [150, 450])
    assert p is not None
    assert p.buy == (PackageCount(450, 1),)
    assert p.leftover_g == 0


def test_no_sizes_and_zero_need() -> None:
    assert choose_packages(300, []) is None
    p = choose_packages(0, [500])
    assert p is not None
    assert p.count == 0


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        choose_packages(-1, [500])
    with pytest.raises(ValueError):
        choose_packages(100, [0.2])


sizes_st = st.lists(st.integers(1, 1500), min_size=1, max_size=4)
need_st = st.floats(0.01, 6000, allow_nan=False)


@given(need_st, sizes_st)
def test_packages_cover_need_and_leftover_is_under_smallest(need: float, sizes: list[int]) -> None:
    p = choose_packages(need, sizes)
    assert p is not None
    assert p.total_g >= need - EPS
    assert p.leftover_g < min(sizes)
    assert all(pc.size_g in sizes and pc.count > 0 for pc in p.buy)
    assert [pc.size_g for pc in p.buy] == sorted({pc.size_g for pc in p.buy}, reverse=True)


@settings(max_examples=60)
@given(st.floats(1, 900, allow_nan=False), st.lists(st.integers(50, 500), min_size=1, max_size=3))
def test_packages_match_brute_force(need: float, sizes: list[int]) -> None:
    p = choose_packages(need, sizes)
    assert p is not None
    best = None
    for n in range(1, math.ceil(need / min(sizes)) + 1):
        for combo in itertools.combinations_with_replacement(sorted(set(sizes)), n):
            total = sum(combo)
            if total >= math.ceil(need - EPS) and total - need < min(sizes):
                key = (n, total)
                best = key if best is None or key < best else best
        if best is not None:
            break
    assert best == (p.count, p.total_g)


# --- display amounts ---


@pytest.mark.parametrize(
    ("grams", "expected"),
    [
        (0.3, Amount(1, DisplayUnit.G)),
        (7.2, Amount(8, DisplayUnit.G)),
        (42, Amount(45, DisplayUnit.G)),
        (45.0000001, Amount(45, DisplayUnit.G)),
        (451, Amount(460, DisplayUnit.G)),
        (995, Amount(1.0, DisplayUnit.KG)),
        (1000, Amount(1.0, DisplayUnit.KG)),
        (1240, Amount(1.3, DisplayUnit.KG)),
    ],
)
def test_mass(grams: float, expected: Amount) -> None:
    assert display.mass(grams) == expected


def test_eggs_onions_and_cans_are_counted() -> None:
    foods = curated_facts()
    assert display_amount(foods["egg-whole-raw"], 260) == Amount(6, DisplayUnit.PIECE)
    assert display_amount(foods["onion"], 150) == Amount(2, DisplayUnit.PIECE)
    assert display_amount(foods["tomatoes-canned"], 800) == Amount(2, DisplayUnit.CAN)


def test_meat_small_pieces_and_liquids_are_measured() -> None:
    foods = curated_facts()
    # chicken breast has a piece weight but is bought by weight
    assert display_amount(foods["chicken-breast-raw"], 640) == Amount(640, DisplayUnit.G)
    assert display_amount(foods["olives-black"], 30) == Amount(30, DisplayUnit.G)
    assert display_amount(foods["milk-2"], 1545) == Amount(1.5, DisplayUnit.L)


@given(st.floats(0.01, 20000, allow_nan=False))
def test_displayed_amount_never_under_buys(grams: float) -> None:
    for food in (
        _facts("x"),
        _facts("egg", FoodCategory.DAIRY_EGGS, portions_g={"piece": 50}),
        _facts("milk", density_g_per_ml=1.03, liquid=True),
    ):
        amount = display_amount(food, grams)
        each = food.portions_g.get("piece")
        shown = display.to_grams(amount, density_g_per_ml=food.density_g_per_ml, each_g=each)
        assert shown >= grams * (1 - 1e-9)


# --- aggregation ---


def test_sums_groups_and_orders() -> None:
    foods = {
        "rice": _facts("rice", FoodCategory.GRAINS_PASTA, packages_g=(1000,)),
        "apple": _facts("apple", FoodCategory.FRUIT, portions_g={"piece": 180}),
        "banana": _facts("banana", FoodCategory.FRUIT, portions_g={"piece": 120}),
        "carrot": _facts("carrot", FoodCategory.VEGETABLES),
    }
    needs = [Need("rice", 300), Need("banana", 100), Need("rice", 450), Need("apple", 200)]
    needs += [Need("carrot", 80)]
    lst = build_list(needs, foods)
    assert [s.category for s in lst.sections] == [
        FoodCategory.VEGETABLES,
        FoodCategory.FRUIT,
        FoodCategory.GRAINS_PASTA,
    ]
    assert [i.food for i in lst.items] == ["carrot", "apple", "banana", "rice"]
    rice = lst.items[-1]
    assert rice.grams == 750
    assert rice.amount == Amount(750, DisplayUnit.G)
    assert rice.packages is not None
    assert rice.packages.buy == (PackageCount(1000, 1),)
    assert lst.items[1].amount == Amount(2, DisplayUnit.PIECE)


def test_sorts_by_name_in_the_chosen_language() -> None:
    foods = {
        "a": FoodFacts("a", "Apple", "Śliwka", FoodCategory.FRUIT),
        "b": FoodFacts("b", "Banana", "Banan", FoodCategory.FRUIT),
    }
    needs = [Need("a", 1), Need("b", 1)]
    assert [i.name for i in build_list(needs, foods, "en").items] == ["Apple", "Banana"]
    assert [i.name for i in build_list(needs, foods, "pl").items] == ["Banan", "Śliwka"]


def test_water_and_zero_needs_are_left_off() -> None:
    foods = curated_facts()
    lst = build_list([Need("water", 500), Need("onion", 0), Need("garlic", 8)], foods)
    assert [i.food for i in lst.items] == ["garlic"]


def test_unknown_food_and_negative_grams_raise() -> None:
    with pytest.raises(KeyError):
        build_list([Need("nope", 10)], {})
    with pytest.raises(ValueError):
        build_list([Need("x", -1)], {"x": _facts("x")})


FOODS = {
    f"f{i}": _facts(
        f"f{i}",
        list(FoodCategory)[i % len(FoodCategory)],
        packages_g=(250, 1000)[: i % 3],
        portions_g={"piece": 60} if i % 2 else {},
    )
    for i in range(8)
}
needs_st = st.lists(
    st.builds(Need, st.sampled_from(sorted(FOODS)), st.floats(0, 3000, allow_nan=False)),
    max_size=30,
)


@given(needs_st)
def test_totals_are_preserved(needs: list[Need]) -> None:
    lst = build_list(needs, FOODS)
    by_food = {i.food: i.grams for i in lst.items}
    for key in FOODS:
        expected = math.fsum(n.grams for n in needs if n.food == key)
        assert by_food.get(key, 0.0) == pytest.approx(expected, abs=EPS)
    for item in lst.items:
        if item.packages is not None:
            assert item.packages.total_g >= item.grams - EPS
            assert item.packages.leftover_g < min(FOODS[item.food].packages_g)


@given(needs_st, st.randoms(use_true_random=False))
def test_order_of_needs_does_not_matter(needs: list[Need], rnd: random.Random) -> None:
    shuffled = list(needs)
    rnd.shuffle(shuffled)
    assert build_list(needs, FOODS) == build_list(shuffled, FOODS)


# --- a real plan ---


@cache
def catalog_lines() -> dict[str, tuple[RecipeLine, ...]]:
    """Per-serving grams of every catalog recipe, keyed like the planner's lines."""
    foods = {f.slug: f for f in load_curated(CURATED).foods}
    lines = {}
    for r in load_catalog(CATALOG).recipes:
        out = []
        for position, ing in enumerate(r.ingredients):
            f = foods[ing.food]
            grams = to_grams(ing.amount, ing.unit, FoodUnitData(f.density_g_per_ml, f.portions))
            out.append(RecipeLine(f"{position}:{ing.food}", ing.food, grams / r.servings))
        lines[r.slug] = tuple(out)
    return lines


def test_list_from_a_real_week() -> None:
    week = plan(load_extract(), TYPICAL, CONFIG)
    assert isinstance(week, Plan)
    recipes = catalog_lines()
    needs = needs_from_plan(week, recipes)
    lst = build_list(needs, curated_facts())

    eaten: dict[str, float] = {}
    for meal in week.meals:
        for line in recipes[meal.recipe_id]:
            if line.key not in meal.leave_out:
                eaten[line.food] = eaten.get(line.food, 0.0) + line.grams * meal.portion
    eaten.pop("water", None)
    by_food = {i.food: i for i in lst.items}
    assert by_food.keys() == {k for k, g in eaten.items() if g > EPS}
    for key, grams in eaten.items():
        assert by_food[key].grams == pytest.approx(grams)

    order = list(FoodCategory)
    assert [order.index(s.category) for s in lst.sections] == sorted(
        order.index(s.category) for s in lst.sections
    )
    for item in lst.items:
        if item.packages is not None:
            assert item.packages.total_g >= item.grams - EPS
    assert build_list(reversed(needs), curated_facts()) == lst
