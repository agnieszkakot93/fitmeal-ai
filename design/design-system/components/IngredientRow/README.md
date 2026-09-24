# IngredientRow

One ingredient in a recipe, with its amount, what FitMeal changed and the Swap action.

**Props:** `name`, `amount` (*150 g*), `was` (original amount or ingredient — renders the paprika change state), `role` (*protein*, *sauce*), `excluded` (badge text, e.g. *Fish — excluded*), `checkable`, `checked`, `swappable`.

- Changed rows are tinted `paprika-soft` so the user can scan what moved.
- Put ingredient rows inside a `.fm-group` container.
