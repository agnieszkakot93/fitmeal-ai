"""food trace status

Revision ID: 0003
Revises: 0002
Create Date: 2026-09-24 23:10:41.512903

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0003"
down_revision: str | Sequence[str] | None = "0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# Frozen copy of TraceStatus at this revision; migrations never import app code.
_STATUSES = "'unknown', 'none_declared', 'declared'"


def upgrade() -> None:
    """Upgrade schema."""
    # Existing rows get "unknown": nobody has checked their traces yet.
    op.add_column(
        "food_items",
        sa.Column("trace_status", sa.Text(), server_default="unknown", nullable=False),
    )
    op.add_column(
        "food_items",
        sa.Column("effective_trace_status", sa.Text(), server_default="unknown", nullable=False),
    )
    op.create_check_constraint(
        op.f("ck_food_items_trace_status_valid"),
        "food_items",
        f"trace_status IN ({_STATUSES}) AND effective_trace_status IN ({_STATUSES})",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(op.f("ck_food_items_trace_status_valid"), "food_items", type_="check")
    op.drop_column("food_items", "effective_trace_status")
    op.drop_column("food_items", "trace_status")
