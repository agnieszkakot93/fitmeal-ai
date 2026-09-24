# MacroRing

The daily kcal ring: outer arc = kcal eaten or planned vs target, inner thin arcs = the P/C/F split.

**Props:** `value`, `target`, `macros` (`{protein:{share}, carbs:{share}, fat:{share}}`, shares of kcal summing to 1; optional), `size` (default `size-ring` 168), `label`.

- The arc turns `warning` when the day is more than 3% over target.
- Always show a `MacroBar` set or `MacroLine` beside it — the ring alone never carries the numbers.
