# CompareCard

Original vs your version: the moment FitMeal shows what it did to a recipe.

**Props:**
- `original`, `yours`: `{kcal, protein}`
- `target`: text, for example *Your lunch: 555 kcal · 45+ g protein*.
- `sourceKcal`: the nutrition the imported page states. It is shown under *Original* as *Source says …* for comparison only, never used.
- `missed`: text for when the target can't be reached while keeping the dish valid. It replaces the found pill with a warning naming the missed target and by how much. Pair it with a `Notice` offering: accept as is, pick a different recipe, or change this meal's share of the day.
- `found`, `foundLabel`, `originalLabel`, `yoursLabel`

Never show an out-of-tolerance result as on target.
