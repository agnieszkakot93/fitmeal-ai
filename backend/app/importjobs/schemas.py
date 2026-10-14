"""Import API schemas. Validation errors never echo the input (§7.7)."""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.importjobs.models import ImportOrigin, ImportStatus, ImportType
from app.importjobs.scrub import CONTROLS, controls
from app.imports.page import MAX_LINES, MAX_NAME_CHARS
from app.recipes.schemas import RecipeSummary

MAX_TEXT_BYTES = 200 * 1024  # §7.7; Caddy enforces the same cap before the body is read
MAX_URL_CHARS = 2048
MAX_GRAMS = 10_000.0
MAX_SERVINGS = 100


class _In(BaseModel):
    model_config = ConfigDict(extra="forbid", hide_input_in_errors=True)


def _no_controls(value: str | None) -> str | None:
    # Postgres refuses NUL, and the failed insert's error would quote the input
    if value is not None and CONTROLS.search(value):
        raise ValueError("control characters are not allowed")
    return value


class ImportIn(_In):
    type: ImportType
    origin: ImportOrigin
    url: str | None = Field(
        default=None,
        max_length=MAX_URL_CHARS,
        description="The page to read (`link`), or a shared post's URL kept as the source "
        "reference only and never fetched (`text`)",
    )
    text: str | None = Field(
        default=None,
        max_length=MAX_TEXT_BYTES,
        description=f"Recipe text (`text` only), at most {MAX_TEXT_BYTES} bytes as UTF-8",
    )

    _url_ok = field_validator("url")(_no_controls)

    @field_validator("text")
    @classmethod
    def _text_controls(cls, value: str | None) -> str | None:
        # PDF text carries form feeds and the like: spaces, not an error
        return controls(value) if value is not None else None

    @model_validator(mode="after")
    def _shape(self) -> Self:
        if self.type is ImportType.LINK:
            if not self.url or self.text is not None:
                raise ValueError("a link import takes `url` and no `text`")
            if self.origin is ImportOrigin.PDF:
                raise ValueError("PDF text is a text import")
        else:
            if not self.text or not self.text.strip():
                raise ValueError("a text import takes `text`")
            if len(self.text.encode()) > MAX_TEXT_BYTES:
                raise ValueError(f"`text` is over {MAX_TEXT_BYTES} bytes")
        return self


class Candidate(BaseModel):
    slug: str
    name_en: str
    name_pl: str
    score: float


class PreviewLine(BaseModel):
    position: int
    raw: str
    # the parse, kept so confirm can turn a chosen food into grams
    amount: float | None
    unit: str | None
    name: str
    note: str | None
    optional: bool
    weight_g: float | None
    food: Candidate | None = Field(description="The matched food, if any")
    grams: float | None
    confidence: float = Field(ge=0, le=1)
    needs_clarification: bool
    candidates: list[Candidate]


class ClarificationKind(StrEnum):
    INGREDIENT = "ingredient"
    SERVINGS = "servings"
    TITLE = "title"


class Clarification(BaseModel):
    kind: ClarificationKind
    position: int | None = Field(description="The ingredient line, for `ingredient`")
    question: str = Field(description="Why we ask, e.g. `which ingredient?`, `how much?`")
    candidates: list[Candidate] = []


class PreviewOut(BaseModel):
    title: str | None
    servings: int | None
    language: str
    source_url: str | None
    instructions: list[str]
    ingredients: list[PreviewLine]
    clarifications: list[Clarification]
    confidence: float = Field(ge=0, le=1, description="The lowest line confidence")


class ImportOut(BaseModel):
    id: uuid.UUID
    type: ImportType
    origin: ImportOrigin
    status: ImportStatus
    error: str | None = Field(
        description="Why it failed: `no_recipe`, `tdm_opt_out`, `robots_disallowed` and the "
        "fetch errors mean the app offers to paste the recipe text instead"
    )
    cached: bool
    created_at: datetime
    expires_at: datetime
    preview: PreviewOut | None
    recipe_id: uuid.UUID | None


class AnswerIn(_In):
    position: int = Field(ge=0, lt=MAX_LINES)
    skip: bool = Field(default=False, description="Leave this line out of the recipe")
    food_slug: str | None = Field(default=None, max_length=200)
    grams: float | None = Field(
        default=None,
        gt=0,
        le=MAX_GRAMS,
        description="For the whole recipe; omit to use the line's own amount",
    )

    _slug_ok = field_validator("food_slug")(_no_controls)

    @model_validator(mode="after")
    def _shape(self) -> Self:
        if self.skip and (self.food_slug or self.grams is not None):
            raise ValueError("a skipped line takes no food or grams")
        if not self.skip and self.food_slug is None and self.grams is None:
            raise ValueError("an answer needs `food_slug`, `grams` or `skip`")
        return self


class ConfirmIn(_In):
    title: str | None = Field(default=None, min_length=1, max_length=MAX_NAME_CHARS)
    servings: int | None = Field(default=None, ge=1, le=MAX_SERVINGS)
    answers: list[AnswerIn] = Field(default=[], max_length=MAX_LINES)

    _title_ok = field_validator("title")(_no_controls)


class UnansweredOut(BaseModel):
    detail: str
    positions: list[int]
    missing: list[ClarificationKind]


class ConfirmOut(BaseModel):
    import_id: uuid.UUID
    recipe: RecipeSummary
