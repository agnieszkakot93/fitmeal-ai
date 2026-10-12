"""Transformation with substitutions. Nutrition values are plausible test data."""

from app.foods.vocab import CulinaryRole as R
from app.nutrition.nutrients import Nutrients
from app.optimizer.combine import miss_size, transform_with_swaps
from app.optimizer.transform import Line, Target, nutrition, transform

EGG = Nutrients(143, 12.6, 9.5, 0.7, 0)
EGG_WHITE = Nutrients(52, 10.9, 0.2, 0.7, 0)
BREAD = Nutrients(250, 9, 3, 45, 6)
BUTTER = Nutrients(717, 0.9, 81, 0.1, 0)


def omelette() -> list[Line]:
    return [
        Line("eggs", EGG, 150, R.MAIN_PROTEIN),
        Line("bread", BREAD, 35, R.CARB_BASE),
        Line("butter", BUTTER, 5, R.COOKING_FAT),
    ]


def test_swap_rescues_a_target_amounts_alone_miss() -> None:
    lines = omelette()
    before = nutrition(lines, {ln.key: ln.grams for ln in lines})
    target = Target(before.kcal * 0.7, before.protein_g)
    assert not transform(lines, target).on_target

    alternatives = {"eggs": [Line("eggs=>white", EGG_WHITE, 150, R.MAIN_PROTEIN)]}
    combined = transform_with_swaps(lines, target, alternatives)
    assert combined.result.on_target, combined.result.misses
    assert [s.original_key for s in combined.swaps] == ["eggs"]
    assert "eggs=>white" in combined.result.grams


def test_no_swap_when_amounts_suffice_or_swap_does_not_help() -> None:
    lines = omelette()
    before = nutrition(lines, {ln.key: ln.grams for ln in lines})
    easy = Target(before.kcal * 0.95, before.protein_g * 0.9)
    alternatives = {"eggs": [Line("eggs=>white", EGG_WHITE, 150, R.MAIN_PROTEIN)]}
    assert transform_with_swaps(lines, easy, alternatives).swaps == []

    impossible = Target(before.kcal * 3, before.protein_g * 3)
    worse = {"eggs": [Line("eggs=>bread", BREAD, 20, R.MAIN_PROTEIN)]}
    combined = transform_with_swaps(lines, impossible, worse)
    assert combined.swaps == []
    assert miss_size(impossible, combined.result) > 0
