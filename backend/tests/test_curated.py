"""Safety checks on the real curated ingredient file, and its schema rules."""

import datetime
import re
from pathlib import Path

import pytest
from pydantic import ValidationError

from app.foods.curated import (
    CuratedFile,
    ReviewStatus,
    TraceSourceType,
    load_curated,
)
from app.foods.lint import allergen_problems
from app.nutrition.allergens import Allergen, TraceStatus, effective_allergens, effective_traces

ROOT = Path(__file__).resolve().parents[2]
CURATED = ROOT / "data" / "foods" / "curated.yaml"
TRACE_POLICY = ROOT / "docs" / "data" / "TRACE_POLICY.md"


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


def test_real_file_has_no_allergen_contradictions(curated: CuratedFile) -> None:
    assert allergen_problems(curated) == []


def test_real_file_states_provenance_on_every_entry(curated: CuratedFile) -> None:
    implicit = [f.slug for f in curated.foods if not {"review", "traces"} <= f.model_fields_set]
    assert implicit == []


def test_real_file_policy_traces_cite_a_rule_of_the_policy(curated: CuratedFile) -> None:
    policy = TRACE_POLICY.read_text(encoding="utf-8")
    rules = set(re.findall(r"^\| `([a-z0-9-]+)` \|", policy, re.M))
    refs = {
        f.slug: f.traces.source.ref
        for f in curated.foods
        if f.traces.source is not None and f.traces.source.type is TraceSourceType.POLICY
    }
    assert refs, "no entry applies the trace policy"
    unknown = {
        slug: ref for slug, ref in refs.items() if ref.removeprefix("TRACE_POLICY.md#") not in rules
    }
    assert unknown == {}


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


LABEL = {"type": "label", "ref": "Brand X granola, 2026-09 pack"}
POLICY = {"type": "policy", "ref": "TRACE_POLICY.md#seeds"}
DECLARED = {"status": "declared", "source": LABEL}


def test_provenance_defaults_to_draft_and_unknown_traces() -> None:
    food = CuratedFile.model_validate({"foods": [_food()]}).foods[0]
    assert food.may_contain == []
    assert food.traces.status is TraceStatus.UNKNOWN
    assert food.traces.source is None
    assert food.review.status is ReviewStatus.DRAFT


def test_may_contain_loads_separately_from_allergens() -> None:
    raw = _food(allergens=["gluten"], may_contain=["tree_nuts", "peanuts"], traces=DECLARED)
    food = CuratedFile.model_validate({"foods": [raw]}).foods[0]
    assert food.allergens == [Allergen.GLUTEN]
    assert food.may_contain == [Allergen.TREE_NUTS, Allergen.PEANUTS]
    assert food.traces.status is TraceStatus.DECLARED
    assert food.traces.source is not None
    assert food.traces.source.type is TraceSourceType.LABEL


@pytest.mark.parametrize(
    "extra",
    [
        {"allergens": ["gluten"], "may_contain": ["gluten"], "traces": DECLARED},
        {"may_contain": ["walnuts"], "traces": DECLARED},
    ],
)
def test_rejects_bad_may_contain(extra: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        CuratedFile.model_validate({"foods": [_food(**extra)]})


@pytest.mark.parametrize(
    "extra",
    [
        {"traces": {"status": "unknown"}},
        {"traces": {"status": "none_declared", "source": LABEL}},
        {"traces": {"status": "none_declared", "source": POLICY}},
        {"traces": {"status": "declared", "source": POLICY}, "may_contain": ["peanuts"]},
    ],
)
def test_accepts_valid_trace_provenance(extra: dict[str, object]) -> None:
    CuratedFile.model_validate({"foods": [_food(**extra)]})


@pytest.mark.parametrize(
    "extra",
    [
        # declared needs a source and at least one trace
        {"traces": {"status": "declared"}, "may_contain": ["peanuts"]},
        {"traces": DECLARED},
        # none declared needs a source and no traces
        {"traces": {"status": "none_declared"}},
        {"traces": {"status": "none_declared", "source": LABEL}, "may_contain": ["peanuts"]},
        # unknown means unknown: no traces, no source
        {"may_contain": ["peanuts"]},
        {"traces": {"status": "unknown"}, "may_contain": ["peanuts"]},
        {"traces": {"status": "unknown", "source": LABEL}},
        # malformed source
        {"traces": {"status": "none_declared", "source": {"type": "llm", "ref": "x"}}},
        {"traces": {"status": "none_declared", "source": {"type": "label", "ref": ""}}},
        {"traces": {"status": "none_declared", "source": {"type": "label"}}},
        {"traces": {"status": "maybe"}},
    ],
)
def test_rejects_invalid_trace_provenance(extra: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        CuratedFile.model_validate({"foods": [_food(**extra)]})


@pytest.mark.parametrize(
    "review",
    [
        {"status": "draft"},
        {"status": "auto_checked"},
        {"status": "auto_checked", "by": "CI", "date": "2026-09-24"},
        {"status": "verified", "by": "AK", "date": "2026-09-24"},
    ],
)
def test_accepts_valid_review(review: dict[str, object]) -> None:
    CuratedFile.model_validate({"foods": [_food(review=review)]})


def test_verified_review_loads_initials_and_date() -> None:
    raw = _food(review={"status": "verified", "by": "AK", "date": "2026-09-24"})
    review = CuratedFile.model_validate({"foods": [raw]}).foods[0].review
    assert review.status is ReviewStatus.VERIFIED
    assert review.by == "AK"
    assert review.date == datetime.date(2026, 9, 24)


@pytest.mark.parametrize(
    "review",
    [
        {"status": "verified"},
        {"status": "verified", "by": "AK"},
        {"status": "verified", "date": "2026-09-24"},
        {"status": "verified", "by": "claude", "date": "2026-09-24"},
        {"status": "verified", "by": "", "date": "2026-09-24"},
        {"status": "verified", "by": "AK", "date": "24.09.2026"},
        {"status": "approved"},
    ],
)
def test_rejects_invalid_review(review: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        CuratedFile.model_validate({"foods": [_food(review=review)]})


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
