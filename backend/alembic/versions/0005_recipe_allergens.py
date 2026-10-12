"""recipe allergens

Revision ID: 0005
Revises: 0004
Create Date: 2026-10-12 19:48:32.766082

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0005"
down_revision: str | Sequence[str] | None = "0004"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# Frozen copy of TraceStatus at this revision; migrations never import app code.
_STATUSES = "'unknown', 'none_declared', 'declared'"


def upgrade() -> None:
    """Upgrade schema."""
    # Existing recipes get "unknown" until `donut-admin recipes import` refreshes them.
    op.add_column(
        "recipes", sa.Column("allergens", sa.ARRAY(sa.Text()), server_default="{}", nullable=False)
    )
    op.add_column(
        "recipes",
        sa.Column("may_contain", sa.ARRAY(sa.Text()), server_default="{}", nullable=False),
    )
    op.add_column(
        "recipes", sa.Column("trace_status", sa.Text(), server_default="unknown", nullable=False)
    )
    op.create_check_constraint(
        op.f("ck_recipes_trace_status_valid"), "recipes", f"trace_status IN ({_STATUSES})"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(op.f("ck_recipes_trace_status_valid"), "recipes", type_="check")
    op.drop_column("recipes", "trace_status")
    op.drop_column("recipes", "may_contain")
    op.drop_column("recipes", "allergens")
