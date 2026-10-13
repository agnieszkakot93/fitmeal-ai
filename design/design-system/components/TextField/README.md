# TextField

A native text input (or `<textarea>`) with a visible label, an optional hint and an error. Use it for free-text exclusions, a recipe link, pasted recipe text, search, and email if a sign-in provider needs it. **Numbers use `NumberField`** (unit suffix, numeric keyboard, the 1,200 kcal floor).

Look: `surface-raised` box, 1.5px `line-strong` border, `radius-sm`, 52 px tall, text `body` (16 px, so iOS Safari doesn't zoom on focus), placeholder `ink-faint`. Focus: `basil` border plus the `focus-ring` outline. Error: `danger` border, label and message.

**Props:**
- `label` (required, visible). `optional`: appends *(optional)* / *(opcjonalnie)*. Don't mark required fields with an asterisk; mark the optional ones.
- `hint`: shown **above** the input, so it is read before typing and isn't covered by a phone keyboard or autocomplete list.
- `error`: shown below with an `alert` icon. Say what's wrong and how to fix it.
- `value` + `onChange(value, event)` (controlled) or `defaultValue`.
- `type` (`text`, `email`, `url`, `search`, `tel`, `password`), `inputMode`, `autoComplete`, `placeholder`, `maxLength`, `name`, `required`, `disabled`, `id`.
- `multiline` + `rows`: a resizable `<textarea>` (pasted recipe text).
- `lang`: `en` or `pl` for the built-in *optional* word.

**States:** empty, filled, focus, hover (pointer: border `ink-muted`), error, disabled.

## Accessibility

- A real `<label for>`. The placeholder is never the label; it disappears while typing.
- `aria-describedby` lists the hint and, when present, the error. The field gets `aria-invalid="true"` with an error.
- The error element is always in the DOM as a polite live region, so an error that appears while typing is announced without stealing focus. On submit, the form moves focus to the first invalid field (and may show a summary with `role="alert"`).
- Validate on blur and on submit, not on every keystroke.
- Use `autocomplete` tokens where they exist (`email`, `url`), and `autocomplete="off"` for health data.
- Colour is never the only error signal: icon, text and the label colour all change.

## Copy

| Key | EN | PL |
| --- | --- | --- |
| `field.optional` | optional | opcjonalnie |
| `onb.restr.free.label` | Something else to avoid | Inne produkty do wykluczenia |
| `onb.restr.free.hint` | Type a food, for example coriander. | Wpisz produkt, np. kolendra. |
| `onb.restr.free.placeholder` | Search foods | Szukaj produktów |
| `import.link.label` | Recipe link | Link do przepisu |
| `import.link.invalid` | This doesn't look like a link. It should start with https:// | To nie wygląda na link. Powinien zaczynać się od https:// |
| `import.text.label` | Recipe text | Tekst przepisu |
| `import.text.placeholder` | Paste the ingredients and steps | Wklej składniki i kroki |

An unmatched free-text exclusion is **not** a field error: it is kept and shown as a `warning` `Notice` in its row with *Not enforced* (`onb.restr.unmatched`, onboarding.md step 11). The field error is only for a value the app can't accept at all.

## Do / don't

- Do keep labels short and visible above the field.
- Do write errors that say how to fix the value.
- Don't use `TextField` for numbers, dates of birth (never collected) or medical conditions (never collected).
- Don't disable paste.
- Don't use `danger` for a hint or for an empty optional field.
