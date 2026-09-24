# NavBar

The iOS 26 screen header. Back and trailing actions float as Liquid Glass (a round back button and one glass capsule grouping the trailing icons), and there is no bar background.

**Props:**
- `title`
- `large`: a 32px large title for tab roots. Trailing actions float at the top right.
- `subtitle`
- `back`: the previous screen's name, used as the accessible label. The button shows a chevron; `'Cancel'` shows a close icon instead.
- `trailing`: one IconButton or several, grouped into a single glass capsule.
- `avatar`: an `Avatar`, placed after the trailing capsule. Every tab root (Today, Plan, Shopping) shows it; it opens Profile.
- `overlay`: floats the bar over a `RecipeHero`.
