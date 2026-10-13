# Select

A native `<select>` with a visible label, hint and error, styled like `TextField` (52 px, `surface-raised`, `line-strong` border, `radius-sm`) with a `chevron-down` icon. The browser draws the option list, so it works with every keyboard, screen reader and phone picker.

Use it for **settings** (language, theme) and for **form fields with a fixed list** the user doesn't need to compare (meal type on a manually entered recipe). On onboarding and plan questions, where the options are the content, use `SegmentedControl` (2–4 options), `SelectCard` (options with descriptions) or `Chip`s (many tags).

**Props:**
- `label` (required), `hint` (above the control), `error` (below, `danger`), `optional`.
- `options`: strings or `{ value, label, disabled }`.
- `value` + `onChange(value, event)` or `defaultValue`.
- `placeholder`: adds a first, disabled, empty option (*Choose a meal*) and selects it when there's no value. Use it when there's no sensible default; then validate on submit.
- `name`, `required`, `disabled`, `autoComplete`, `id`, `lang`.

**States:** default, hover (pointer), focus, placeholder shown, error, disabled.

## Accessibility

- Native semantics: `<label for>`, arrow keys, type-ahead, `Space`/`Alt+↓` to open; the phone's own picker on touch.
- `aria-describedby` = hint + error; `aria-invalid="true"` on error; the error is a polite live region (same as `TextField`).
- The chevron is decorative (`aria-hidden`); the whole control is the target, 52 px tall.
- Never change page, language or theme on `change` without telling the user; the language select applies immediately and keeps focus on itself, so screen readers stay in place (3.2.2 is met because the change is the expected result of a setting).
- Long PL option labels are truncated with an ellipsis only in the closed control; the open list shows them in full. Keep options short anyway.

## Copy

| Key | EN | PL |
| --- | --- | --- |
| `profile.language` | Language | Język |
| `profile.language.hint` | Starts with your browser's language. | Na początek taki jak w przeglądarce. |
| `profile.theme` | Theme | Motyw |
| `profile.theme.system` | Same as this device | Jak na tym urządzeniu |
| `profile.theme.light` | Light | Jasny |
| `profile.theme.dark` | Dark | Ciemny |
| `recipe.meal_type` | Meal type | Rodzaj posiłku |
| `recipe.meal_type.placeholder` | Choose a meal | Wybierz posiłek |
| `recipe.meal_type.required` | Choose which meal this recipe is for. | Wybierz, na który posiłek jest ten przepis. |

Language names are written in their own language (*Polski*, *English*) in both UIs.

## Do / don't

- Do use the native control; don't rebuild a custom listbox.
- Do give a default when one exists (language, theme).
- Don't use a Select for allergens, exclusion tiers or plan length; those need every option visible.
- Don't hide an option because of a tier or allergy without saying why elsewhere on the page.
