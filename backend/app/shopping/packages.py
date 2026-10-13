"""Which packages to buy to cover a need (PRD §8.10 package counts).

The choice is the fewest packages whose total covers the need with less left
over than the smallest package size, so no package in it is ever redundant.
Among those, the least left over wins, then the larger packages.
Package sizes are whole grams; the need may be fractional.
"""

from __future__ import annotations

import math
from collections.abc import Iterable
from dataclasses import dataclass

# absorbs float noise from summing, so 200.0000000001 g needs 200 g, not 201 g
EPS = 1e-6


@dataclass(frozen=True, slots=True)
class PackageCount:
    size_g: int
    count: int


@dataclass(frozen=True, slots=True)
class Packages:
    """What to buy: package sizes largest first, and what is left over."""

    buy: tuple[PackageCount, ...]
    need_g: float

    @property
    def count(self) -> int:
        return sum(p.count for p in self.buy)

    @property
    def total_g(self) -> int:
        return sum(p.size_g * p.count for p in self.buy)

    @property
    def leftover_g(self) -> float:
        return max(0.0, self.total_g - self.need_g)


def package_sizes(sizes: Iterable[float]) -> tuple[int, ...]:
    """Distinct sizes in whole grams, largest first."""
    out = {round(s) for s in sizes}
    if any(s <= 0 for s in out):
        raise ValueError("package sizes must be at least 1 g")
    return tuple(sorted(out, reverse=True))


def choose_packages(need_g: float, sizes: Iterable[float]) -> Packages | None:
    """The packages that cover ``need_g``; ``None`` when the food has no package sizes.

    An unbounded knapsack over totals from the need up to the need plus the
    smallest size (a multiple of the smallest size always lands in that range).
    """
    if need_g < 0:
        raise ValueError("need must not be negative")
    ordered = package_sizes(sizes)
    if not ordered:
        return None
    if need_g <= EPS:
        return Packages((), 0.0)
    target = max(1, math.ceil(need_g - EPS))
    top = target + ordered[-1] - 1
    # fewest[t]: fewest packages totalling exactly t grams, -1 if none does
    fewest = [-1] * (top + 1)
    fewest[0] = 0
    for t in range(1, top + 1):
        best = -1
        for s in ordered:
            if s <= t and fewest[t - s] >= 0 and (best < 0 or fewest[t - s] + 1 < best):
                best = fewest[t - s] + 1
        fewest[t] = best
    total = min(
        (t for t in range(target, top + 1) if fewest[t] >= 0),
        key=lambda t: (fewest[t], t),
    )
    counts = dict.fromkeys(ordered, 0)
    t = total
    while t:
        # largest size that stays on a shortest path, so the result is deterministic
        s = next(s for s in ordered if s <= t and fewest[t - s] == fewest[t] - 1)
        counts[s] += 1
        t -= s
    return Packages(tuple(PackageCount(s, n) for s, n in counts.items() if n), need_g)
