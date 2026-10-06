# Notice

A block of text that stops or explains: allergen conflicts, plans that can't be built, goals that were relaxed, import fallbacks, and offline states.

**Props:**
- `tone`:
  - `danger`: an allergen or strict-intolerance conflict. Blocking. Reserved for allergies: never use it for anything else.
  - `warning`: a target missed, no plan possible, or the allergen check can't run because there's no profile on this phone (Import Preview 26b, blocking).
  - `info`: soft goals relaxed, and import fallbacks.
  - `offline`: no connection; also the neutral tone for general notices (health notice, subscription, iCloud not reachable).
- `title`, `body`, `items` (a list of what blocked it or what was relaxed), `actions` (`[{label, icon}]`; the first is primary), `icon`.

Rules:
- **Allergen conflicts are blocking, never warnings.** Name the ingredient *and* the allergen (*Contains peanuts (peanut butter). Your allergy.*), put the notice at the top of the screen, and never collapse it. The recipe can be saved, but can't be personalized or planned until the ingredient is substituted or removed.
- **No profile on this phone:** the allergen check can't run, so Import Preview is blocked with a `warning` notice at the top (*We can’t check this recipe for your allergens*), primary action *Set up my profile*. The recipe can still be saved. Never show "no allergens found" when the check didn't run.
- **No plan possible:** say what blocked it in plain words and give concrete actions (a specific setting, a shorter plan, add recipes, relax an intolerance). Never offer to relax an allergy.
- **Offline:** say which action needs a connection. Don't fail silently.

## Import fallbacks

When an import can't read the source, it falls back to the user pasting the text. Nothing is wrong with what the user did, so:

- Tone is always `info`, never `danger` or `warning`.
- The first (primary) action is always **Paste recipe text** (`icon: 'text'`). A second, quiet action may offer another way (*Choose another PDF*, *Try another link*).
- The title says what happened in plain words; the body says what to do and, for links, that the link is kept as the source. Put a source row with the URL right under the notice.
- Don't blame the site or the user, and don't mention law or robots files. *This site doesn't allow automated reading* is enough.

| Case | Title | Second action |
| --- | --- | --- |
| Scanned PDF (no text layer) | *This PDF is a scan* | *Choose another PDF* |
| Page without schema.org recipe data | *We can’t read a recipe on this page* | *Try another link* |
| Site opts out of text and data mining | *We don’t open this site* | *Try another link* |
| Instagram or TikTok URL pasted | *We don’t open Instagram or TikTok links* (with Share → FitMeal steps as `items`) | none |
| Share with an empty caption | *This post has no caption to use* | none |
