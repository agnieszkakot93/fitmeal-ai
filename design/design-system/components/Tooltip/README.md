# Tooltip

A short label that appears on hover or keyboard focus, for **icon-only buttons on desktop** (*More actions*, *Swap lunch*) and for the reason a control is unavailable (*You can check this off on Fri.*). `ink` bubble with `surface` text, `footnote` weight 600, `radius-sm`, max 15rem wide.

**A tooltip is never the only place for information.** Touch users never see it, and many screen-reader users won't either. The icon button already has its name in `aria-label`; a disabled reason is also its `aria-describedby`, and the page must make the same fact clear another way (the day column, the date).

**Props:**
- `label`: the text. Short; no links or buttons inside (a tooltip can't hold interactive content).
- `children`: exactly one focusable trigger (`IconButton`, a button, a link).
- `describe`: `false` (default) = the tooltip repeats the trigger's `aria-label` and is `aria-hidden`, so it isn't read twice. `true` = it adds information and becomes the trigger's `aria-describedby`.
- `placement`: `bottom` (default), `top` or `end`.
- `delay`: hover delay in ms (default 400). Keyboard focus shows it at once.
- `open`: forces it open (showcases, tests).

**States:** hidden, shown on hover, shown on keyboard focus, dismissed with `Esc`.

## Accessibility (WCAG 1.4.13)

- **Dismissible:** `Esc` hides it without moving focus.
- **Hoverable:** the pointer can move onto the bubble without it disappearing (no gap between trigger and bubble).
- **Persistent:** it stays until hover/focus leaves or `Esc`; no timeout.
- Shown on `:focus-visible` only, so a mouse click doesn't leave a bubble behind.
- `role="tooltip"`. In label mode it is `aria-hidden`; in describe mode it is referenced by `aria-describedby` (read even while hidden).
- The trigger keeps its own 44 px target; the bubble isn't a target.
- With `prefers-reduced-motion`, no fade.

## Copy

| Key | EN | PL |
| --- | --- | --- |
| `meal.action.more` | More actions | Więcej działań |
| `meal.action.swap_a11y` | Swap {slot} | Zamień: {slot} |
| `plan.future_eat_hint` | You can check this off on {weekday}. | Odhaczysz to w dniu: {weekday}. |

## Do / don't

- Do give every icon-only button on desktop a tooltip with the same words as its `aria-label`.
- Do keep it to one short line in EN (PL may wrap).
- Don't put allergen, nutrition or price information in a tooltip.
- Don't use a tooltip on text buttons or links that already say what they do.
- Don't use it on phone layouts; show a visible label instead.
