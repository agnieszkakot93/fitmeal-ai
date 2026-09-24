# ExclusionRow

One excluded food category with its severity tier: Allergy, Intolerance, Don't like, Prefer not.

**Props:** `name` (*Fish*), `examples` (*salmon, tuna, cod*), `severity` (`allergy` | `intolerance` | `dislike` | `prefer-not` | null), `onChange`.

- `allergy` is always a hard constraint and paints `danger`; `intolerance` paints `warning`; the other two stay neutral.
- Tapping the selected tier again clears it.
