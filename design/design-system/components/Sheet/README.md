# Sheet

A decision panel that adapts to the screen: a **bottom sheet** on phone (< 600 px), inset `space-2` with `radius-sheet` corners, and a centred **`Dialog`** from 600 px. Use it for swap meal, swap ingredient, *I don't have this*, the sign-in sheet over a new plan, and confirmations from *No plan possible*. It is the web version of the iOS floating glass sheet, but solid `surface-raised` (see *Web* in the brand book).

It shares everything with `Dialog` (native `<dialog>`, focus, `Esc`, return focus, scroll lock); only the presentation differs.

**Props:** all `Dialog` props, plus:
- `presentation`: `auto` (default; sheet below 600 px viewport, modal from 600), `sheet` or `modal`. Fix it only in showcases and tests.

**Content pattern for decisions** (brand book *Decisions*): title naming the thing (*Swap chicken breast*), ranked `SwapOption`s with their `Delta`, the effect on the day if it changes, one primary `Button` naming the result (*Use turkey breast*), and the `footnote` *Nothing changes until you confirm.*

**States:** sheet (phone), modal (tablet and desktop); short content, long content (the panel scrolls inside, the title stays at the top of the scroll); with or without description.

## Accessibility

- Same as `Dialog`: `aria-modal`, inert background, focus on the title at open, `Esc` closes, focus returns to the trigger.
- No drag handle and no swipe-to-close: on the web a handle suggests a gesture that isn't there. Close is the × button, `Esc`, the backdrop, or the quiet action.
- Actions are stacked full width on phone, primary first; in a row from 600 px.
- The sheet never covers the whole screen; the page above it stays visible under the `scrim`, so the context of the decision is kept.
- At 200% zoom the panel scrolls inside itself (max height = viewport − `space-12`).
- Swap options are a radio group (`SwapOption` is `role="radio"`); wrap them in an element with `role="radiogroup"` and `aria-labelledby` the title.

## Copy

| Key | EN | PL |
| --- | --- | --- |
| `swap.ingredient.title` | Swap {ingredient} | Zamień: {ingredient} |
| `swap.confirm_note` | Nothing changes until you confirm. | Nic się nie zmieni, dopóki nie potwierdzisz. |
| `swap.by_protein` | Amounts are converted by protein, not 1:1 | Ilości przeliczamy według białka, nie 1:1 |
| `plan.relax.title` | Change {item} to "avoid when possible"? | Zmienić {item} na „unikaj, gdy to możliwe”? |
| `plan.relax.confirm` | {item} may appear when nothing else fits, always labelled. Your allergies don't change. | {item} może się pojawić, gdy nic innego nie pasuje – zawsze z oznaczeniem. Twoje alergie się nie zmieniają. |
| `plan.relax.yes` | Change to avoid when possible | Zmień na „unikaj, gdy to możliwe” |
| `plan.relax.no` | Keep as intolerance | Zostaw jako nietolerancję |

PL note: `{item}` in `plan.relax.title` needs the accusative (*laktozę*, *gluten*); the food name list must carry that form, or the sentence must be rewritten as *Zmienić poziom dla: {item}?*.

## Do / don't

- Do keep one primary per sheet and name the result in it.
- Do show the effect on the day before the user confirms.
- Don't offer an option that conflicts with an allergy. It isn't greyed out; it isn't there.
- Don't use a sheet for navigation (that's a page with its own URL) or for long forms.
- Don't put a second sheet on top of a sheet.
