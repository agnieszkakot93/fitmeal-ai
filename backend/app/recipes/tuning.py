"""How well the transformation engine hits typical targets on the stored catalog.

Each scenario derives a per-serving target from a recipe's own nutrition. Used by
``donut-admin recipes tune-report`` and by a regression test on the committed
FDC snapshot, so changes to role bounds, rounding or weights are measured on
real recipes, not just synthetic ones.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.nutrition.nutrients import Nutrients
from app.optimizer.combine import transform_with_swaps
from app.optimizer.transform import Miss, Target
from app.recipes import repository
from app.recipes.models import Recipe

SCENARIOS: dict[str, Callable[[Nutrients], Target]] = {
    "cut 20% kcal, keep protein": lambda n: Target(n.kcal * 0.8, n.protein_g),
    "add 20% kcal, keep protein": lambda n: Target(n.kcal * 1.2, n.protein_g),
    "25% more protein, same kcal": lambda n: Target(n.kcal, n.protein_g * 1.25),
}


@dataclass
class ScenarioResult:
    hits: int = 0
    total: int = 0
    hits_with_swaps: int = 0  # on target only thanks to a substitution
    misses: list[tuple[str, list[Miss]]] = field(default_factory=list)


async def evaluate(session: AsyncSession, swaps: bool = True) -> dict[str, ScenarioResult]:
    results = {name: ScenarioResult() for name in SCENARIOS}
    ids = list(await session.scalars(select(Recipe.id).where(Recipe.slug.is_not(None))))
    for recipe_id in ids:
        recipe = await repository.get(session, recipe_id)
        assert recipe is not None
        per_serving = repository.compute_nutrition(recipe).per_serving
        lines = repository.transform_lines(recipe)
        alternatives = await repository.substitution_alternatives(session, recipe) if swaps else {}
        for name, make_target in SCENARIOS.items():
            combined = transform_with_swaps(lines, make_target(per_serving), alternatives)
            outcome = combined.result
            result = results[name]
            result.total += 1
            if outcome.on_target:
                result.hits += 1
                result.hits_with_swaps += bool(combined.swaps)
            else:
                result.misses.append((recipe.slug or "", outcome.misses))
    return results


def render(results: dict[str, ScenarioResult]) -> str:
    lines = []
    for name, r in results.items():
        lines.append(
            f"{name}: {r.hits}/{r.total} on target ({r.hits_with_swaps} with a substitution)"
        )
        for slug, misses in sorted(r.misses):
            detail = ", ".join(f"{m.metric.value} {m.actual:.0f} vs {m.target:.0f}" for m in misses)
            lines.append(f"  - {slug}: {detail}")
    return "\n".join(lines)
