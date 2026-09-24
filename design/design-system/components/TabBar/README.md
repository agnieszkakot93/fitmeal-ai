# TabBar

The iOS 26 tab bar: a floating Liquid Glass capsule with four tabs (Today, Plan, Shopping, Profile) and, beside it, a separate round paprika-glass Add button.

**Props:**
- `active`: `today`, `plan`, `shopping` or `profile`.
- `accessory`: a `BottomAccessory` that sits above the bar.
- `minimized`: shrinks the bar to the active tab's icon and moves the accessory inline between it and Add. Use it while the user scrolls down (SwiftUI `.tabBarMinimizeBehavior(.onScrollDown)`).

- It floats over content. Let lists scroll underneath it, and never put a solid background behind it.
- The selected tab is `basil` on the `glass-selected` lens. Other tabs stay `ink`, not muted, so they stay legible on glass.
- Add is never "active". It opens the Add Recipe sheet. In SwiftUI it is a `Tab(role: .search)`-style separate item.
- With Reduce Transparency on, the glass turns into solid `surface-raised`.
