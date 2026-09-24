from pathlib import Path

import pytest
import yaml

from app import cli
from app.foods import importer
from app.foods.curated import CuratedFile
from app.foods.lint import allergen_problems


def _food(slug: str, en: str, pl: str, **extra: object) -> dict[str, object]:
    return {
        "slug": slug,
        "name": {"en": en, "pl": pl},
        "category": "other",
        "origin": "plant",
        "culinary_roles": ["carb_base"],
        **extra,
    }


def problems(*foods: dict[str, object]) -> list[str]:
    return allergen_problems(CuratedFile.model_validate({"foods": list(foods)}))


@pytest.mark.parametrize(
    ("origin", "allergens"),
    [
        ("dairy", ["milk"]),
        ("egg", ["eggs"]),
        ("fish", ["fish"]),
        ("shellfish", ["crustaceans"]),
        ("shellfish", ["molluscs"]),
    ],
)
def test_origin_with_its_allergen_is_fine(origin: str, allergens: list[str]) -> None:
    assert problems(_food("x", "X", "X", origin=origin, allergens=allergens)) == []


@pytest.mark.parametrize("origin", ["dairy", "egg", "fish", "shellfish"])
def test_origin_without_its_allergen_fails(origin: str) -> None:
    [problem] = problems(_food("x", "X", "X", origin=origin))
    assert problem.startswith(f"x: origin {origin} but no ")


def test_inherited_allergen_satisfies_origin() -> None:
    milk = _food("milk", "Milk", "Mleko", origin="dairy", allergens=["milk"])
    whey = _food("whey", "Whey", "Serwatka", origin="dairy", derived_from=["milk"])
    assert problems(milk, whey) == []


@pytest.mark.parametrize(
    ("en", "pl", "allergen"),
    [
        ("Wheat flour", "Mąka", "gluten"),
        ("Pasta", "Makaron pszenny", "gluten"),
        ("Rye bread", "Chleb", "gluten"),
        ("Rolled oats", "Płatki", "gluten"),
        ("Grain", "Płatki owsiane", "gluten"),
        ("Couscous", "Kuskus", "gluten"),
        ("Peanut butter", "Masło", "peanuts"),
        ("Snack", "Orzeszki ziemne", "peanuts"),
        ("Firm tofu", "Tofu", "soy"),
        ("Drink", "Napój sojowy", "soy"),
        ("Tahini", "Pasta", "sesame"),
        ("Seeds", "Sezam", "sesame"),
        ("Dijon mustard", "Musztarda", "mustard"),
        ("Celeriac", "Seler korzeniowy", "celery"),
        ("Almonds", "Migdały", "tree_nuts"),
        ("Nuts", "Orzechy włoskie", "tree_nuts"),
        ("Cashews", "Nerkowce", "tree_nuts"),
    ],
)
def test_name_naming_an_allergen_source_needs_that_allergen(
    en: str, pl: str, allergen: str
) -> None:
    [problem] = problems(_food("x", en, pl))
    assert problem.endswith(f"but no {allergen} allergen")
    assert problems(_food("x", en, pl, allergens=[allergen])) == []


def test_alias_counts_like_a_name() -> None:
    food = _food("x", "Pasta", "Makaron", aliases={"en": ["durum wheat pasta"]})
    assert problems(food) == ["x: name 'durum wheat pasta' says 'wheat' but no gluten allergen"]


@pytest.mark.parametrize(
    ("en", "pl"),
    [
        # not the allergen, although the word looks close
        ("Buckwheat groats", "Kasza gryczana"),
        ("Coconut milk", "Mleczko kokosowe"),
        ("Nutmeg", "Gałka muszkatołowa"),
        ("Eggplant", "Bakłażan"),
        # explicitly free from it
        ("Gluten-free rolled oats", "Płatki owsiane bezglutenowe"),
        ("Soy free spread", "Pasta bez soi"),
        ("Nut-free granola", "Granola"),
        ("Almond-flavour, nut free", "Ciastka"),
    ],
)
def test_no_false_alarms(en: str, pl: str) -> None:
    assert problems(_food("x", en, pl)) == []


def test_reports_one_problem_per_food_and_allergen() -> None:
    food = _food("x", "Wheat bread", "Chleb pszenny", aliases={"en": ["wheat loaf"]})
    assert len(problems(food)) == 1


def test_import_reports_contradictions_and_writes_nothing(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    raw = _food("cheese", "Cheese", "Ser", origin="dairy")
    raw["nutrition"] = {
        "kcal": 400,
        "protein_g": 25,
        "fat_g": 33,
        "carbs_g": 1,
        "fiber_g": 0,
        "source_ref": "test label",
    }
    report = importer.resolve(CuratedFile.model_validate({"foods": [raw]}), None)
    assert report.allergen_problems == ["cheese: origin dairy but no milk allergen"]
    assert "allergen contradictions" in report.summary()

    path = tmp_path / "curated.yaml"
    path.write_text(yaml.safe_dump({"foods": [raw]}), encoding="utf-8")
    # exits before opening a database session, with or without --dry-run
    assert cli.main(["foods", "import", "--curated", str(path)]) == 1
    assert "nothing written" in capsys.readouterr().err
