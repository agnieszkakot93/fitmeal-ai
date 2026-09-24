# SwapOption

A ranked alternative in the Ingredient Swap and Recipe Swap sheets, with its impact.

**Props:** `title`, `amount` (the converted amount, never 1:1 grams), `delta` (Delta `items`), `best`, `note`, `selected`, `blocked` (reason text — allergen or exclusion — disables it).

- Order by fit; the first gets `best`.
- Show blocked options only when the user would expect them (*Tofu — contains soy, your allergy*), so they learn why.
