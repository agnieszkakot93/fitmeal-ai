"""Catalog recipes: list, detail, personalize and substitution options.

Only catalog recipes (no owner) are served here; private imports get their own
owner-filtered endpoints with auth. Requests that need the user's exclusions or
targets carry them in a JSON body, never the URL, so they don't end up in
access logs (D8); the GET variants work without them.
"""

from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import ARRAY, Text, cast, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.auth.routing import HideInputRoute
from app.core.db import get_session
from app.foods import repository as foods_repo
from app.foods.models import FoodItem
from app.foods.vocab import CulinaryRole
from app.nutrition.allergens import Exclusion, TraceStatus
from app.nutrition.nutrients import Nutrients
from app.optimizer.combine import transform_with_swaps
from app.optimizer.substitute import Option, options
from app.optimizer.transform import Target
from app.recipes import repository
from app.recipes.models import Recipe, RecipeIngredient
from app.recipes.schemas import (
    BlockedDetail,
    BlockedOut,
    ChangeOut,
    ChangeReason,
    ConflictOut,
    FoodRef,
    IngredientOut,
    MissOut,
    NutritionOut,
    PersonalizeIn,
    PersonalizeOut,
    ProposedIngredient,
    RecipeDetail,
    RecipeList,
    RecipeSummary,
    SearchIn,
    SubstitutionOption,
    SubstitutionsIn,
    SubstitutionsOut,
    SwapOut,
    nutrients_out,
    to_exclusions,
)

router = APIRouter(prefix="/v1/recipes", tags=["recipes"], route_class=HideInputRoute)

Session = Annotated[AsyncSession, Depends(get_session)]

_NOT_FOUND = "recipe not found"
_WITH_FOODS = (
    selectinload(Recipe.ingredients)
    .selectinload(RecipeIngredient.food)
    .options(selectinload(FoodItem.portions), selectinload(FoodItem.aliases))
)


def _key(ingredient: RecipeIngredient) -> str:
    return f"{ingredient.position}:{ingredient.food.slug}"


def _food_ref(food: FoodItem) -> FoodRef:
    return FoodRef(slug=food.slug, name_en=food.name_en, name_pl=food.name_pl)


def _role(ingredient: RecipeIngredient) -> CulinaryRole:
    return CulinaryRole(ingredient.culinary_role or ingredient.food.culinary_roles[0])


def _total_minutes(recipe: Recipe) -> int | None:
    if recipe.prep_minutes is None and recipe.cook_minutes is None:
        return None
    return (recipe.prep_minutes or 0) + (recipe.cook_minutes or 0)


def _summary(recipe: Recipe, conflicts: list[ConflictOut] | None = None) -> RecipeSummary:
    per_serving = None
    if recipe.kcal is not None:
        per_serving = nutrients_out(
            Nutrients(
                kcal=recipe.kcal,
                protein_g=recipe.protein_g or 0.0,
                fat_g=recipe.fat_g or 0.0,
                carbs_g=recipe.carbs_g or 0.0,
                fiber_g=recipe.fiber_g or 0.0,
            ).scale(1 / recipe.servings)
        )
    return RecipeSummary(
        id=recipe.id,
        slug=recipe.slug,
        title_en=recipe.title_en,
        title_pl=recipe.title_pl,
        servings=recipe.servings,
        prep_minutes=recipe.prep_minutes,
        cook_minutes=recipe.cook_minutes,
        total_minutes=_total_minutes(recipe),
        difficulty=recipe.difficulty,
        tags=recipe.tags,
        per_serving=per_serving,
        allergens=recipe.allergens,
        may_contain=recipe.may_contain,
        trace_status=TraceStatus(recipe.trace_status),
        conflicts=conflicts or [],
    )


async def _search(session: AsyncSession, query: SearchIn) -> RecipeList:
    # catalog recipes only; private imports need an owner check
    stmt = select(Recipe).where(Recipe.owner_user_id.is_(None))
    if query.tags:
        stmt = stmt.where(Recipe.tags.op("@>")(cast(query.tags, ARRAY(Text))))
    if query.max_total_minutes is not None:
        total = func.coalesce(Recipe.prep_minutes, 0) + func.coalesce(Recipe.cook_minutes, 0)
        stmt = stmt.where(total <= query.max_total_minutes)
    stmt = stmt.order_by(Recipe.title_en, Recipe.id)
    exclusions = to_exclusions(query.exclusions)
    if exclusions:
        # The exclusion check needs every ingredient's food, so it runs in Python
        # and pagination follows it. Fine for the catalog's size.
        stmt = stmt.options(_WITH_FOODS)
    recipes = list(await session.scalars(stmt))

    items = []
    for recipe in recipes:
        conflicts: list[ConflictOut] = []
        if exclusions:
            result = repository.check_exclusions(recipe, exclusions)
            if result.blocked:
                continue
            conflicts = [
                ConflictOut(key=c.key, verdict=c.verdict, optional=c.optional)
                for c in result.conflicts
            ]
        items.append(_summary(recipe, conflicts))
    page = items[query.offset : query.offset + query.limit]
    return RecipeList(items=page, total=len(items))


@router.get("", response_model=RecipeList)
async def list_recipes(
    session: Session,
    tag: Annotated[list[str], Query(max_length=10, description="All must match")] = [],  # noqa: B006
    max_total_minutes: Annotated[int | None, Query(ge=1, le=1440)] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0, le=10_000)] = 0,
) -> RecipeList:
    """The catalog without exclusions; use `POST /v1/recipes/search` to apply them."""
    query = SearchIn(tags=tag, max_total_minutes=max_total_minutes, limit=limit, offset=offset)
    return await _search(session, query)


@router.post("/search", response_model=RecipeList)
async def search_recipes(session: Session, body: SearchIn) -> RecipeList:
    """The catalog filtered by the user's exclusions (sent per request, never stored).

    Recipes with an excluded required ingredient are left out.
    """
    return await _search(session, body)


async def _get(session: AsyncSession, recipe_id: uuid.UUID) -> Recipe:
    recipe = await repository.get(session, recipe_id)
    if recipe is None or recipe.owner_user_id is not None:
        raise HTTPException(status_code=404, detail=_NOT_FOUND)
    return recipe


@router.get("/{recipe_id}", response_model=RecipeDetail, responses={404: {}})
async def get_recipe(session: Session, recipe_id: uuid.UUID) -> RecipeDetail:
    recipe = await _get(session, recipe_id)
    nutrition = repository.compute_nutrition(recipe)
    ingredients = []
    for i in recipe.ingredients:
        food = i.food
        ingredients.append(
            IngredientOut(
                key=_key(i),
                position=i.position,
                food=_food_ref(food),
                amount_g=round(i.amount_g, 1),
                per_serving_g=round(i.amount_g / recipe.servings, 1),
                display_amount=i.display_amount,
                display_unit=i.display_unit,
                culinary_role=_role(i),
                optional=i.optional,
                prep_note=i.prep_note,
                allergens=food.effective_allergens,
                may_contain=food.effective_may_contain,
                trace_status=TraceStatus(food.effective_trace_status),
            )
        )
    return RecipeDetail(
        **_summary(recipe).model_dump(),
        instructions_en=recipe.instructions_en,
        instructions_pl=recipe.instructions_pl,
        equipment=recipe.equipment,
        fridge_days=recipe.fridge_days,
        freezer_friendly=recipe.freezer_friendly,
        meal_prep_score=recipe.meal_prep_score,
        ingredients=ingredients,
        nutrition=NutritionOut(
            total=nutrients_out(nutrition.total),
            per_serving=nutrients_out(nutrition.per_serving),
            total_grams=round(nutrition.total_grams, 1),
        ),
    )


@router.post(
    "/{recipe_id}/personalize",
    response_model=PersonalizeOut,
    responses={404: {}, 409: {"model": BlockedOut}},
)
async def personalize(
    session: Session, recipe_id: uuid.UUID, body: PersonalizeIn
) -> PersonalizeOut:
    """Propose one serving adjusted to the meal target. Nothing is stored (D8).

    Excluded optional ingredients are left out. A recipe with an excluded
    required ingredient answers 409 with the ingredients to substitute first
    (see the substitutions endpoint).
    """
    recipe = await _get(session, recipe_id)
    exclusions = to_exclusions(body.exclusions)
    checked = repository.check_exclusions(recipe, exclusions)
    if checked.blocked:
        raise HTTPException(
            status_code=409,
            detail=BlockedDetail(
                message="a required ingredient is excluded; substitute it first",
                must_substitute=checked.must_substitute,
            ).model_dump(),
        )
    removed = set(checked.must_remove)
    lines = [ln for ln in repository.transform_lines(recipe) if ln.key not in removed]
    if not lines:
        raise HTTPException(
            status_code=409,
            detail=BlockedDetail(message="every ingredient is excluded").model_dump(),
        )
    t = body.target
    target = Target(kcal=t.kcal, protein_min_g=t.protein_min_g, fat_g=t.fat_g, carbs_g=t.carbs_g)
    alternatives = await repository.substitution_alternatives(session, recipe, exclusions)
    combined = transform_with_swaps(lines, target, alternatives)
    result = combined.result

    swapped = {s.original_key: s.replacement for s in combined.swaps}
    new_foods = await foods_repo.get_by_slugs(
        session, [_swapped_slug(s.replacement.key) for s in combined.swaps]
    )
    ingredients = []
    changes = []
    for i in recipe.ingredients:
        key = _key(i)
        original_g = i.amount_g / recipe.servings
        food = i.food
        grams = 0.0
        if key in removed:
            changes.append(
                ChangeOut(
                    key=key, original_g=round(original_g, 1), grams=0, reason=ChangeReason.EXCLUDED
                )
            )
        elif key in swapped:
            food = new_foods[_swapped_slug(swapped[key].key)]
            grams = result.grams[swapped[key].key]
        else:
            grams = result.grams[key]
        ingredients.append(
            ProposedIngredient(
                key=key,
                position=i.position,
                food=_food_ref(food),
                original_food=i.food.slug,
                original_g=round(original_g, 1),
                grams=round(grams, 1),
                removed=key in removed,
                swapped=key in swapped,
            )
        )
    changes += [
        ChangeOut(
            key=c.key,
            original_g=round(c.original_g, 1),
            grams=round(c.grams, 1),
            reason=ChangeReason(c.reason.value),
        )
        for c in result.changes
    ]
    return PersonalizeOut(
        recipe_id=recipe.id,
        ingredients=ingredients,
        changes=changes,
        swaps=[
            SwapOut(
                original_key=s.original_key,
                replacement_key=s.replacement.key,
                food=_food_ref(new_foods[_swapped_slug(s.replacement.key)]),
                grams=round(s.replacement.grams, 1),
            )
            for s in combined.swaps
        ],
        original_nutrition=nutrients_out(repository.compute_nutrition(recipe).per_serving),
        nutrition=nutrients_out(result.nutrition),
        on_target=result.on_target,
        misses=[
            MissOut(metric=m.metric, target=round(m.target, 1), actual=round(m.actual, 1))
            for m in result.misses
        ],
    )


def _swapped_slug(alt_key: str) -> str:
    # substitution_alternatives keys a replacement "<original key>=><food slug>"
    return alt_key.rsplit("=>", 1)[1]


async def _substitutions(
    session: AsyncSession, recipe_id: uuid.UUID, query: SubstitutionsIn
) -> SubstitutionsOut:
    recipe = await _get(session, recipe_id)
    ingredient = next((i for i in recipe.ingredients if i.position == query.ingredient), None)
    if ingredient is None:
        raise HTTPException(status_code=404, detail="ingredient not found")
    key = _key(ingredient)
    exclusions = to_exclusions(query.exclusions)
    grams = ingredient.amount_g / recipe.servings
    role = _role(ingredient)

    fix = next((f for f in await repository.propose_fixes(session, recipe, exclusions)
                if f.key == key), None)  # fmt: skip
    ranked: list[Option]
    if fix is not None:
        ranked = fix.substitutes[: query.limit]
    else:
        ranked = await _options(session, ingredient, grams, role, exclusions, query.limit)
    foods = await foods_repo.get_by_slugs(session, [o.key for o in ranked])
    return SubstitutionsOut(
        key=key,
        position=ingredient.position,
        food=_food_ref(ingredient.food),
        grams=round(grams, 1),
        culinary_role=role,
        excluded=fix is not None,
        remove=fix is not None and fix.remove,
        options=[
            SubstitutionOption(
                food=_food_ref(foods[o.key]),
                grams=round(o.grams, 1),
                same_group=o.same_group,
                disliked=o.disliked,
                delta=nutrients_out(o.delta),
                score=round(o.score, 3),
            )
            for o in ranked
        ],
    )


async def _options(
    session: AsyncSession,
    ingredient: RecipeIngredient,
    grams: float,
    role: CulinaryRole,
    exclusions: list[Exclusion],
    limit: int,
) -> list[Option]:
    food = ingredient.food
    candidates = await foods_repo.substitution_candidates(session, food, role.value)
    return options(
        foods_repo.to_substitution_food(food),
        grams,
        role,
        [foods_repo.to_substitution_food(c) for c in candidates],
        exclusions,
        limit=limit,
    )


@router.get("/{recipe_id}/substitutions", response_model=SubstitutionsOut, responses={404: {}})
async def get_substitutions(
    session: Session,
    recipe_id: uuid.UUID,
    ingredient: Annotated[int, Query(ge=0, le=1000, description="The ingredient's `position`")],
    limit: Annotated[int, Query(ge=1, le=20)] = 5,
) -> SubstitutionsOut:
    """Ranked substitutes for one ingredient, without exclusions.

    Use `POST` on the same path to send the user's exclusions.
    """
    query = SubstitutionsIn(ingredient=ingredient, limit=limit)
    return await _substitutions(session, recipe_id, query)


@router.post("/{recipe_id}/substitutions", response_model=SubstitutionsOut, responses={404: {}})
async def post_substitutions(
    session: Session, recipe_id: uuid.UUID, body: SubstitutionsIn
) -> SubstitutionsOut:
    """Ranked substitutes for one ingredient that respect the user's exclusions.

    An excluded ingredient gets the fix from the exclusion check (`remove` for
    an optional one, else safe substitutes); allergy and strict-intolerance
    conflicts are never offered, dislikes are ranked down.
    """
    return await _substitutions(session, recipe_id, body)
