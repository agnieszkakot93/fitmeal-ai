from pathlib import Path

import pytest

from app.foods.fdc import FdcDataError, FdcFood, FdcIndex, load_fdc_dirs, to_nutrients
from app.nutrition.nutrients import Nutrients

FIXTURES = Path(__file__).parent / "fixtures" / "fdc"


@pytest.fixture(scope="module")
def index() -> FdcIndex:
    return load_fdc_dirs([FIXTURES])


def test_loads_foundation_and_sr_legacy_only(index: FdcIndex) -> None:
    assert 900003 not in index.by_id  # branded
    assert 171077 in index.by_id


def test_foods_missing_energy_are_skipped(index: FdcIndex) -> None:
    assert 900002 not in index.by_id


def test_carbs_exclude_fiber(index: FdcIndex) -> None:
    rice = index.by_id[900001].nutrients
    assert rice.carbs_g == pytest.approx(80.0 - 1.3)
    assert rice.fiber_g == pytest.approx(1.3)


def test_description_lookup_prefers_foundation(index: FdcIndex) -> None:
    egg = index.find(description="egg, WHOLE, raw, fresh")
    assert egg is not None
    assert egg.fdc_id == 748967
    # foundation record has only Atwater-specific energy
    assert egg.nutrients.kcal == 148


def test_lookup_by_id(index: FdcIndex) -> None:
    found = index.find(fdc_id=171413)
    assert found is not None
    assert found.nutrients.fat_g == 100


def test_suggestions_for_near_misses(index: FdcIndex) -> None:
    suggestions = index.suggest("Chicken, broiler or fryers, breast, meat, raw")
    assert suggestions[0] == "chicken, broilers or fryers, breast, meat only, raw"


def test_wrong_directory_is_explained(tmp_path: Path) -> None:
    with pytest.raises(FdcDataError):
        load_fdc_dirs([tmp_path])


def _food(fdc_id: int, description: str) -> FdcFood:
    return FdcFood(fdc_id, description, "sr_legacy_food", Nutrients(52, 0.3, 0.2, 11.4, 2.4), 86)


def test_description_matches_without_the_distribution_program_suffix() -> None:
    index = FdcIndex(
        [
            _food(
                171688,
                "Apples, raw, with skin (Includes foods for USDA's Food Distribution Program)",
            )
        ]
    )
    found = index.find(description="Apples, raw, with skin")
    assert found is not None and found.fdc_id == 171688


def test_missing_carbs_count_as_zero_only_when_energy_fits() -> None:
    lean_meat = {1008: 120.0, 1003: 22.5, 1004: 2.6}
    n = to_nutrients(lean_meat)
    assert n is not None and n.carbs_g == 0
    assert to_nutrients({1008: 300.0, 1003: 5.0, 1004: 1.0}) is None


def test_suggestions_share_words_and_incomplete_foods_are_named() -> None:
    index = FdcIndex(
        [
            _food(1, "Rice, brown, long grain, unenriched, raw"),
            _food(2, "Ostrich, top loin, raw"),
        ],
        incomplete={3: "Turkey, ground, raw"},
    )
    assert index.suggest("Rice, brown, long-grain, raw")[0].startswith("rice, brown")
    assert index.incomplete_matches("turkey, ground, raw") == ["3: Turkey, ground, raw"]
