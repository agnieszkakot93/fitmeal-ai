"""Import job storage: quota, owner-scoped reads, confirm into a private recipe."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta

from sqlalchemy import delete, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.foods import repository as foods_repo
from app.importjobs.config import get_import_settings
from app.importjobs.models import ImportJob, ImportOrigin, ImportStatus, ImportType
from app.importjobs.schemas import (
    AnswerIn,
    ClarificationKind,
    ConfirmIn,
    PreviewLine,
    PreviewOut,
)
from app.imports.match import _grams as grams_for
from app.imports.parse import ParsedLine
from app.recipes import repository as recipes_repo
from app.recipes.models import Recipe, RecipeIngredient, RecipeSource, SourceType
from app.users.models import User


class QuotaExceeded(Exception):
    pass


async def create(
    session: AsyncSession,
    user_id: uuid.UUID,
    type_: ImportType,
    origin: ImportOrigin,
    url: str | None,
    text: str | None,
) -> ImportJob:
    """A queued job, counted against the quota now, not when it finishes (§7.7).

    Locking the user row serialises one user's submissions, so two parallel
    requests can't both take the last unit of quota.
    """
    settings = get_import_settings()
    await session.execute(select(User.id).where(User.id == user_id).with_for_update())
    since = datetime.now(UTC) - timedelta(days=1)
    used = await session.scalar(
        select(func.count())
        .select_from(ImportJob)
        .where(ImportJob.user_id == user_id, ImportJob.created_at > since)
    )
    if (used or 0) >= settings.import_daily_quota:
        raise QuotaExceeded
    job = ImportJob(
        user_id=user_id,
        type=type_.value,
        origin=origin.value,
        status=ImportStatus.QUEUED.value,
        source_url=url,
        input_text=text,
        expires_at=datetime.now(UTC) + timedelta(days=settings.import_preview_ttl_days),
    )
    session.add(job)
    await session.flush()
    return job


async def get_owned(
    session: AsyncSession, user_id: uuid.UUID, import_id: uuid.UUID, *, lock: bool = False
) -> ImportJob | None:
    """Every read is filtered by owner (§7.7); an expired preview reads as missing."""
    stmt = select(ImportJob).where(
        ImportJob.id == import_id,
        ImportJob.user_id == user_id,
        or_(
            ImportJob.status == ImportStatus.CONFIRMED.value,
            ImportJob.expires_at > datetime.now(UTC),
        ),
    )
    if lock:
        stmt = stmt.with_for_update()
    return await session.scalar(stmt)


async def claim(session: AsyncSession, import_id: uuid.UUID, retry: bool) -> ImportJob | None:
    """Move a queued job to running; None if another run has it or it's gone.

    ``retry``: arq is running the job again after a worker died mid-run.
    """
    statuses = [ImportStatus.QUEUED.value] + ([ImportStatus.RUNNING.value] if retry else [])
    claimed = await session.scalar(
        update(ImportJob)
        .where(ImportJob.id == import_id, ImportJob.status.in_(statuses))
        .values(status=ImportStatus.RUNNING.value)
        .returning(ImportJob.id)
    )
    await session.commit()
    return await session.get(ImportJob, claimed) if claimed else None


async def purge_expired(session: AsyncSession) -> int:
    """Delete unconfirmed jobs past their expiry, with their previews."""
    result = await session.execute(
        delete(ImportJob).where(
            ImportJob.status != ImportStatus.CONFIRMED.value,
            ImportJob.expires_at <= datetime.now(UTC),
        )
    )
    return int(getattr(result, "rowcount", 0) or 0)


# --- confirm -----------------------------------------------------------------


class Unanswered(Exception):
    def __init__(self, positions: list[int], missing: list[ClarificationKind]) -> None:
        super().__init__("unanswered clarifications")
        self.positions = positions
        self.missing = missing


class BadAnswer(Exception):
    def __init__(self, detail: str) -> None:
        super().__init__(detail)
        self.detail = detail


_SOURCE_TYPES = {
    (ImportType.LINK, ImportOrigin.PASTE): SourceType.LINK,
    (ImportType.LINK, ImportOrigin.SHARE): SourceType.LINK,
    (ImportType.TEXT, ImportOrigin.PASTE): SourceType.TEXT,
    (ImportType.TEXT, ImportOrigin.SHARE): SourceType.TEXT,
    (ImportType.TEXT, ImportOrigin.PDF): SourceType.PDF,
}


def _parsed(line: PreviewLine) -> ParsedLine:
    return ParsedLine(
        raw=line.raw,
        amount=line.amount,
        unit=line.unit,
        name=line.name,
        note=line.note,
        optional=line.optional,
        weight_g=line.weight_g,
    )


def _check_answers(preview: PreviewOut, body: ConfirmIn) -> dict[int, AnswerIn]:
    answers = {a.position: a for a in body.answers}
    positions = {line.position for line in preview.ingredients}
    if len(answers) != len(body.answers) or not answers.keys() <= positions:
        raise BadAnswer("answers must name each ingredient line at most once")
    unanswered = [
        line.position
        for line in preview.ingredients
        if line.needs_clarification and line.position not in answers
    ]
    missing = []
    if (body.servings or preview.servings) is None:
        missing.append(ClarificationKind.SERVINGS)
    if not (body.title or preview.title):
        missing.append(ClarificationKind.TITLE)
    if unanswered or missing:
        raise Unanswered(unanswered, missing)
    return answers


async def confirm(
    session: AsyncSession, user_id: uuid.UUID, job: ImportJob, body: ConfirmIn
) -> Recipe:
    """Store the preview, with the user's answers, as their private recipe (D10).

    Food ids are re-checked and nutrition and allergens recomputed here; nothing
    the client sends sets them, and the source is always ``private_only``.
    """
    preview = PreviewOut.model_validate(job.preview)
    answers = _check_answers(preview, body)
    wanted = {a.food_slug for a in answers.values() if a.food_slug}
    wanted |= {line.food.slug for line in preview.ingredients if line.food}
    foods = await foods_repo.get_by_slugs(session, sorted(wanted))

    ingredients: list[RecipeIngredient] = []
    for line in preview.ingredients:
        answer = answers.get(line.position)
        if answer is not None and answer.skip:
            continue
        slug = (answer.food_slug if answer else None) or (line.food.slug if line.food else None)
        food = foods.get(slug) if slug else None
        if food is None:
            raise BadAnswer(f"line {line.position}: unknown food")
        grams = answer.grams if answer else None
        if grams is None and line.food is not None and line.food.slug == slug:
            grams = line.grams
        if grams is None:
            grams = grams_for(_parsed(line), food)[0]
        if grams is None or grams <= 0:
            raise BadAnswer(f"line {line.position}: grams needed")
        own_amount = answer is None or answer.grams is None
        ingredients.append(
            RecipeIngredient(
                position=len(ingredients),
                food=food,
                amount_g=grams,
                display_amount=line.amount if own_amount and line.amount else None,
                display_unit=line.unit if own_amount and line.amount else None,
                optional=line.optional,
                prep_note=line.note,
            )
        )
    if not ingredients:
        raise BadAnswer("the recipe has no ingredients left")

    title = body.title or preview.title
    polish = preview.language == "pl"
    source = RecipeSource(
        type=_SOURCE_TYPES[(ImportType(job.type), ImportOrigin(job.origin))].value,
        # the post or page URL as attribution; a PDF's file name never reaches us
        reference=job.source_url,
        content_hash=job.cache_key,
    )
    recipe = Recipe(
        source=source,
        owner_user_id=user_id,
        title_pl=title if polish else None,
        title_en=None if polish else title,
        instructions_pl=preview.instructions if polish else [],
        instructions_en=[] if polish else preview.instructions,
        servings=body.servings or preview.servings,
        ingredients=ingredients,
    )
    session.add(recipe)
    recipes_repo.refresh_nutrition(recipe)
    recipes_repo.refresh_allergens(recipe)
    await session.flush()

    job.status = ImportStatus.CONFIRMED.value
    job.recipe_id = recipe.id
    job.preview = None  # source lines are deleted on confirm (§7.7)
    return recipe
