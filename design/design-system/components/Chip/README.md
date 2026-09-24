# Chip

A pill toggle for multi-select preferences, equipment and clarification answers.

**Props:** `selected`, `onChange(bool)` (omit for uncontrolled), `icon`, `disabled`; children = label. Selected chips show a check and switch to `basil-soft` / `basil-ink`.

- Use for choices where several can be on: *High protein*, *Quick meals*, *Air fryer*.
- For one-of-N use `SegmentedControl` or `SelectCard`.
