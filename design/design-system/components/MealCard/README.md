# MealCard

One planned meal on Today or the Plan: slot, time, name, macros, meal-prep state, status and the Recipe and Swap actions.

**Props:** `slot` (*Lunch*), `time`, `title`, `kcal`, `protein`, `carbs`, `fat`, `status`, `prep`, `badges` (`[{label, tone, icon}]`), `swappable`, `actions` (false hides the buttons).
- `status`:
  - `planned`
  - `cooked`: adds a *Cooked* badge.
  - `eaten` or `skipped`: **locked**. The pill shows a lock, Swap disappears, and later swaps and rebalances never change the meal.
- `prep`: `{portion: '1/2', cook: 'Wed', eatBy: 'Thu'}`. Every prepped meal shows its cook day and "eat by" day.

- The *Eat* pill is the North Star event. Keep it on every card on Today and on Weekly Plan, and let it work offline.
- A meal that stays fresh reads *Prepare fresh*.
