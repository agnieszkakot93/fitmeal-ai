# Working in parallel

Rules for several agents or contributors working on `develop` at the same time
(wave 1: see the task list in the PR that added this file).

- **Dependencies:** only a scaffolding PR changes `backend/pyproject.toml` and
  `uv.lock`. Feature branches don't, so lockfile conflicts can't happen. Ask for
  a dependency in the PR description instead. Wave 2 pre-adds `arq` (background
  jobs) and `cryptography` (column encryption, D13).
- **Routers:** a feature registers its API by adding one import and one entry to
  `ROUTERS` in `backend/app/main.py`. Nothing else in that file changes.
- **Migrations:** revision ids are assigned up front, and each task adds only its
  own. Wave 1: `0006` users and consent records (auth, merged). Wave 2:

  | Revision | Table(s) | Task |
  |---|---|---|
  | `0007_health_profiles` | `health_profiles` (encrypted columns, D13) | health profile |
  | `0008_plans` | `plans`, `plan_slots`, slot-status events | plans API |
  | `0009_recipe_variants` | `recipe_variants` | variants and swaps |
  | `0010_import_jobs` | `import_jobs` | async imports |
  | `0011_shopping_items` | `shopping_items` | shopping list API |

  Each sets `down_revision` to the number before it. Tasks run in parallel, so
  whoever merges second rebases the chain: merge `develop` in and point
  `down_revision` at the latest revision already on `develop` (keep your own id),
  then re-run `alembic check`.
- **CLI:** `backend/app/cli.py` stays untouched. A feature that needs a command
  puts a function in `backend/app/<feature>/cli.py`; wiring it is a follow-up.
- **Files:** each task owns its own package or folder and touches nothing else.
- **Checks before pushing:** `ruff check`, `ruff format --check`, `mypy app tests`,
  full `pytest` against Postgres, `alembic check`. Never lower existing test floors
  (`tests/test_tuning.py`, the import golden-set gate).
