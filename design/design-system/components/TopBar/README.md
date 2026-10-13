# TopBar

The web page header. It replaces the iOS `NavBar` on web: the page title as the one `<h1>`, an optional back link, and page actions. It is solid (no glass) and sits at the top of `AppShell`'s top zone.

**Props:**
- `title`: the page title, rendered as `<h1>` (`level={2}` only in showcases or nested panels).
- `large`: tab roots (Today, Plan, Shopping) use `display` (32); other pages use `title-1` (24).
- `subtitle`: one `callout` line in `ink-muted` (*Wed, 14 Oct · Day 3 of 7*).
- `back`: `{ label, href, onClick }`. A real link with a chevron and the parent page's name (*Plan*). Use it on pages below a tab root (*New plan*, a recipe). Tab roots have no back link.
- `actions`: page actions, right-aligned (*New plan* as a secondary `Button sm`, icon buttons with `Tooltip`).
- `avatar`: the phone Profile entry. Hidden inside `AppShell` from 600 px, where `SideNav` shows it.
- `sticky`: sticks to the top on `surface` with a `line` hairline (long pages such as Shopping).
- `titleId`: id for the `<h1>`, for focusing it on route change or as `aria-labelledby`.

**States:** tab root (large, avatar), sub-page (back link), with actions, sticky.

## Accessibility

- `<header>` inside `<main>`, so it isn't a banner landmark. The `<h1>` has `tabIndex=-1`: on route change the app focuses it, so screen readers announce the new page; it isn't in the Tab order.
- The back link's accessible name is *Back to Plan* / *Wróć do: Plan*: a visually hidden prefix plus the visible label, so the visible text is part of the name (2.5.3). It's a link, so browser Back and this link go to the same URL.
- Icon-only actions need an `aria-label` and, on desktop, a `Tooltip` with the same text.
- Titles wrap; they are never truncated (PL titles run about 30% longer).
- The back link and every action are at least `size-tap` (44) tall.

## Copy

| Key | EN | PL |
| --- | --- | --- |
| `topbar.back_prefix` (hidden) | Back to | Wróć do: |
| `today.title` | Today | Dzisiaj |
| `today.subtitle` | {date} · Day {n} of {total} | {date} · Dzień {n} z {total} |
| `plan.create.title` | New plan | Nowy plan |
| `plan.subtitle` | {start} – {end} · {n} days | {start} – {end} · {n} dni |

## Do / don't

- Do keep one `TopBar` and one `<h1>` per page.
- Do name the parent page in the back link, not *Back*.
- Don't put the primary action of a form in the `TopBar`. It goes at the end of the form (sticky at the bottom on phone).
- Don't use glass, and don't let content scroll under a non-sticky `TopBar`.
- Don't put more than two actions here; the rest go in a `…` menu.
