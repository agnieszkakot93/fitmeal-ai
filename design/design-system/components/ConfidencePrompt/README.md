# ConfidencePrompt

Asks the user to resolve a low-confidence import line instead of guessing. It is the *Clarification prompt* screen of the PRD.

**Props:** `raw` (the imported text, for example *1 cup cheese*), `question` (*Which cheese?*), `options`, `selected`.

- It appears below 0.8 confidence. Always include *Other* as the last option.
- **Until the user answers, the line counts as possibly containing any of their allergies or strict intolerances.** So the recipe stays blocked from planning, and the prompt says so.
