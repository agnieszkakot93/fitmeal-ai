# BottomAccessory

A glass capsule above the tab bar for what's happening now: the next meal, meal-prep day, a cooking timer, basket progress. It's the SwiftUI `tabViewBottomAccessory`.

**Props:**
- `icon`
- `tone`: `basil` or `paprika`, for the icon disc.
- `title`: one short line.
- `subtitle`
- `action`: the label of one glass-prominent button, for example *Eat*, *Start* or *Pause*.
- `progress`: 0–1. Draws a paprika line along the bottom edge.

- Show one accessory at a time, and only while it's useful. Hide it when nothing is next.
- When the tab bar is minimized, the accessory moves inline.
