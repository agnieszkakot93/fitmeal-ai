# SwapOption

A ranked alternative in the Ingredient Swap and Meal Swap sheets, with its nutrition impact.

**Props:** `title`, `amount` (the converted amount, never 1:1 grams), `delta` (Delta `items`: kcal and macros), `best`, `note`, `selected`.

- Order by fit. The first gets `best`.
- **Candidates that conflict with an allergy or a strict intolerance are never shown.** Neither are disliked items. The engine filters them out, so the list only ever holds safe options.
- No price in the MVP. Cost deltas arrive with estimated pricing in Phase 2.
