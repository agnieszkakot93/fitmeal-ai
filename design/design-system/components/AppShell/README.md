# AppShell

The web page frame. It places navigation, the page header, notices, the main content, an optional right rail and the toast region, and switches layout at the web breakpoints. Mobile-first: the phone layout is the default and wider layouts are added on top.

| Breakpoint | Layout |
| --- | --- |
| `sm` < 600 | One column, gutter `space-5`. Bottom `TabBar` (glass, with Add) sticks to the bottom; an optional `BottomAccessory` sits above it. |
| `md` 600–1023 | `SideNav` as a rail on the left, content centred at max `container-md`, gutter `space-6`. No bottom bar. |
| `lg` ≥ 1024 | `SideNav` with labels, content max `container-lg`, gutter `space-8`. With `aside`, a two-column grid: main column (max `container-main-lg`) and a sticky right rail (`aside-lg`). |

The switch uses container queries on the shell's own width, so it behaves the same full-screen and in a showcase frame.

**Props:**
- `active`: `today`, `plan` or `shopping`. Marks the current destination in both `TabBar` and `SideNav` (`aria-current="page"`).
- `header`: the page `TopBar` (holds the `<h1>`).
- `banner`: an `OfflineBanner`, rendered first. Keep it mounted (`state="none"` when online) so its live region works.
- `notices`: the notices zone (`Notice`, `InstallPrompt`), stacked, never collapsed.
- `aside` + `asideLabel`: right-rail content at `lg` (Today: day summary, Cook today, Up next). Below `lg` it stacks between the notices and the main content.
- `children`: the main content.
- `accessory`: a `BottomAccessory`, phone only. From `md` show its content inline in the page.
- `toasts`: `Toast` elements. The `ToastRegion` live region is always rendered, so the first toast is announced.
- `avatar`: the Profile entry for `SideNav`. On phone, pass an `Avatar` to `TopBar` as well; `TopBar` hides its avatar from `md` up, so there's only ever one.
- `hrefs`, `onNavigate`, `onAdd`, `lang`: passed to `TabBar` and `SideNav`. Destinations are real links (`/today`, `/plan`, `/shopping`).
- `nav={false}` hides both navigations (onboarding). `narrow` caps content at `container-onboarding` (560).
- `contained`: the shell becomes its own scroller (showcases, embedded frames). In the app, leave it off so the document scrolls and mobile browsers can collapse their toolbars.
- `mainId` (default `main`): the skip-link target.

**States:** phone, tablet, desktop; with or without `aside`, `accessory`, `banner`; `nav={false}` for onboarding.

## Accessibility

- Landmarks: one `<main>`, one visible `<nav aria-label="Main">` (the other is `display: none` at each size, so it's out of the accessibility tree), the right rail as `<aside aria-label>`. The page `<h1>` lives in `TopBar`.
- The first focusable element is the skip link *Skip to main content*, hidden until focused. It moves focus to `<main tabindex="-1">`.
- DOM order is top zone (banner, header, notices) → aside → main content → toasts → bottom bar. At `lg` the aside is placed in the right column by grid areas, not by reordering the DOM, so Tab order stays notices → summary → meals.
- On route change the app moves focus to the new `<h1>` and updates `document.title`.
- Sticky parts (bottom bar, banner, header) must not hide focus: set `scroll-padding-bottom` on `html` to `size-tabbar` + `space-8` on phone, and `scroll-padding-top` to the sticky banner/header height.
- At 200% zoom a desktop gets the tablet or phone layout. Nothing scrolls horizontally except a `WeekTable`.

## Copy

| Key | EN | PL |
| --- | --- | --- |
| `shell.skip` | Skip to main content | Przejdź do treści |
| `shell.nav` (landmark name) | Main | Menu główne |
| `shell.aside.today` | Day summary | Podsumowanie dnia |

## Do / don't

- Do use one `AppShell` per page and put the page title in `TopBar`.
- Do keep notices in `notices`, above the content, never inside a collapsed panel. Allergen and no-profile notices are never hidden.
- Don't add a second navigation (top tabs, hamburger) beside `TabBar` / `SideNav`.
- Don't use `contained` in the app; it breaks the browser's own scrolling behaviour.
- Don't wrap `PhoneFrame` around web screens. Show web screens at 375, 768 and 1280 px instead.
