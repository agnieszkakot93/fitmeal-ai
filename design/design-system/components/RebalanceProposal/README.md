# RebalanceProposal

The proposal that follows a confirmed swap when the day moves outside tolerance. It lists every portion adjustment, and nothing is applied until the user confirms.

**Props:**
- `title`, `body`
- `adjustments`: `[{meal, portion: '−8%', kcal: '−70 kcal', accepted}]`. Each row has its own checkbox, so the user can reject an individual adjustment.
- `locked`: `[{meal, reason}]`, for meals that won't change: eaten, skipped, or earlier in the day.
- `before` / `after`: `{kcal, protein}`
- `cta`
- `unreachable`: when ±20% on the remaining meals can't restore the target. The actions become *Accept anyway*, *Different swap* and *Undo swap*.

Rules:
- Each adjustment is at most ±20% of that meal's portion. The proposal never takes the day below 1,200 kcal.
- Always show both totals, so the user sees what they approve.
- *Keep day as is* is always one tap.
