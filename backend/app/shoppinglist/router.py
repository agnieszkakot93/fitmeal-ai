"""The shopping list of a plan, and checking items off (PRD §8.10, Development Plan §10).

The list is rebuilt from the plan on every read, so it always matches the
plan's current recipes and portions; checkmarks are kept per food.
"""

from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.deps import CurrentUser
from app.auth.routing import HideInputRoute
from app.core.db import get_session
from app.shopping.aggregate import Lang, ShoppingItem, make_item
from app.shoppinglist import repository
from app.shoppinglist.models import ShoppingListItem
from app.shoppinglist.schemas import (
    AmountOut,
    PackageCountOut,
    PackagesOut,
    SectionOut,
    ShoppingItemCheckIn,
    ShoppingItemOut,
    ShoppingListOut,
)

router = APIRouter(tags=["shopping"], route_class=HideInputRoute)

Session = Annotated[AsyncSession, Depends(get_session)]
LangParam = Annotated[
    Lang | None, Query(description="Language of the item names; overrides Accept-Language")
]
AcceptLanguage = Annotated[str | None, Header()]

LANGS: tuple[Lang, ...] = ("en", "pl")


def pick_lang(lang: Lang | None, accept_language: str | None) -> Lang:
    """``lang`` if given, else the first of en/pl in Accept-Language by preference, else en."""
    if lang is not None:
        return lang
    ranked: list[tuple[float, int, Lang]] = []
    for i, part in enumerate((accept_language or "").split(",")):
        tag, _, params = part.strip().partition(";")
        primary = tag.strip().split("-")[0].lower()
        q = 1.0
        for p in params.split(";"):
            key, _, value = p.strip().partition("=")
            if key == "q":
                try:
                    q = float(value)
                except ValueError:
                    q = 0.0
        for code in LANGS:
            if primary == code and q > 0:
                ranked.append((-q, i, code))
    return min(ranked)[2] if ranked else "en"


def _item_out(item: ShoppingItem, row: ShoppingListItem) -> ShoppingItemOut:
    packages = item.packages
    return ShoppingItemOut(
        id=row.id,
        food_slug=item.food,
        name=item.name,
        category=item.category,
        grams=item.grams,
        amount=AmountOut(value=item.amount.value, unit=item.amount.unit),
        packages=None
        if packages is None
        else PackagesOut(
            buy=[PackageCountOut(size_g=p.size_g, count=p.count) for p in packages.buy],
            count=packages.count,
            total_g=packages.total_g,
            leftover_g=packages.leftover_g,
        ),
        checked=row.checked,
        checked_updated_at=row.checked_updated_at,
    )


@router.get("/v1/plans/{plan_id}/shopping-list", response_model=ShoppingListOut)
async def shopping_list(
    plan_id: uuid.UUID,
    user: CurrentUser,
    session: Session,
    lang: LangParam = None,
    accept_language: AcceptLanguage = None,
) -> ShoppingListOut:
    """The plan's shopping list by store section, with checkmarks.

    Regenerated from the plan each time: foods still on it keep their id and
    checkmark, foods no longer needed drop off.
    """
    plan = await repository.owned_plan(session, user.id, plan_id)
    if plan is None:
        # another user's plan looks the same as a missing one
        raise HTTPException(status.HTTP_404_NOT_FOUND, "plan not found")
    chosen = pick_lang(lang, accept_language)
    shopping, rows = await repository.sync(session, plan, chosen)
    await session.commit()
    return ShoppingListOut(
        plan_id=plan_id,
        lang=chosen,
        sections=[
            SectionOut(category=s.category, items=[_item_out(i, rows[i.food]) for i in s.items])
            for s in shopping.sections
        ],
    )


@router.patch("/v1/shopping-items/{item_id}", response_model=ShoppingItemOut)
async def check_item(
    item_id: uuid.UUID,
    body: ShoppingItemCheckIn,
    user: CurrentUser,
    session: Session,
    lang: LangParam = None,
    accept_language: AcceptLanguage = None,
) -> ShoppingItemOut:
    """Check or uncheck an item.

    Idempotent per ``event_id``: replaying an event (an offline outbox retrying)
    returns the item unchanged. Reusing an event id for a different change is a 409.
    """
    row = await repository.owned_item(session, user.id, item_id)
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "item not found")
    try:
        await repository.record_check(session, row, body.event_id, body.checked)
    except repository.EventConflict:
        await session.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT, "event id already used for a different change"
        ) from None
    item = make_item(repository.to_facts(row.food), row.grams, pick_lang(lang, accept_language))
    await session.commit()
    return _item_out(item, row)
