# Rename plan: FitMeal AI → Donut

The Product Owner approved **Donut** as the final brand on 2026-10-06 ([NAME_RESEARCH.md](NAME_RESEARCH.md)). This plan says what gets renamed, in what order, and what waits.

The availability checks are still open (NAME_RESEARCH.md §8.6.3). The plan is ordered so nothing hard to undo happens before the matching check passes.

## Inventory (develop, 2026-10-06)

| Form | Where | Count |
|---|---|---|
| `FitMeal AI` / `FitMeal` (brand in prose) | README, CLAUDE.md, docs/, `.claude/agents/`, design system (72 files), backend README, data README | ~170 |
| `fitmeal` (technical identifiers) | `backend/pyproject.toml` (`fitmeal-backend`, `fitmeal-admin`), DB user and name, Redis URL, CI workflow, infra | ~50 |
| `FITMEAL_` (env prefix) | `backend/app/core/config.py`, `.env.example`, CI workflow, infra | ~18 |
| iOS display name, bundle ID | `ios/` not started yet | 0 |
| Repository name `fitmeal-ai` | GitHub | 1 |

## Phase 1: user-facing text (now)

Safe to do now, easy to revert, no external dependency.

1. **Design system** (`design/design-system/`): brand name in README, component READMEs and previews, plus the `window.FitMeal` bundle global. Owner: `product-designer`. The bundle global is a code identifier: rename it in the same PR as every file that references it.
2. **Product docs**: README, `docs/PRD.md`, `docs/DEVELOPMENT_PLAN.md`, backend and data READMEs. Use "Donut" as the brand and keep "FitMeal AI" once as "formerly FitMeal AI" in the README for history.
3. **Agent definitions and CLAUDE.md**: update the brand name in `.claude/agents/*.md` and CLAUDE.md. Replace the "do not rename until approved" rule in CLAUDE.md with a pointer to this plan.
4. **Copy**: PL/EN strings use "Donut". The store title target is "Donut: Meal Planner & Macros" (28 characters).

## Phase 2: technical identifiers (after Phase 1 merges)

Mechanical, but touches CI and local setups. Do it in one PR with a note to contributors.

- `backend/pyproject.toml`: `fitmeal-backend` → `donut-backend`; CLI `fitmeal-admin` → `donut-admin`; regenerate `uv.lock` with `uv lock`.
- Env prefix `FITMEAL_` → `DONUT_` in `config.py`, `.env.example`, CI and infra. Contributors must update their local `.env`.
- Dev and CI database user and name `fitmeal` / `fitmeal_test` → `donut` / `donut_test` (dev only, so no data migration is needed).

## Phase 3: external identities (each only after its check passes)

| Item | Gate (NAME_RESEARCH.md §8.6.3) |
|---|---|
| Register `donut.app` / `getdonut.com` / `donut.pl` | Domain check |
| File trademark (EU, PL; classes 9, 42, 44) | TMview/EUIPO search plus attorney view on Donut for Slack |
| iOS bundle ID (e.g. `app.donut.ios`) and App Store name | App Store Connect name check. The bundle ID can't be changed after the first App Store upload, so set it once the domain is secured. |
| Social handles | Handle check, PO decides |
| Rename the GitHub repo `fitmeal-ai` | Optional; GitHub redirects the old URL |

Domains, trademarks and accounts are purchased or registered by the Product Owner, not by agents.

## Risks

- The trademark and App Store checks may still fail (Donut for Slack is the main conflict). Phases 1 and 2 are cheap to redo if so; Phase 3 isn't, which is why it's gated.
- Phase 2 breaks local `.env` files until contributors update the prefix.
