# Dialog

A modal for a short decision that needs an answer before the user goes on: replace a plan, confirm a loaded profile, confirm a setting change from *No plan possible*. Built on the native `<dialog>` element with `showModal()`. Centred, max `dialog-max` (440), solid `surface-raised`, `radius-xl`, `shadow-sheet`, over the light `scrim`.

For choices with options (swap meal, swap ingredient, *I don't have this*) use `Sheet`, which is a bottom sheet on phone and this Dialog from 600 px.

**Props:**
- `open`, `onClose(reason)`: controlled. `reason` is `escape`, `backdrop` or `close`. Always pass `onClose`; it is what keeps your state in sync with `Esc`.
- `title` (required): a question or the outcome (*Replace your current plan?*). Rendered as `<h2>` and used as `aria-labelledby`.
- `description`: one or two sentences, used as `aria-describedby`.
- `children`: extra content (a profile summary, a list).
- `actions`: `Button`s. The first is the primary and names the outcome (*Replace plan*); then a quiet way out that also names its outcome (*Keep current plan*, *Not now*). Never *OK* / *Cancel*.
- `closeButton` (default true): the × `IconButton` (*Close* / *Zamknij*).
- `closeOnBackdrop` (default true): set false when the dialog holds typed input that would be lost.
- `preview`: showcase only; renders the panel inline without opening a modal.

**States:** open, closed; with description, with body content; one or two actions.

## Accessibility

- Native modal `<dialog>` with `aria-modal="true"`: the rest of the page is inert, so focus is trapped and screen readers can't wander behind it.
- On open, focus goes to the title (`tabIndex=-1`), so the question is read first; put `data-autofocus` on a control to focus it instead (e.g. the safe action in a destructive dialog).
- `Esc` closes (`onClose('escape')`). On close, focus returns to the element that opened it; if that element is gone, move focus to the page `<h1>`.
- Page scroll is locked while open (`html:has(dialog[open])`).
- Actions keep DOM order = visual order (primary first), in a row from 600 px and stacked full-width in a `Sheet` on phone.
- `::backdrop` uses `scrim`; very old browsers that don't pass variables to `::backdrop` show no dim, which is acceptable.

## Copy

| Key | EN | PL |
| --- | --- | --- |
| `dialog.close` | Close | Zamknij |
| `plan.replace.title` | Replace your current plan? | Zastąpić obecny plan? |
| `plan.replace.body` | Meals you've already marked stay in your history. | Odhaczone posiłki zostaną w historii. |
| `plan.replace.yes` | Replace plan | Zastąp plan |
| `plan.replace.no` | Keep current plan | Zostaw obecny plan |
| `data.load_confirm` | Use this profile? | Użyć tego profilu? |
| `data.load_confirm.body` | This replaces the profile in this browser. | Zastąpi to profil zapisany w tej przeglądarce. |
| `data.load_confirm.yes` | Use this profile | Użyj tego profilu |
| `data.load_confirm.other` | Choose another file | Wybierz inny plik |
| `data.download.title` | Download your profile? | Pobrać profil? |
| `data.download_warning` | This file contains your allergies and targets. Keep it private. | Ten plik zawiera Twoje alergie i cele. Nie udostępniaj go. |
| `common.not_now` | Not now | Nie teraz |

## Do / don't

- Do list allergies in full in a profile summary, with the `danger` badge and the word *allergy*. Never truncate them.
- Do say what stays safe (*Meals you've already marked stay in your history.*, *Your allergies don't change.*).
- Don't use a Dialog for information the user can't act on; use a `Notice` in the page.
- Don't stack dialogs. Close one before opening another.
- Don't use `danger` for the primary unless the action deletes something (*Delete account*).
- Don't open a Dialog on page load (except the sign-in sheet over a new plan, per the onboarding spec).
