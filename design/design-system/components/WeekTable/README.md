# WeekTable

The whole plan at a glance on desktop: **days as columns, meal slots as rows**, a compact meal in each cell, day totals at the top, and meal-prep batches linked across days (weekly-plan.md, `lg`). Below 1024 px viewport it renders as a **stacked list**: one section per day with its meals in slot order.

- **Table** (`lg`): a real `<table>` in a `surface-raised` card with `line` grid lines. Columns are at least `week-col-min` (168) wide; when the container is narrower (a 1024 px window with `SideNav` and a right rail), the table scrolls horizontally inside its own region while the slot column stays pinned. Today's column header is `basil` with a *Today* badge; cook days carry a paprika *Cook day* badge.
- **List** (`sm`/`md`, and any desktop at 200% zoom): day heading (*Wed 14 Oct*), badges, the day's `MacroLine`, then each slot's caption and its meal card.

On the Weekly Plan screen the spec uses `DayStrip` + one day on phone and tablet. Use the list layout where all days should be visible at once (an overview, a printable view, a desktop at high zoom).

Each meal shows its title (a link to the recipe), `MacroLine` kcal + protein, badges, and the status: an *Eat* pill, or static *Eaten* / *Skipped* with a lock. Cards in the same batch get a 2px `paprika` edge, and in the table a short paprika connector to the next day's card. The connector is decorative; the badge text (*Cooked Mon · eat by Wed*) carries the meaning.

**Props:**
- `days`: `{ id, name, date, label, today, cook, totals: { kcal, protein } }`. `label` is the full spoken date (*Wednesday 14 October*) used in accessible names.
- `slots`: `{ id, label }` in slot order.
- `meals[dayId][slotId]`: `{ title, kcal, protein, status, href, badges, batch, eatHint, queued }`. An empty cell renders *No meal*.
  - `badges`: same order rules as `MealCard` on Today. The relaxed-intolerance `warning` badge is always shown, also in the compact card; there is no overflow.
  - `batch`: the same id on every card cooked in one batch.
  - `eatHint`: for future days. *Eat* becomes `aria-disabled` with this text as its description and tooltip (*You can check this off on Fri.*).
  - `queued`: an offline status change waiting to sync (`clock` icon, *Saved on this device, will sync*).
- `layout`: `auto` (default: table from 1024 px viewport, list below), `table` or `list`.
- `caption` (default *Your plan*), `showCaption`, `headingLevel` for the list's day headings (default 2), `lang`.
- `onEat(dayId, slotId)`, `onOpen(dayId, slotId)` (when there's no `href`).

**States:** planned, cooked, eaten (locked), skipped (locked, muted), future (Eat disabled with hint), queued offline, empty slot, batch start/middle/end, relaxed-intolerance label, today column.

## Accessibility

- Table: `<caption>` (visually hidden unless `showCaption`), `<th scope="col">` per day and `<th scope="row">` per slot, so a screen reader announces *Wednesday 14 Oct, Lunch* on each cell. Today's header has `aria-current="date"`. A first body row, *Day total*, holds the day totals so they aren't repeated in every column header.
- The scroll container is a labelled region (`role="region"`, `aria-labelledby` the caption) with `tabindex="0"`, so keyboard users can scroll it.
- **Keyboard:** Tab reaches every link and button in reading order (row by row). With focus on a meal title, arrow keys move to the meal title in the next/previous day (←/→) or slot (↑/↓), skipping empty cells; `Home`/`End` go to the first/last day in the row, `Ctrl+Home`/`Ctrl+End` to the first/last meal. In the list layout ↑/↓ move between meals in order. Arrow keys don't trap: Tab always leaves.
- *Eat* has the accessible name *Eat lunch, Wednesday 14 October*; locked statuses are text with a lock icon named *Locked*. Status is never colour-only.
- List: an `<ol>` of days, each a `<section>` labelled by its heading, with an `<ol>` of meals (slot order matters).
- The batch connector and edge are CSS only, invisible to assistive tech.
- At 200% zoom a desktop gets the list (the viewport is under 1024 px), which reflows at 320 px with no horizontal scroll.

## Copy

| Key | EN | PL |
| --- | --- | --- |
| `plan.week.caption` | Your plan | Twój plan |
| `plan.week.meal` (hidden corner header) | Meal | Posiłek |
| `plan.week.total` | Day total | Suma dnia |
| `plan.week.no_meal` | No meal | Brak posiłku |
| `plan.week.today` | Today | Dzisiaj |
| `plan.week.cook_day` | Cook day | Dzień gotowania |
| `meal.action.eat` | Eat | Zjedz |
| `meal.action.eat_a11y` | Eat {slot}, {day} | Zjedz: {slot}, {day} |
| `meal.status.eaten` / `skipped` | Eaten / Skipped | Zjedzone / Pominięte |
| `meal.locked_a11y` | Locked | Zablokowane |
| `plan.future_eat_hint` | You can check this off on {weekday}. | Odhaczysz to w dniu: {weekday}. |
| `prep.cook_today` | Cook today · eat by {day} | Ugotuj dziś · zjedz do: {day} |
| `prep.cooked_on` | Cooked {day} · eat by {eat_by} | Ugotowane: {day} · zjedz do: {eat_by} |
| `meal.label.relaxed` | Contains {item} · avoid when possible | Zawiera: {item} · unikaj, gdy to możliwe |

## Do / don't

- Do keep the relaxed-intolerance badge visible on every card that has it.
- Do show day totals as returned by the planner, with *On target* in the day summary elsewhere; the table itself doesn't judge the numbers.
- Don't colour cells by over/under target, and don't use `danger` anywhere in the plan (allergens can't be in a plan).
- Don't make the whole cell one big link around the buttons; the title is the link.
- Don't drag and drop meals in the MVP; swaps go through the Swap sheet.
