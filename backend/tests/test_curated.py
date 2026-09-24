"""Safety checks on the real curated ingredient file."""

from pathlib import Path

import pytest
from pydantic import ValidationError

from app.foods.curated import CuratedFile, load_curated
from app.nutrition.allergens import Allergen, Origin, effective_allergens

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
