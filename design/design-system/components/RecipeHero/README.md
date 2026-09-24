# RecipeHero

The edge-to-edge top of a recipe. It stands in for food photography with a plate drawn from the recipe's own macro split: a protein, carbs and fat ring. Glass toolbar buttons float over it.

**Props:** `macros` (`{protein, carbs, fat}`, shares of kcal), `height` (default 300), `tone` (`paprika`, `basil` or `premium` background), `children` (an overlaid `NavBar overlay`).

- Imported recipes never reuse the source's photos, so the plate is the default image. The user's own photos can replace it later.
- Round only the bottom corners (`radius-xl`). It runs under the status bar.
