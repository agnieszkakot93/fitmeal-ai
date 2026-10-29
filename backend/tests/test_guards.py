"""Rules every new endpoint and table must follow, checked here so nobody has to remember them.

If one of these fails on a new route or column, fix the code. Add to an
allowlist only when the exception is deliberate, with the reason next to it.
"""

from __future__ import annotations

from fastapi.dependencies.models import Dependant
from fastapi.routing import APIRoute

from app.auth.deps import current_user
from app.auth.routing import HideInputRoute
from app.core.db import Base
from app.main import create_app

# Public endpoints: no account needed. Prefixes, matched against the route path.
PUBLIC_PREFIXES = (
    "/v1/auth/",  # signing in and refreshing tokens
    "/v1/foods/",  # food database
    "/v1/nutrition/",  # stateless calculator
    "/v1/recipes",  # shared catalog; private imports are not served here
)
PUBLIC_PATHS = {"/healthz"}


def _api_routes() -> list[APIRoute]:
    return [r for r in create_app().routes if isinstance(r, APIRoute)]


def _depends_on(dependant: Dependant, target: object) -> bool:
    return any(d.call is target or _depends_on(d, target) for d in dependant.dependencies)


def _is_public(path: str) -> bool:
    return path in PUBLIC_PATHS or path.startswith(PUBLIC_PREFIXES)


def test_every_private_route_requires_a_user() -> None:
    missing = [
        f"{sorted(r.methods or ())} {r.path}"
        for r in _api_routes()
        if not _is_public(r.path) and not _depends_on(r.dependant, current_user)
    ]
    assert not missing, (
        "These routes don't take `user: CurrentUser` (app.auth.deps). Add it, or, if the "
        f"route is meant to be public, add it to PUBLIC_PREFIXES with a reason: {missing}"
    )


def test_every_v1_route_hides_submitted_values_in_422s() -> None:
    missing = [
        r.path
        for r in _api_routes()
        if r.path.startswith("/v1/") and not isinstance(r, HideInputRoute)
    ]
    assert not missing, (
        "Create the router with `APIRouter(..., route_class=HideInputRoute)` "
        f"(app.auth.routing) so validation errors don't echo tokens or health data: {missing}"
    )


def test_every_user_column_is_deleted_with_the_account() -> None:
    """Account deletion (GDPR Art. 17) relies on ON DELETE CASCADE to users.id."""
    missing = []
    for table in Base.metadata.sorted_tables:
        if table.name == "users":
            continue
        for column in table.columns:
            if column.name != "user_id" and not column.name.endswith("_user_id"):
                continue
            ok = any(
                fk.column.table.name == "users" and fk.ondelete == "CASCADE"
                for fk in column.foreign_keys
            )
            if not ok:
                missing.append(f"{table.name}.{column.name}")
    assert not missing, (
        "Point these at the account with "
        '`ForeignKey("users.id", ondelete="CASCADE")` and add a migration: '
        f"{missing}"
    )
