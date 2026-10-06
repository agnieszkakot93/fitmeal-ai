# Icon

Line icons for the web previews and Android parity; 24px grid, 1.75 stroke, round caps, drawn in `currentColor`.

On iOS use the SF Symbol listed in the brand book's Iconography table instead — `Icon` exists so web surfaces and previews match it.

**Props:** `name` (one of `Icon.names`), `size` (px, default 22), `weight` (stroke, default 1.75; 2.1–2.5 for active/checked), `label` (gives it `role="img"`; omit for decorative icons).

- `cloud` (SF `icloud`) means the user's private iCloud only: the *Sync with iCloud* toggle, restoring a profile on a new phone, and the iCloud line in *Where your data lives*. Don't use it for our servers.
- Do colour icons by setting `color` on the parent (`ink`, `ink-muted`, `basil`).
- Don't use icons as the only label of a control — pair with text, or give the button an `aria-label`.
