"""recipe variants in plan slots

Revision ID: 0009
Revises: 0007
Create Date: 2026-10-14 10:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0009"
down_revision: str | Sequence[str] | None = "0007"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "plan_slot_variants",
        sa.Column("slot_id", sa.Integer(), nullable=False),
        sa.Column("variant_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["slot_id"],
            ["plan_slots.id"],
            name=op.f("fk_plan_slot_variants_slot_id_plan_slots"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["variant_id"],
            ["recipe_variants.id"],
            name=op.f("fk_plan_slot_variants_variant_id_recipe_variants"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("slot_id", name=op.f("pk_plan_slot_variants")),
    )
    op.create_index(
        op.f("ix_plan_slot_variants_variant_id"),
        "plan_slot_variants",
        ["variant_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_plan_slot_variants_variant_id"), table_name="plan_slot_variants")
    op.drop_table("plan_slot_variants")
