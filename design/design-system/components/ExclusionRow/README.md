# ExclusionRow

One excluded item (an EU allergen, a diet category or a matched free-text entry) with its severity tier: Allergy, Intolerance, Don't like, Prefer not.

**Props:** `name` (*Peanuts*), `examples` (*incl. peanut butter, peanut oil*), `severity` (`allergy`, `intolerance`, `dislike`, `prefer-not` or null), `relaxed` (intolerance only), `onChange`.

What each tier does:
- **Allergy** paints `danger`. It is a hard exclusion that includes derived ingredients (whey → milk) and "may contain" traces, and the row says so. Only changing the tier in Profile relaxes it.
- **Intolerance** paints `warning`. It is a hard exclusion by default, and traces are allowed. Ticking **Avoid when possible** relaxes it to a strong penalty: used only when nothing else fits, and always labelled on the recipe.
- **Don't like** and **Prefer not** stay neutral. They are ranking penalties only. The Substitution Engine never introduces a disliked item.

Tapping the selected tier again clears it. Allergen information is never collapsed or hidden.
