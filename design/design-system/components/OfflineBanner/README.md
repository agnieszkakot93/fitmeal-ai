# OfflineBanner

A thin status line at the top of every tab page that says whether the app is online and whether check-offs are waiting to sync (README §Offline, today.md, weekly-plan.md). It tells the user what still works; it never blocks. Put it in `AppShell banner` with `sticky`.

| State | Look | EN |
| --- | --- | --- |
| `none` | Nothing visible; the empty live region stays mounted | — |
| `offline` | `surface-sunken`, `wifi-off` | *You're offline. Your plan and meal check-offs still work.* + *N changes are waiting to sync.* when `pending` > 0 |
| `syncing` | `basil-soft` / `basil-ink`, `repeat` | *You're back online. Syncing N changes…* |
| `synced` | `basil-soft` / `basil-ink`, `check` | *You're back online. Everything is synced.* Hide it after about 4 s (`state="none"`). |
| `stuck` | `warning-soft`, `alert` in `warning`, *Try again* | *Some check-offs haven't synced yet.* (only after retries have failed for 24 h, per today.md) |

**Props:** `state`, `pending` (number of queued changes), `onRetry` (for `stuck`), `sticky`, `lang` (`en` / `pl`, with plural forms built in).

Offline detection: `navigator.onLine` plus a failed fetch (both, because `onLine` can be true on a captive network). Actions that need a connection (generate, swap, rebalance, import, sign-in) stay visible and show an inline `offline` `Notice` naming the action when tapped (`state.offline.action.*`); the banner doesn't list them.

## Accessibility

- `role="status"` (polite). Keep the component mounted with `state="none"` so the region exists before the first change; a region inserted together with its text often isn't announced.
- Text, not colour, carries the state; the icon is decorative.
- Sticky at the top: add its height to `scroll-padding-top` so it never covers the focused element.
- *Try again* is a real button, at least 36 px tall inside a 44 px row.
- Don't announce every sync tick: update `pending` when the count changes, not on a timer.

## Copy

| Key | EN | PL |
| --- | --- | --- |
| `state.offline.banner` | You're offline. Your plan and meal check-offs still work. | Jesteś offline. Plan i odhaczanie posiłków nadal działają. |
| `state.offline.pending` | {n, plural, one {# change is waiting to sync.} other {# changes are waiting to sync.}} | {n, plural, one {# zmiana czeka na synchronizację.} few {# zmiany czekają na synchronizację.} many {# zmian czeka na synchronizację.}} |
| `state.online.syncing` | {n, plural, one {You're back online. Syncing # change…} other {You're back online. Syncing # changes…}} | {n, plural, one {Znów jesteś online. Synchronizujemy # zmianę…} few {Znów jesteś online. Synchronizujemy # zmiany…} many {Znów jesteś online. Synchronizujemy # zmian…}} |
| `state.online.synced` | You're back online. Everything is synced. | Znów jesteś online. Wszystko jest zsynchronizowane. |
| `today.sync_stuck` | Some check-offs haven't synced yet. | Część odhaczonych posiłków jeszcze się nie zsynchronizowała. |
| `state.error.retry` | Try again | Spróbuj ponownie |

PL plurals: 1 zmiana · 2–4, 22–24 … zmiany · 5–21, 25 … zmian (and 12–14 zmian).

## Do / don't

- Do say what still works, not only that the connection is gone.
- Do keep queued check-offs on the device and send them on reconnect, then show `synced` briefly.
- Don't use `danger` for offline; it isn't an error the user caused.
- Don't hide the user's data or grey out the page while offline.
- Don't stack two banners. One component shows the current state.
