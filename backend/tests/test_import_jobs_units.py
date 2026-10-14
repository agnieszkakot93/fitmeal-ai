"""Import job pieces without a database: text splitting and cache keys."""

from __future__ import annotations

import uuid

import pytest

from app.importjobs import cache
from app.importjobs.extract import from_page, servings_from, split_text
from app.imports.page import PageRecipe


def test_split_text_by_headers() -> None:
    draft = split_text(
        "Pancakes\nServes 4\n\nIngredients:\n- 2 eggs\n- salt\n"
        "Method\n1. Whisk everything.\n2) Fry."
    )
    assert draft.title == "Pancakes"
    assert draft.servings == 4
    assert draft.ingredients == ["2 eggs", "salt"]
    assert draft.instructions == ["Whisk everything.", "Fry."]
    assert draft.language == "en"


def test_split_text_without_headers() -> None:
    draft = split_text(
        "Placki bananowe\n2 jajka\n1 banan\nsól do smaku\n"
        "Rozgnieć banana widelcem i wymieszaj z jajkami, potem smaż na patelni.\n"
    )
    assert (draft.title, draft.servings, draft.language) == ("Placki bananowe", None, "pl")
    assert draft.ingredients == ["2 jajka", "1 banan", "sól do smaku"]
    assert draft.instructions == [
        "Rozgnieć banana widelcem i wymieszaj z jajkami, potem smaż na patelni."
    ]


def test_split_text_keeps_decimal_amounts() -> None:
    assert split_text("Ingredients\n2.5 kg flour").ingredients == ["2.5 kg flour"]


@pytest.mark.parametrize(
    ("value", "expected"),
    [("4", 4), ("2 porcje", 2), ("Serves 6", 6), ("0", None), ("500", None), (None, None)],
)
def test_servings_from(value: str | None, expected: int | None) -> None:
    assert servings_from(value) == expected


def test_from_page() -> None:
    page = PageRecipe("https://x.example/r", "Owsianka", ["1 banan"], ["Mix."], "2 porcje", "pl-PL")
    draft = from_page(page)
    assert (draft.title, draft.servings, draft.language) == ("Owsianka", 2, "pl")


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        ("HTTPS://Example.COM/Recipe?p=123#top", "https://example.com/Recipe?p=123"),
        ("https://example.com:443/a?utm_source=x&id=7&UTM_medium=y", "https://example.com/a?id=7"),
        ("http://example.com", "http://example.com/"),
        ("https://example.com:8443/a", "https://example.com:8443/a"),
    ],
)
def test_normalise_url(url: str, expected: str) -> None:
    assert cache.normalise_url(url) == expected


def test_link_key_ignores_noise_but_not_the_query() -> None:
    key = cache.link_key("https://example.com/r?p=1")
    assert cache.link_key("https://EXAMPLE.com/r?p=1&utm_campaign=z#x") == key
    assert cache.link_key("https://example.com/r?p=2") != key
    assert cache.link_key("https://example.com/R?p=1") != key


def test_text_key_is_per_user_and_keyed() -> None:
    a, b = uuid.uuid4(), uuid.uuid4()
    key = cache.text_key(a, "2 eggs\n1 banana")
    assert cache.text_key(a, "  2 eggs \n\n1   banana\n") == key
    assert cache.text_key(b, "2 eggs\n1 banana") != key
    assert key.startswith("text:")
    # not a plain hash of the content: a leaked key says nothing about the text
    assert "2 eggs" not in key
