# Delta

The nutrition impact of a change: *+4 kcal · −2 g P*.

**Props:** `items`: `[{value, unit: 'kcal'|'g'|'PLN', letter, tone: 'good'|'bad'|'neutral'}]`. Signs use a true minus (−).

- Tone follows the user's goal, not the sign. On a cut, −kcal is `good` and +protein is `good`. Protein dropping below the minimum is `bad`.
- **No price deltas in the MVP.** The `PLN` unit is for Phase 2 (estimated pricing). Until then, show kcal and macros only.
