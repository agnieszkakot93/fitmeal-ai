import pytest

from app.imports.words import is_descriptor, same_word, tokens


@pytest.mark.parametrize(
    ("a", "b"),
    [
        ("oliwy", "oliwa"),
        ("mąki", "mąka"),
        ("pszennej", "pszenna"),
        ("cukru", "cukier"),
        ("czosnku", "czosnek"),
        ("oliwek", "oliwki"),
        ("soli", "sól"),
        ("słodkiej", "słodka"),
        ("żółtego", "żółty"),
        ("sera", "ser"),
        ("maslo", "masło"),  # typed without diacritics
        ("tomatoes", "tomato"),
        ("blueberries", "blueberry"),
    ],
)
def test_inflected_forms_are_the_same_word(a: str, b: str) -> None:
    assert same_word(a, b)


@pytest.mark.parametrize(
    ("a", "b"),
    [
        ("mąki", "mak"),  # flour is not poppy seed
        ("masła", "maślanka"),  # butter is not buttermilk
        ("oliwek", "oliwa"),  # olives are not olive oil
        ("pomidorki", "pomidory"),
        ("oil", "seeds"),
    ],
)
def test_different_words_stay_apart(a: str, b: str) -> None:
    assert not same_word(a, b)


@pytest.mark.parametrize(
    ("word", "descriptor"),
    [
        ("ciepłego", True),
        ("mrożonych", True),
        ("młodych", True),
        ("gazowanej", True),
        ("shredded", True),
        ("frozen", True),
        ("mleka", False),
        ("malin", False),
        ("2%", False),
    ],
)
def test_descriptors(word: str, descriptor: bool) -> None:
    assert is_descriptor(word) is descriptor


def test_tokens_drop_fillers() -> None:
    assert tokens("filet z łososia") == ["filet", "łososia"]
