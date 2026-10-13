"""Consent history, data export and account erasure."""

from __future__ import annotations

import uuid
from collections.abc import Sequence
from datetime import UTC, datetime
from typing import Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy import delete, exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.auth.models import RefreshToken
from app.core.db import Base
from app.plans.models import MealPlan, PlanSlot, SlotEvent
from app.recipes.models import Recipe, RecipeSource, RecipeVariant
from app.users.models import ConsentRecord, User
from app.users.schemas import ConsentIn, ConsentOut, ExportOut, MeOut, SessionOut


async def consent_history(session: AsyncSession, user_id: uuid.UUID) -> Sequence[ConsentRecord]:
    stmt = (
        select(ConsentRecord)
        .where(ConsentRecord.user_id == user_id)
        .order_by(ConsentRecord.recorded_at, ConsentRecord.id)
    )
    return (await session.scalars(stmt)).all()


async def current_consents(session: AsyncSession, user_id: uuid.UUID) -> list[ConsentOut]:
    latest: dict[str, ConsentRecord] = {}
    for record in await consent_history(session, user_id):
        latest[record.type] = record
    return [ConsentOut.model_validate(r) for r in latest.values()]


async def add_consents(
    session: AsyncSession, user_id: uuid.UUID, consents: list[ConsentIn]
) -> None:
    # one timestamp for one screen's answers; never an UPDATE (append-only)
    now = datetime.now(UTC)
    session.add_all(
        ConsentRecord(
            user_id=user_id,
            type=c.type.value,
            version=c.version,
            granted=c.granted,
            recorded_at=now,
        )
        for c in consents
    )


async def me(session: AsyncSession, user: User) -> MeOut:
    return MeOut(
        id=user.id,
        created_at=user.created_at,
        email_relay=user.email_relay,
        consents=await current_consents(session, user.id),
    )


def _columns(row: Base) -> dict[str, Any]:
    return {c.key: jsonable_encoder(getattr(row, c.key)) for c in row.__mapper__.column_attrs}


async def export(session: AsyncSession, user: User) -> ExportOut:
    history = await consent_history(session, user.id)
    sessions = (
        await session.scalars(
            select(RefreshToken)
            .where(RefreshToken.user_id == user.id)
            .order_by(RefreshToken.created_at)
        )
    ).all()
    recipes = (
        await session.scalars(
            select(Recipe)
            .where(Recipe.owner_user_id == user.id)
            .options(selectinload(Recipe.ingredients))
            .order_by(Recipe.created_at)
        )
    ).all()
    sources = {
        s.id: s
        for s in await session.scalars(
            select(RecipeSource).where(RecipeSource.id.in_([r.source_id for r in recipes]))
        )
    }
    variants = (
        await session.scalars(
            select(RecipeVariant)
            .where(RecipeVariant.user_id == user.id)
            .order_by(RecipeVariant.created_at)
        )
    ).all()
    plans = (
        await session.scalars(
            select(MealPlan)
            .where(MealPlan.user_id == user.id)
            .options(selectinload(MealPlan.slots))
            .order_by(MealPlan.created_at)
        )
    ).all()
    events: dict[int, list[SlotEvent]] = {}
    for event in await session.scalars(
        select(SlotEvent)
        .join(PlanSlot)
        .join(MealPlan)
        .where(MealPlan.user_id == user.id)
        .order_by(SlotEvent.received_at, SlotEvent.id)
    ):
        events.setdefault(event.slot_id, []).append(event)
    return ExportOut(
        exported_at=datetime.now(UTC),
        user=await me(session, user),
        consent_history=[ConsentOut.model_validate(r) for r in history],
        sessions=[SessionOut.model_validate(t) for t in sessions],
        private_recipes=[
            {
                **_columns(r),
                "source": _columns(sources[r.source_id]),
                "ingredients": [_columns(i) for i in r.ingredients],
            }
            for r in recipes
        ],
        recipe_variants=[_columns(v) for v in variants],
        plans=[
            {
                **_columns(p),
                "slots": [
                    {**_columns(slot), "events": [_columns(e) for e in events.get(slot.id, [])]}
                    for slot in p.slots
                ],
            }
            for p in plans
        ],
    )


async def erase(session: AsyncSession, user_id: uuid.UUID) -> None:
    """Delete the account and everything stored about it (GDPR Art. 17).

    Recipes and variants point at users without a foreign key (they predate
    this table), so they are deleted here explicitly. Refresh tokens, consent
    records and plans (with their slots and events) go with the user row
    (ON DELETE CASCADE).
    """
    source_ids = (
        await session.scalars(select(Recipe.source_id).where(Recipe.owner_user_id == user_id))
    ).all()
    await session.execute(delete(RecipeVariant).where(RecipeVariant.user_id == user_id))
    # cascades to the recipes' ingredients and any variants built on them
    await session.execute(delete(Recipe).where(Recipe.owner_user_id == user_id))
    if source_ids:
        await session.execute(
            delete(RecipeSource).where(
                RecipeSource.id.in_(source_ids),
                RecipeSource.type != "catalog",
                ~exists().where(Recipe.source_id == RecipeSource.id),
            )
        )
    await session.execute(delete(User).where(User.id == user_id))
