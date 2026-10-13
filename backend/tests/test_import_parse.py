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


@pytest.mark.parametrize(
    ("raw", "amount", "unit", "name"),
    [
        ("1 garlic clove, crushed", 1, "clove", "garlic"),
        ("3 garlic cloves", 3, "clove", "garlic"),
        ("2 celery stalks", 2, "stalk", "celery"),
        ("1 ½ cups blueberries", 1.5, "cup", "blueberries"),
        ("a handful of blueberries", 1, "handful", "blueberries"),
        ("pół kilo ziemniaków", 0.5, "kg", "ziemniaków"),
        ("pomidorki koktajlowe, garść", 1, "handful", "pomidorki koktajlowe"),
        ("½ kostki masła (100 g)", 0.5, "pack", "masła"),
        ("1 tsp coconut oil for the pan", 1, "tsp", "coconut oil"),
        ("1 head romaine lettuce", 1, "piece", "romaine lettuce"),
    ],
)
def test_units_written_around_the_name(raw: str, amount: float, unit: str, name: str) -> None:
    parsed = parse_line(raw)
    assert parsed.amount == pytest.approx(amount)
    assert (parsed.unit, parsed.name) == (unit, name)


@pytest.mark.parametrize(
    ("raw", "weight_g"),
    [
        ("2 cukinie (ok. 600 g)", 600),
        ("1 can (28 oz) crushed tomatoes", 793.786),
        ("1 opakowanie tofu naturalnego (180 g)", 180),
        ("2 fillets (150 g each)", 300),
        ("1 can (400 g) chickpeas, drained", None),  # the can's weight includes the liquid
        ("2 jajka (rozmiar M)", None),
        ("3 eggs", None),
    ],
)
def test_weight_stated_in_a_note(raw: str, weight_g: float | None) -> None:
    got = parse_line(raw).weight_g
    assert got == (pytest.approx(weight_g, rel=1e-4) if weight_g is not None else None)


@pytest.mark.parametrize(
    ("raw", "several"),
    [
        ("sól, pieprz", True),
        ("sól, pieprz do smaku", True),
        ("fresh basil, chopped", False),
        ("parmesan, for serving", False),
        ("2 ząbki czosnku, posiekane", False),
    ],
)
def test_comma_list_without_amount(raw: str, several: bool) -> None:
    assert parse_line(raw).several is several
