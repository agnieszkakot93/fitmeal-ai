from pathlib import Path

import pytest

from app.foods.fdc import FdcDataError, FdcIndex, load_fdc_dirs

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
