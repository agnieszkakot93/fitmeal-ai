# IconButton

A 44px round icon-only button. Use `glass` for toolbar and floating controls, as on iOS 26.

**Props:** `icon`, `label` (required; it becomes the `aria-label`), `variant`, `size`, `onClick`, `disabled`. `variant` is one of:
- `glass`: a Liquid Glass circle.
- `glass-prominent`: a basil-tinted glass circle.
- `sunken`: a 32px stepper.
- `raised`: a solid circle.

- In a `NavBar`, pass bare IconButtons as `trailing`. The bar groups them into one glass capsule, so don't give each one its own glass.
