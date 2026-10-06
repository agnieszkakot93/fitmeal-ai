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

## Branch naming

New branches are named `<type>/<short-description>`, where type is one of `feat`, `fix`, `chore`, `refactor`, `docs`, `test`, `perf`, `ci` (e.g. `feat/weekly-plan-swap`, `fix/usda-import-duplicate-foods`). Full rules in [CLAUDE.md](CLAUDE.md#branch-naming).

Branches are deleted (on GitHub and locally) once their PR is merged; `main` and `develop` are kept. See [CLAUDE.md](CLAUDE.md#deleting-branches-after-merge).

## Stack at a glance

- **iOS:** Swift 6, SwiftUI (iOS 17+), SwiftData, StoreKit 2, Sign in with Apple
- **Backend:** Python 3.12, FastAPI, PostgreSQL 16, Redis, arq, SciPy/HiGHS + OR-Tools
- **AI:** Claude on AWS Bedrock, EU region (Haiku 4.5 for extraction, Sonnet 5 for long texts/hard cases). Used for import only; nutrition math is deterministic.
- **Hosting:** Hetzner Cloud VPS (EU) + Docker Compose, Cloudflare (DNS/CDN/R2), Sentry (EU). No analytics SDK; the health profile stays on the phone.

## Claude Code agent team

Subagents in [`.claude/agents/`](.claude/agents) cover the roles on this project. Claude Code picks them automatically from their descriptions, or you can ask for one by name ("have the security-engineer review this").

| Agent | Owns |
|---|---|
| `engineering-manager` | Breaking work into tasks, sequencing, scope checks against the PRD and plan, Definition of Done |
| `mobile-architect` | `ios/`: SwiftUI, Share Extension, SwiftData, StoreKit 2, OpenAPI client |
| `backend-engineer` | `backend/`, `data/`, `infra/`: FastAPI, Postgres/Alembic, nutrition engine, optimizer, import pipeline |
| `product-designer` | Flows, screen specs, PL/EN copy, explainability, paywall, accessibility |
| `security-engineer` | Read-only reviews: auth, payments, GDPR health data, SSRF, LLM prompt safety |
| `qa-engineer` | Test plans, property-based tests, golden set and LLM evals, acceptance checks |
| `brand-researcher` | Brand naming research: name concepts, store/domain/trademark/handle checks, PL/EN language checks, [naming report](docs/branding/NAME_RESEARCH.md) |
