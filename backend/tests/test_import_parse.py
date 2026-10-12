import pytest

from app.imports.parse import parse_line


@pytest.mark.parametrize(
    ("raw", "amount", "unit", "name", "note", "optional"),
    [
        ("2 ząbki czosnku, posiekane", 2, "clove", "czosnku", "posiekane", False),
        ("200g piersi z kurczaka", 200, "g", "piersi z kurczaka", None, False),
        ("1½ cups rolled oats", 1.5, "cup", "rolled oats", None, False),
        ("1 1/2 szklanki mleka", 1.5, "szklanka", "mleka", None, False),
        ("2-3 łyżki oliwy", 2.5, "tbsp", "oliwy", None, False),
        ("2,5 dkg masła", 2.5, "dag", "masła", None, False),
        ("szczypta soli", 1, "pinch", "soli", None, False),
        ("sól do smaku", None, None, "sól", None, True),
        ("1 can (400 g) chopped tomatoes", 1, "can", "chopped tomatoes", "400 g", False),
        ("3 eggs", 3, None, "eggs", None, False),
        ("½ avocado", 0.5, None, "avocado", None, False),
        ("2 handfuls of spinach", 2, "handful", "spinach", None, False),
        ("- 1 tbsp olive oil", 1, "tbsp", "olive oil", None, False),
        ("fresh basil", None, None, "fresh basil", None, False),
    ],
)
def test_parse_line(
    raw: str, amount: float | None, unit: str | None, name: str, note: str | None, optional: bool
) -> None:
    parsed = parse_line(raw)
    assert parsed.amount == (pytest.approx(amount) if amount is not None else None)
    assert (parsed.unit, parsed.name, parsed.note, parsed.optional) == (unit, name, note, optional)


@pytest.mark.parametrize(
    ("raw", "several"),
    [
        ("sól i pieprz do smaku", True),
        ("salt and pepper", True),
        ("1 tbsp oil or butter", True),
        ("1 łyżka oliwy z oliwek", False),
        ("2 kromki chleba żytniego", False),
    ],
)
def test_several_ingredients_in_one_line(raw: str, several: bool) -> None:
    assert parse_line(raw).several is several
