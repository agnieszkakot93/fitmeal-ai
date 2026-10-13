# Toast

A short confirmation of something the user just did, with an optional *Undo*. It appears at the bottom (on phone above the `TabBar` and `BottomAccessory`), never covers the control the user is working with, and goes away on its own. Fill is `ink` with `surface` text, `radius-lg`, `shadow-sheet`, max width `dialog-max`.

`ToastRegion` is the polite live region that holds the toasts. Render it once per page and keep it mounted, even when empty (`AppShell` does this), so screen readers register it before the first toast.

**Props (`Toast`):**
- `message`: what happened, past tense, with the meal name (*Lunch marked as eaten*).
- `action`: `{ label, onClick }`, usually *Undo*. Clicking it runs `onClick`, then dismisses.
- `icon`: optional (`clock` for *Saved on this device, will sync*).
- `duration`: ms before auto-dismiss, default 10000 (the Today spec's Undo window). `0` keeps it until dismissed.
- `onDismiss(reason)`: `timeout`, `action`, `close` or `escape`. Without it the toast has no × and no timer.

**States:** with action, without action, with icon; paused (hover or focus inside); dismissed.

## Accessibility

- Announced through the `ToastRegion` (`role="status"`, `aria-live="polite"`, `aria-atomic="false"`). Toasts don't set their own role, so there are no nested live regions.
- **Focus never moves into a toast.** Keyboard users reach *Undo* with Tab; on Today the app inserts the toast so *Undo* follows the meal card in the Tab order (today.md).
- The timer **pauses** while the pointer is over the toast or focus is inside it, and while the browser tab is hidden. It resumes with the time that was left (2.2.1).
- `Esc` with focus inside dismisses it. The × button is *Dismiss* / *Zamknij*.
- *Undo* and × are 44 px targets. The focus ring switches to `surface` on the dark fill.
- With `prefers-reduced-motion`, it appears without sliding.
- Don't use a toast for errors that need action, for allergen information, or for anything the user must read: those are `Notice`s in the page.

## Copy

| Key | EN | PL |
| --- | --- | --- |
| `meal.toast.eaten` | {slot} marked as eaten | {slot}: oznaczono jako zjedzone |
| `meal.toast.skipped` | {slot} skipped | {slot}: pominięto |
| `meal.toast.cooked` | {slot} marked as cooked | {slot}: oznaczono jako ugotowane |
| `meal.toast.undo` | Undo | Cofnij |
| `state.offline.queued_a11y` | Saved on this device, will sync | Zapisano na tym urządzeniu, zsynchronizuje się później |
| `toast.dismiss` | Dismiss | Zamknij |

## Do / don't

- Do keep it to one line in EN; PL may wrap to two.
- Do offer *Undo* for status changes and removals.
- Don't stack more than two toasts; replace the older one.
- Don't use `danger`, `warning` or paprika fills on a toast.
- Don't praise or judge (*Great job!*, *Too much today*). Say what changed.
