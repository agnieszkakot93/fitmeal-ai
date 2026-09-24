# FitMeal AI — backend

FastAPI modular monolith. See [../docs/DEVELOPMENT_PLAN.md](../docs/DEVELOPMENT_PLAN.md) for the architecture.

## Run locally

With Docker (Postgres, Redis and the API with live reload):

```bash
docker compose -f infra/docker-compose.yml up --build    # from the repo root
open http://localhost:8000/docs
```

Or with a local Python, using Postgres/Redis from Compose:

```bash
docker compose -f infra/docker-compose.yml up -d postgres redis
cd backend
uv sync
uv run alembic upgrade head
uv run uvicorn app.main:app --reload
```

To load ingredient data, see [../data/README.md](../data/README.md).

## Checks

```bash
uv run pytest                 # needs Postgres: uses the fitmeal_test database
uv run ruff check . && uv run ruff format --check .
uv run mypy app tests
uv run alembic check          # models and migrations in sync
```

New migration after changing models: `uv run alembic revision --autogenerate -m "..."`.

## Layout

```
app/
  core/        settings, database session, text folding
  nutrition/   pure engine: units → grams, nutrient math, allergens (no I/O)
  foods/       food tables, curated-list + USDA FDC importer, search and nutrition APIs
  cli.py       fitmeal-admin commands
alembic/       migrations
tests/         unit tests + API/DB tests against real Postgres
```

## API so far

| Endpoint | What it does |
|---|---|
| `GET /healthz` | DB connectivity check |
| `GET /v1/foods/search?q=pierś&lang=pl` | Fuzzy ingredient search over PL/EN aliases, diacritics-insensitive |
| `GET /v1/foods/{slug}` | Ingredient detail: nutrition, allergens (incl. inherited), portions, packages |
| `POST /v1/nutrition/calculate` | Ingredient list (`amount` + any unit such as `łyżka`, `szklanka`, `szt`) → grams, totals, per serving. Lines that can't be converted come back together as a 422. |
