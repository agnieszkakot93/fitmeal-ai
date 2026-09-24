"""food may contain

Revision ID: 0002
Revises: 0001
Create Date: 2026-09-24 21:49:09.827478

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0002"
down_revision: str | Sequence[str] | None = "0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "food_items",
        sa.Column("may_contain", sa.ARRAY(sa.Text()), server_default="{}", nullable=False),
    )
    op.add_column(
        "food_items",
        sa.Column(
            "effective_may_contain", sa.ARRAY(sa.Text()), server_default="{}", nullable=False
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("food_items", "effective_may_contain")
    op.drop_column("food_items", "may_contain")
