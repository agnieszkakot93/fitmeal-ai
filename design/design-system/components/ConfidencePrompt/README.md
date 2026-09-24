# ConfidencePrompt

Asks the user to resolve a low-confidence import line instead of guessing.

**Props:** `raw` (the text as imported: *1 cup cheese*), `question` (*Which cheese?*), `options`, `selected`.

- Trigger below 0.8 confidence. Always include *Other* as the last option.
