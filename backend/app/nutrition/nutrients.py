"""Nutrient values and the arithmetic on them.

Conventions used everywhere in the engine:

* Values are stored **per 100 g** of the food as sold/weighed (raw unless the
  food item says otherwise).
* ``carbs_g`` means *available* carbohydrate as printed on EU labels
  ("węglowodany"), i.e. **excluding fiber**. USDA data reports carbohydrate
  "by difference", which includes fiber; the FDC importer subtracts fiber.
"""

from __future__ import annotations

from dataclasses import dataclass, fields

# Atwater factors (kcal per gram) used for the sanity check only; the kcal
# value itself always comes from the source database.
KCAL_PER_G_PROTEIN = 4.0
KCAL_PER_G_CARBS = 4.0
KCAL_PER_G_FAT = 9.0
KCAL_PER_G_FIBER = 2.0


@dataclass(frozen=True, slots=True)
class Nutrients:
    kcal: float = 0.0
    protein_g: float = 0.0
    fat_g: float = 0.0
    carbs_g: float = 0.0
    fiber_g: float = 0.0

    def __add__(self, other: Nutrients) -> Nutrients:
        return Nutrients(
            **{f.name: getattr(self, f.name) + getattr(other, f.name) for f in fields(self)}
        )

    def scale(self, factor: float) -> Nutrients:
        return Nutrients(**{f.name: getattr(self, f.name) * factor for f in fields(self)})

    def rounded(self) -> Nutrients:
        """Rounding for display: whole kcal, one decimal for grams."""
        return Nutrients(
            kcal=round(self.kcal),
            protein_g=round(self.protein_g, 1),
            fat_g=round(self.fat_g, 1),
            carbs_g=round(self.carbs_g, 1),
            fiber_g=round(self.fiber_g, 1),
        )

    @staticmethod
    def total(items: list[Nutrients]) -> Nutrients:
        result = Nutrients()
        for item in items:
            result = result + item
        return result


def for_grams(per_100g: Nutrients, grams: float) -> Nutrients:
    if grams < 0:
        raise ValueError("grams must be non-negative")
    return per_100g.scale(grams / 100.0)


def atwater_kcal(n: Nutrients) -> float:
    return (
        n.protein_g * KCAL_PER_G_PROTEIN
        + n.carbs_g * KCAL_PER_G_CARBS
        + n.fat_g * KCAL_PER_G_FAT
        + n.fiber_g * KCAL_PER_G_FIBER
    )


def energy_is_consistent(n: Nutrients, tolerance: float = 0.15, slack_kcal: float = 15.0) -> bool:
    """True when the stated kcal roughly matches the macros.

    Catches unit mix-ups (kJ vs kcal) and data-entry errors. Alcohol, polyols
    and organic acids are not modelled, so the tolerance is deliberately loose.
    """
    expected = atwater_kcal(n)
    return abs(n.kcal - expected) <= max(slack_kcal, tolerance * max(n.kcal, expected))
