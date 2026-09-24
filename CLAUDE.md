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

## Deleting branches after merge

A branch is deleted as soon as its pull request is merged, both on GitHub and locally. The long-lived branches `main` and `develop` are never deleted.

- **Remote:** press "Delete branch" on the merged PR, or `git push origin --delete <branch>`. Turning on "Automatically delete head branches" in the repository settings does this for every PR.
- **Local:** `git switch develop && git pull && git branch -d <branch>`, then `git fetch --prune` to drop stale remote-tracking refs.
- Follow-up work goes on a new branch cut from the latest `develop`, never on the merged one.

## Brand Research

Use the brand-researcher subagent for:

- Product and competitor research.
- App naming and brand positioning.
- Domain and trademark investigation.
- International naming considerations.

The brand-researcher reports to the Engineering Manager.

All findings must be documented in:
docs/branding/NAME_RESEARCH.md

Brand selection requires Product Owner approval.

Do not rename application identifiers, domains,
packages, or product assets until the final name
has been approved.
