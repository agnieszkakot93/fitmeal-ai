# InstallPrompt

A small card that offers to install Donut as a PWA so the plan works offline. It is offered **once, after the first plan** (README §Offline), sits in the notices zone of Today or Plan, and **never blocks**: no modal, no overlay, no countdown. Neutral look (`surface-sunken`, like an `offline`-tone `Notice`), never paprika or basil fill.

**Props:**
- `platform`:
  - `prompt`: the browser fired `beforeinstallprompt`. Shows *Install Donut*; `onInstall` calls the saved event's `prompt()`.
  - `ios`: iOS / iPadOS Safari (no install event). Shows the Share → *Add to Home Screen* steps instead of a button.
  - `none`: renders nothing (already installed: `display-mode: standalone`; or unsupported browser).
- `onInstall`, `onDismiss` (*Not now*), `lang`.

**When to show:** after the first plan is generated and the user is signed in; not during onboarding; not while a Dialog or Sheet is open; not when offline. After *Not now* or a finished install, don't show it again in this browser (remember it in app state). Profile can keep a permanent *Install Donut* row.

**States:** install button (Chromium, Edge, Samsung Internet), iOS steps, hidden.

## Accessibility

- A `<section>` labelled by its title. Not a live region and not focused on appear: it is part of the page, in DOM order after the other notices.
- Both actions are real buttons with visible text; *Not now* is a quiet button, not an × icon.
- The iOS steps are text (no screenshot of Safari), so they read and translate correctly.
- No motion on appear.

## Copy

| Key | EN | PL |
| --- | --- | --- |
| `state.install.title` | Use your plan offline | Korzystaj z planu offline |
| `state.install.body` | Add Donut to your home screen to use your plan without a connection. | Dodaj Donut do ekranu początkowego, aby korzystać z planu bez internetu. |
| `state.install.cta` | Install Donut | Zainstaluj Donut |
| `state.install.ios_steps` | In Safari, tap Share, then Add to Home Screen. | W Safari stuknij Udostępnij, a potem Do ekranu początkowego. |
| `common.not_now` | Not now | Nie teraz |

## Do / don't

- Do say the benefit (the plan works offline) in plain words.
- Do respect *Not now* permanently for this browser.
- Don't show it on the first visit, before value, or more than once.
- Don't make install a condition for any feature. Everything works in a browser tab.
- Don't promise that data is backed up by installing; installing doesn't move the profile (that is `ProfileFileCard`).
