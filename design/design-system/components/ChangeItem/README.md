# ChangeItem

One line of *Why did FitMeal change this?*: the change, its measured effect, and a Keep/Undo control.

**Props:** `what` (*Reduced oil by 8 g*), `effect` (*saves 72 kcal*), `icon`, `rejected` (start as rejected), `decidable` (false hides the control on read-only lists). Render it inside `<ul class="fm-changes">`.

- Every change can be rejected on its own. The engine then re-solves without it, and nothing is saved until the user confirms (*Save my version*).
- Effects come from the nutrition engine, never from the LLM. Quote numbers, not adjectives.
