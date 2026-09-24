# FitMeal AI

Intelligent meal planning for iOS: import any recipe (social media, link, PDF) and get it adapted to your calories, macros, allergies, budget and meal-prep schedule, with a weekly plan and shopping list.

- [Product Requirements (PRD)](docs/PRD.md)
- [Development Plan: architecture, stack, infrastructure costs, sprints](docs/DEVELOPMENT_PLAN.md)
- [Backend: running locally, checks, API](backend/README.md)
- [Food data: loading USDA FoodData Central](data/README.md)

## Repository layout

```
ios/        SwiftUI app + Share Extension + local Swift packages (not started)
backend/    Python / FastAPI modular monolith + arq worker
infra/      Docker Compose, Caddy, backup scripts
data/       Food database seeds and import scripts
docs/       PRD, plans, decisions
```

## Stack at a glance

- **iOS:** Swift 6, SwiftUI (iOS 17+), SwiftData, StoreKit 2, Sign in with Apple
- **Backend:** Python 3.12, FastAPI, PostgreSQL 16, Redis, arq, SciPy/HiGHS + OR-Tools
- **AI:** Claude API (Haiku 4.5 for extraction, Sonnet 5 for PDFs/hard cases). Used for import only; nutrition math is deterministic.
- **Hosting:** Hetzner Cloud VPS (EU) + Docker Compose, Cloudflare (DNS/CDN/R2), Sentry, PostHog EU
