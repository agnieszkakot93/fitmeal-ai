# SideNav

Navigation for tablet and desktop. Same destinations as `TabBar` (Today, Plan, Shopping), the paprika Add button, and the `Avatar` that opens Profile. `AppShell` shows it from 600 px and hides `TabBar`.

- **Rail** (`md`, 600–1023): `sidenav-rail` wide, icon above a short label. The current page gets a `basil-soft` pill behind its icon; Add is a round `paprika` button.
- **Full** (`lg`, ≥ 1024): `sidenav-full` wide, the name *Donut* in plain type at the top, icon beside label, the current page as a `basil-soft` capsule with `basil-ink` bold text, and Add as a `paprika` capsule.

It is solid `surface` with a `line` hairline on the right, never glass.

**Props:**
- `active`: `today`, `plan` or `shopping`.
- `variant`: `auto` (default; follows `AppShell`), `rail` or `full` (fixes the look, e.g. in showcases).
- `hrefs`: override the default `/today`, `/plan`, `/shopping`. `onNavigate(id, event)`: for client-side routing; call `event.preventDefault()` and push the route.
- `onAdd`: opens Add recipe.
- `avatar`: the Profile entry (`Avatar`), at the bottom.
- `lang`: `en` or `pl`.

**States:** each destination current; hover (pointer devices: `surface-sunken` fill; rail: on the icon pill); focus (`focus-ring`).

## Accessibility

- `<nav aria-label="Main">` with a `<ul>` of `<a href>` links. The current link has `aria-current="page"`, not only a colour: it is also bold and has a filled shape.
- Add is a `<button>` (it opens a sheet, it doesn't navigate). Its accessible name is its visible label *Add recipe*.
- Labels are always visible, also in the rail, so the rail never relies on tooltips.
- Tab order: Add → Today → Plan → Shopping → Profile. No arrow-key handling: it's a list of links, not a menu.
- Every item is at least `size-tap` (44 px) tall; rail items are 60 px.
- In the rail, long PL labels (*Dodaj przepis*) wrap to two lines rather than truncating.

## Copy

| Key | EN | PL |
| --- | --- | --- |
| `nav.today` | Today | Dzisiaj |
| `nav.plan` | Plan | Plan |
| `nav.shopping` | Shopping | Zakupy |
| `nav.add` | Add recipe | Dodaj przepis |
| `nav.profile` (Avatar name) | Profile | Profil |
| `nav.label` (landmark) | Main | Menu główne |

## Do / don't

- Do keep exactly the three tab destinations plus Add and Profile. Shopping, Plan and Today are the same on every device.
- Do make Add the only paprika item.
- Don't add Settings, Help or a recipes library here without a spec; they go in Profile.
- Don't collapse the rail to icons only.
- Don't use `danger` or `warning` badges on navigation items.
