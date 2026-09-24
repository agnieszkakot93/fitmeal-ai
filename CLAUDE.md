# FitMeal AI: working rules

See [README.md](README.md) for the repository layout and stack, and `.claude/agents/` for the agent team.

## Branch naming

Every new branch is named `<type>/<short-description>`:

- `<type>` says what kind of change it is (see the table below).
- `<short-description>` is lowercase kebab-case, a few words saying what the branch does, e.g. `recipe-url-import`.
- An issue number, when there is one, goes at the start of the description: `fix/42-negative-macro-totals`.

| Type | Use for |
|---|---|
| `feat` | A new feature or user-visible capability |
| `fix` | A bug fix |
| `chore` | Maintenance with no behavior change: dependencies, tooling, config |
| `refactor` | Restructuring code without changing behavior |
| `docs` | Documentation only |
| `test` | Adding or fixing tests only |
| `perf` | A performance improvement |
| `ci` | CI workflows and build pipelines |

Examples: `feat/weekly-plan-swap`, `fix/usda-import-duplicate-foods`, `chore/bump-fastapi`, `docs/api-auth-flow`.

Only these types are allowed. Pick the one that matches the main purpose of the branch; if a branch mixes several, it should probably be split.
