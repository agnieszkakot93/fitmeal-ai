"""Safety checks on the real curated ingredient file."""

from pathlib import Path

import pytest
from pydantic import ValidationError

from app.foods.curated import CuratedFile, load_curated
from app.nutrition.allergens import Allergen, Origin, effective_allergens, effective_traces

CURATED = Path(__file__).resolve().parents[2] / "data" / "foods" / "curated.yaml"


@pytest.fixture(scope="module")
def curated() -> CuratedFile:
    return load_curated(CURATED)


@pytest.fixture(scope="module")
def effective(curated: CuratedFile) -> dict[str, frozenset[Allergen]]:
    return effective_allergens(
        {f.slug: f.allergens for f in curated.foods},
        {f.slug: f.derived_from for f in curated.foods},
    )


def test_file_is_valid_and_non_trivial(curated: CuratedFile) -> None:
    assert len(curated.foods) >= 100


ORIGIN_ALLERGEN = {
    Origin.DAIRY: Allergen.MILK,
    Origin.EGG: Allergen.EGGS,
    Origin.FISH: Allergen.FISH,
}


def test_origin_implies_allergen(
    curated: CuratedFile, effective: dict[str, frozenset[Allergen]]
) -> None:
    missing = [
        f.slug
        for f in curated.foods
        if f.origin in ORIGIN_ALLERGEN and ORIGIN_ALLERGEN[f.origin] not in effective[f.slug]
    ]
    assert missing == []


def test_shellfish_declares_crustaceans_or_molluscs(
    curated: CuratedFile, effective: dict[str, frozenset[Allergen]]
) -> None:
    for f in curated.foods:
        if f.origin is Origin.SHELLFISH:
            assert effective[f.slug] & {Allergen.CRUSTACEANS, Allergen.MOLLUSCS}, f.slug


@pytest.mark.parametrize(
    ("slug", "allergen"),
    [
        ("whey-protein-isolate", Allergen.MILK),
        ("mayonnaise", Allergen.EGGS),
        ("soy-sauce", Allergen.GLUTEN),
        ("oats-rolled", Allergen.GLUTEN),
        ("celery-stalk", Allergen.CELERY),
        ("tahini", Allergen.SESAME),
    ],
)
def test_known_allergens(
    effective: dict[str, frozenset[Allergen]], slug: str, allergen: Allergen
) -> None:
    assert allergen in effective[slug]


def test_real_file_traces_never_repeat_contained_allergens(
    curated: CuratedFile, effective: dict[str, frozenset[Allergen]]
) -> None:
    traces = effective_traces(
        {f.slug: f.may_contain for f in curated.foods},
        {f.slug: f.derived_from for f in curated.foods},
        effective,
    )
    assert all(not (traces[slug] & effective[slug]) for slug in traces)


def _food(**extra: object) -> dict[str, object]:
    return {
        "slug": "granola",
        "name": {"en": "Granola", "pl": "Granola"},
        "category": "grains_pasta",
        "origin": "plant",
        "culinary_roles": ["carb_base"],
        **extra,
    }


def test_may_contain_defaults_to_none() -> None:
    food = CuratedFile.model_validate({"foods": [_food()]}).foods[0]
    assert food.may_contain == []


def test_may_contain_loads_separately_from_allergens() -> None:
    raw = _food(allergens=["gluten"], may_contain=["tree_nuts", "peanuts"])
    food = CuratedFile.model_validate({"foods": [raw]}).foods[0]
    assert food.allergens == [Allergen.GLUTEN]
    assert food.may_contain == [Allergen.TREE_NUTS, Allergen.PEANUTS]


@pytest.mark.parametrize(
    "extra",
    [
        {"allergens": ["gluten"], "may_contain": ["gluten"]},
        {"may_contain": ["walnuts"]},
    ],
)
def test_rejects_bad_may_contain(extra: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        CuratedFile.model_validate({"foods": [_food(**extra)]})


def test_rejects_unknown_parent() -> None:
    with pytest.raises(ValidationError):
        CuratedFile.model_validate(
            {
                "foods": [
                    {
                        "slug": "whey",
                        "name": {"en": "Whey", "pl": "Serwatka"},
                        "category": "other",
                        "origin": "dairy",
                        "culinary_roles": ["main_protein"],
                        "derived_from": ["milk"],
                    }
                ]
            }
        )


def test_rejects_mass_unit_as_portion() -> None:
    with pytest.raises(ValidationError):
        CuratedFile.model_validate(
            {
                "foods": [
                    {
                        "slug": "x",
                        "name": {"en": "X", "pl": "X"},
                        "category": "other",
                        "origin": "other",
                        "culinary_roles": ["seasoning"],
                        "portions": {"g": 5},
                    }
                ]
            }
        )
