# NumberField

A numeric input with a unit suffix, for calories, grams and body data.

**Props:** `label`, `value`, `unit` (*kcal*, *g*, *kg*, *cm*), `hint`, `error`, `large` (a 48px centred numeral for the single question on an onboarding screen), `placeholder`.

- Hints say where a value came from: *Suggested from your body data. Change it anytime.*
- **The 1200 kcal floor is a refusal, not a warning.** Below it, show the error state with the reason: *FitMeal doesn't build plans below 1,200 kcal a day. Very low intakes need a doctor or dietitian.* Continue stays disabled. A suggested value is clamped to 1200.
- No weekly-budget amount in the MVP: it comes with estimated pricing in Phase 2.
