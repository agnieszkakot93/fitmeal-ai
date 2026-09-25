"""Allergen lint for the curated list: clear contradictions only.

Two kinds of rule, both checked against a food's *effective* allergens (own +
inherited through ``derived_from``):

* origin: a dairy food must contain milk, an egg food eggs, a fish food fish, a
  shellfish food crustaceans or molluscs;
* name: a food whose name or alias names a source of an allergen ("wheat",
  "tahini", "pszenne", "orzeszki ziemne", "grana padano" ...) must contain it.

Name rules only list words that always mean the allergen. Ambiguous words
("milk" in almond milk, "butter" in peanut butter, "orzech" on its own) are
left out on purpose: a false alarm here would teach people to ignore the lint.
A food that calls itself free from an allergen anywhere in its names
("gluten-free oats", "płatki owsiane bezglutenowe") is exempt from that
allergen's name rule.
"""

from __future__ import annotations

import re

from app.core.text import fold
from app.foods.curated import CuratedFile, CuratedFood
from app.nutrition.allergens import Allergen, Origin, effective_allergens

ORIGIN_ALLERGENS: dict[Origin, frozenset[Allergen]] = {
    Origin.DAIRY: frozenset({Allergen.MILK}),
    Origin.EGG: frozenset({Allergen.EGGS}),
    Origin.FISH: frozenset({Allergen.FISH}),
    Origin.SHELLFISH: frozenset({Allergen.CRUSTACEANS, Allergen.MOLLUSCS}),
}


def _words(*patterns: str) -> re.Pattern[str]:
    return re.compile(r"\b(?:" + "|".join(patterns) + r")\b")


# Matched against folded (lowercase, no diacritics) names and aliases, EN + PL.
# `\b` before each word keeps "buckwheat" (gluten-free) out of "wheat".
NAME_ALLERGENS: dict[Allergen, re.Pattern[str]] = {
    Allergen.GLUTEN: _words(
        r"wheat",
        r"barley",
        r"rye",
        r"spelt",
        r"oats?",
        r"oatmeal",
        r"semolina",
        r"couscous",
        r"bulgur",
        r"pszen\w*",
        r"jeczmie\w*",
        r"zyt\w*",
        r"orkisz\w*",
        r"owies",
        r"owsian\w*",
        r"kuskus",
        r"kasza manna",
    ),
    Allergen.PEANUTS: _words(r"peanuts?", r"orzesz\w* ziemn\w*", r"arachid\w*"),
    # Grana Padano is normally made with lysozyme from egg ("lizozym z jaja").
    Allergen.EGGS: _words(r"grana padano"),
    Allergen.SOY: _words(r"soy", r"soya", r"soybeans?", r"tofu", r"tempeh", r"edamame", r"soj\w*"),
    Allergen.SESAME: _words(r"sesame", r"tahini", r"sezam\w*"),
    Allergen.MUSTARD: _words(r"mustard", r"musztard\w*", r"gorczyc\w*"),
    Allergen.CELERY: _words(r"celery", r"celeriac", r"seler\w*"),
    Allergen.TREE_NUTS: _words(
        r"almonds?",
        r"walnuts?",
        r"hazelnuts?",
        r"cashews?",
        r"pistachios?",
        r"pecans?",
        r"macadamias?",
        r"brazil nuts?",
        r"migdal\w*",
        r"orzech\w* wlosk\w*",
        r"orzech\w* laskow\w*",
        r"nerkowc\w*",
        r"nerkowiec",
        r"pistacj\w*",
        r"pekan\w*",
    ),
}

FREE_FROM: dict[Allergen, re.Pattern[str]] = {
    Allergen.GLUTEN: _words(r"gluten[- ]free", r"bezglutenow\w*", r"bez glutenu"),
    Allergen.PEANUTS: _words(r"peanut[- ]free", r"bez orzeszkow ziemnych"),
    Allergen.EGGS: _words(r"egg[- ]free", r"lysozyme[- ]free", r"bez jaj", r"bez lizozymu"),
    Allergen.SOY: _words(r"soy[- ]free", r"bez soi"),
    Allergen.SESAME: _words(r"sesame[- ]free", r"bez sezamu"),
    Allergen.MUSTARD: _words(r"mustard[- ]free", r"bez gorczycy", r"bez musztardy"),
    Allergen.CELERY: _words(r"celery[- ]free", r"bez selera"),
    Allergen.TREE_NUTS: _words(r"(?:tree )?nut[- ]free", r"bez orzechow"),
}


def allergen_problems(curated: CuratedFile) -> list[str]:
    """Every clear origin/name vs allergen contradiction in the file."""
    effective = effective_allergens(
        {f.slug: f.allergens for f in curated.foods},
        {f.slug: f.derived_from for f in curated.foods},
    )
    problems: list[str] = []
    for food in curated.foods:
        problems.extend(food_problems(food, effective[food.slug]))
    return problems


def food_problems(food: CuratedFood, contains: frozenset[Allergen]) -> list[str]:
    """Contradictions for one food, given its effective allergens."""
    problems = []
    expected = ORIGIN_ALLERGENS.get(food.origin)
    if expected and not expected & contains:
        wanted = " or ".join(sorted(a.value for a in expected))
        problems.append(f"{food.slug}: origin {food.origin.value} but no {wanted} allergen")
    names = _names(food)
    for allergen, pattern in NAME_ALLERGENS.items():
        if allergen in contains or any(FREE_FROM[allergen].search(n) for n in names):
            continue
        match = next((m for m in map(pattern.search, names) if m), None)
        if match:
            problems.append(
                f"{food.slug}: name {match.string!r} says {match.group(0)!r} "
                f"but no {allergen.value} allergen"
            )
    return problems


def _names(food: CuratedFood) -> list[str]:
    return [fold(n) for n in (food.name.en, food.name.pl, *food.aliases.en, *food.aliases.pl)]
