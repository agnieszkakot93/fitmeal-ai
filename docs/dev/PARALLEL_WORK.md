# Working in parallel

Rules for several agents or contributors working on `develop` at the same time
(wave 1: see the task list in the PR that added this file).

- **Dependencies:** only a scaffolding PR changes `backend/pyproject.toml` and
  `uv.lock`. Feature branches don't, so lockfile conflicts can't happen. Ask for
  a dependency in the PR description instead.
- **Routers:** a feature registers its API by adding one import and one entry to
  `ROUTERS` in `backend/app/main.py`. Nothing else in that file changes.
- **Migrations:** revision ids are assigned up front. Wave 1: `0006` is reserved
  for users and consent records (auth). Nobody else adds a migration in wave 1.
- **CLI:** `backend/app/cli.py` stays untouched. A feature that needs a command
  puts a function in `backend/app/<feature>/cli.py`; wiring it is a follow-up.
- **Files:** each task owns its own package or folder and touches nothing else.
- **Checks before pushing:** `ruff check`, `ruff format --check`, `mypy app tests`,
  full `pytest` against Postgres, `alembic check`. Never lower existing test floors
  (`tests/test_tuning.py`, the import golden-set gate).
