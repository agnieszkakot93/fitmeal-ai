# Notice

A block of text that stops or explains: allergen conflicts, plans that can't be built, goals that were relaxed, and offline states.

**Props:**
- `tone`:
  - `danger`: an allergen or strict-intolerance conflict. Blocking.
  - `warning`: a target missed, or no plan possible.
  - `info`: soft goals relaxed.
  - `offline`: no connection.
- `title`, `body`, `items` (a list of what blocked it or what was relaxed), `actions` (`[{label, icon}]`; the first is primary), `icon`.

Rules:
- **Allergen conflicts are blocking, never warnings.** Name the ingredient *and* the allergen (*Contains peanuts (peanut butter). Your allergy.*), put the notice at the top of the screen, and never collapse it. The recipe can be saved, but can't be personalized or planned until the ingredient is substituted or removed.
- **No plan possible:** say what blocked it in plain words and give concrete actions (a specific setting, a shorter plan, add recipes, relax an intolerance). Never offer to relax an allergy.
- **Offline:** say which action needs a connection. Don't fail silently.
