"""Transformation with substitutions (PRD §8.3 step 2 feeding steps 3-10).

When adjusting amounts alone can't reach the target, try swapping one
ingredient for a safe substitute and re-solving, then a second one if that
helps further. The caller supplies the alternatives (already filtered for the
user's exclusions by the Substitution Engine), so this stays a pure function.
A swap is only ever a proposal: the user confirms it like any other change.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field

from app.optimizer.transform import (
    KCAL_TOLERANCE_ROUNDED,
    Line,
    Metric,
    Result,
    Target,
    transform,
)

MAX_SWAPS = 2


@dataclass(frozen=True, slots=True)
class Swap:
    original_key: str
    replacement: Line


@dataclass(frozen=True, slots=True)
class CombinedResult:
    result: Result
    swaps: list[Swap] = field(default_factory=list)


def miss_size(target: Target, result: Result) -> float:
    """How far outside the tolerances the result is; 0 when on target."""
    size = 0.0
    for miss in result.misses:
        if miss.metric is Metric.KCAL:
            allowed = KCAL_TOLERANCE_ROUNDED * target.kcal
            size += max(0.0, abs(miss.actual - miss.target) - allowed) / target.kcal
        else:
            size += (miss.target - miss.actual) / max(miss.target, 1.0)
    return size


def transform_with_swaps(
    lines: Sequence[Line],
    target: Target,
    alternatives: Mapping[str, Sequence[Line]],
    max_swaps: int = MAX_SWAPS,
) -> CombinedResult:
    """Best result from at most ``max_swaps`` greedy single swaps.

    ``alternatives`` maps an original line key to replacement lines (a different
    food, an amount that does the same job). Swaps are only tried while the
    target is missed, and only kept when they reduce the miss.
    """
    current = list(lines)
    best = CombinedResult(transform(current, target))
    for _ in range(max_swaps):
        if best.result.on_target:
            break
        trials = []
        for i, line in enumerate(current):
            for alt in alternatives.get(line.key, ()):
                candidate = [*current[:i], alt, *current[i + 1 :]]
                result = transform(candidate, target)
                trials.append(
                    (miss_size(target, result), alt.key, result, candidate, line.key, alt)
                )
        if not trials:
            break
        size, _, result, candidate, original_key, alt = min(trials, key=lambda t: (t[0], t[1]))
        if size >= miss_size(target, best.result):
            break
        best = CombinedResult(result, [*best.swaps, Swap(original_key, alt)])
        current = candidate
    return best
