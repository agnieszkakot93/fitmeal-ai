# Donut: web app

Mobile-first responsive PWA (Dev Plan D11, §3.1): Vite + React + TypeScript (strict), React Router, react-intl (PL default, EN), a typed client generated from the backend's OpenAPI, and a Workbox service worker.

## Run locally

```bash
cd web
pnpm install
pnpm dev                 # http://localhost:5173, proxies /v1 to the API on :8000
```

The API (see [../backend/README.md](../backend/README.md)) runs separately. Set `VITE_API_BASE_URL` to call an API on another origin; by default the app calls its own origin (Caddy in production, the Vite proxy in dev).

## Checks

```bash
pnpm lint                # eslint + prettier --check
pnpm typecheck           # tsc -b
pnpm test                # Vitest unit tests
pnpm build && pnpm test:e2e   # Playwright smoke test, mobile + desktop, against the build
```

CI runs all of these in `.github/workflows/web.yml`.

## API client

`src/api/schema.d.ts` is generated, never edited by hand. After the backend API changes:

```bash
pnpm api:generate        # needs uv; exports app.openapi() to openapi.json, then runs openapi-typescript
```

Commit `openapi.json` and `src/api/schema.d.ts`; CI fails if they don't match the backend. The script imports the FastAPI app read-only.

Use the client from `src/api/client.ts` (`api.GET("/v1/foods/search", …)`). Auth (`src/api/session.ts`): the access JWT stays in memory; on a 401 the client refreshes once through `POST /v1/auth/refresh` with the HttpOnly cookie scoped to `/v1/auth`, then retries. Tokens never go to localStorage, sessionStorage or IndexedDB.

## Layout

```
src/
  app/            entry pieces: routes, Layout (AppShell), paths
  design-system/  loads design/design-system/ (bundle.js, bundle.css, typings); not a copy
  api/            generated schema, client, auth session
  i18n/           message files (pl.json, en.json), LocaleProvider, useT
  storage/        IndexedDB wrapper (stub)
  sw/             service worker (Workbox) and its registration
  features/       one folder per screen (placeholders for now)
build/            build-time helpers: tokens.json → CSS variables
e2e/              Playwright
```

- **Design system:** components come from `window.Donut`, loaded from `../design/design-system/components/bundle.js`, typed by its `index.d.ts`. CSS variables are generated at build time from `tokens.json` (`virtual:donut-tokens.css`).
- **Copy:** every string is in `src/i18n/messages/*.json`, with the same keys in both files (a unit test checks this). Use the spec's keys (`today.title`, `onb.welcome.title` …) where a spec defines them.
- **Routes:** one URL per screen; a route's `handle` sets its title, current tab and whether the navigation is shown.
