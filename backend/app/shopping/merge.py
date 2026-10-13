"""Tick items and keep ticks when a shopping list is regenerated (PRD §8.10)."""

from __future__ import annotations

import dataclasses
from collections.abc import Mapping

from app.shopping.aggregate import Section, ShoppingList


def _with_bought(lst: ShoppingList, bought: Mapping[str, int]) -> ShoppingList:
    return ShoppingList(
        tuple(
            Section(
                s.category,
                tuple(dataclasses.replace(i, checked_g=bought.get(i.food, 0)) for i in s.items),
            )
            for s in lst.sections
        )
    )


def _bought(lst: ShoppingList) -> dict[str, int]:
    return {i.food: i.checked_g for i in lst.items if i.checked_g}


def check(lst: ShoppingList, food: str) -> ShoppingList:
    """Tick an item: everything it needs now counts as bought."""
    item = next((i for i in lst.items if i.food == food), None)
    if item is None:
        raise KeyError(food)
    bought = _bought(lst)
    bought[food] = max(item.checked_g, item.grams)
    return _with_bought(lst, bought)


def uncheck(lst: ShoppingList, food: str) -> ShoppingList:
    bought = _bought(lst)
    bought.pop(food, None)
    return _with_bought(lst, bought)


def merge(previous: ShoppingList, new: ShoppingList) -> ShoppingList:
    """``new`` with what was already bought on ``previous``, matched by food key.

    A ticked item whose need grew comes back unticked with ``still_to_buy_g``
    holding only the extra; one whose need shrank stays ticked. Foods no longer
    in the plan drop out.
    """
    return _with_bought(new, _bought(previous))
