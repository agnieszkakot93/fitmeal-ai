# Avatar

The user's initials (or photo) in a circle. It's the only way into Profile: it sits at the top right of every tab root, as in Apple's iOS 26 apps.

**Props:** `initials` (falls back to a person icon), `size` (face diameter, default 36; the hit target is never below 44), `badge` (a paprika dot for something that needs the user in Profile, such as a renewal or an unfinished target; a string becomes its accessible label), `label` (default *Profile*).

- Pass it to `NavBar` as `avatar`, not inside `trailing`. It's a person, not a glass action.
- Tapping it opens Profile as a page sheet over the current tab, with Done (glass-prominent check) at the top right.
- Use the badge sparingly: it should mean "open Profile now", never marketing.
