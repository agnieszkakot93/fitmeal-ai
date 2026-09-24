from enum import StrEnum


class FoodCategory(StrEnum):
    """Also the shopping-list sections, in store-walk order."""

    VEGETABLES = "vegetables"
    FRUIT = "fruit"
    MEAT_FISH = "meat_fish"
    DAIRY_EGGS = "dairy_eggs"
    BAKERY = "bakery"
    GRAINS_PASTA = "grains_pasta"
    LEGUMES = "legumes"
    NUTS_SEEDS = "nuts_seeds"
    OILS_FATS = "oils_fats"
    CONDIMENTS = "condiments"
    SPICES = "spices"
    SWEETS_BAKING = "sweets_baking"
    BEVERAGES = "beverages"
    OTHER = "other"


class CulinaryRole(StrEnum):
    """What an ingredient does in a dish; bounds how the optimizer may change it."""

    MAIN_PROTEIN = "main_protein"
    CARB_BASE = "carb_base"
    VEGETABLE = "vegetable"
    AROMATIC = "aromatic"
    FRUIT = "fruit"
    COOKING_FAT = "cooking_fat"
    CREAMY_BASE = "creamy_base"
    CHEESE = "cheese"
    BINDER = "binder"
    SAUCE_BASE = "sauce_base"
    SEASONING = "seasoning"
    SWEETENER = "sweetener"
    LIQUID = "liquid"
    TOPPING = "topping"
    LEAVENING = "leavening"
    ACID = "acid"
