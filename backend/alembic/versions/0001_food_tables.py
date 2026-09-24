"""food tables

Revision ID: 0001
Revises:
Create Date: 2026-09-24 21:00:52.132352

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0001"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")
    op.create_table(
        "food_items",
        sa.Column("id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("slug", sa.Text(), nullable=False),
        sa.Column("name_en", sa.Text(), nullable=False),
        sa.Column("name_pl", sa.Text(), nullable=False),
        sa.Column("category", sa.Text(), nullable=False),
        sa.Column("origin", sa.Text(), nullable=False),
        sa.Column("kcal", sa.Float(), nullable=False),
        sa.Column("protein_g", sa.Float(), nullable=False),
        sa.Column("fat_g", sa.Float(), nullable=False),
        sa.Column("carbs_g", sa.Float(), nullable=False),
        sa.Column("fiber_g", sa.Float(), nullable=False),
        sa.Column("water_g", sa.Float(), nullable=True),
        sa.Column("density_g_per_ml", sa.Float(), nullable=True),
        sa.Column("allergens", sa.ARRAY(sa.Text()), server_default="{}", nullable=False),
        sa.Column("effective_allergens", sa.ARRAY(sa.Text()), server_default="{}", nullable=False),
        sa.Column("culinary_roles", sa.ARRAY(sa.Text()), server_default="{}", nullable=False),
        sa.Column("substitution_groups", sa.ARRAY(sa.Text()), server_default="{}", nullable=False),
        sa.Column("source", sa.Text(), nullable=False),
        sa.Column("source_ref", sa.Text(), nullable=True),
        sa.Column("reviewed", sa.Boolean(), server_default="false", nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "kcal >= 0 AND protein_g >= 0 AND fat_g >= 0 AND carbs_g >= 0 AND fiber_g >= 0",
            name=op.f("ck_food_items_nutrients_non_negative"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_food_items")),
        sa.UniqueConstraint("slug", name=op.f("uq_food_items_slug")),
    )
    op.create_table(
        "food_aliases",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("food_id", sa.UUID(), nullable=False),
        sa.Column("lang", sa.Text(), nullable=False),
        sa.Column("alias", sa.Text(), nullable=False),
        sa.Column("alias_folded", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ["food_id"],
            ["food_items.id"],
            name=op.f("fk_food_aliases_food_id_food_items"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_food_aliases")),
        sa.UniqueConstraint(
            "food_id", "lang", "alias_folded", name=op.f("uq_food_aliases_food_id")
        ),
    )
    op.create_index(
        "ix_food_aliases_alias_folded_trgm",
        "food_aliases",
        ["alias_folded"],
        unique=False,
        postgresql_using="gin",
        postgresql_ops={"alias_folded": "gin_trgm_ops"},
    )
    op.create_table(
        "food_derivations",
        sa.Column("food_id", sa.UUID(), nullable=False),
        sa.Column("parent_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["food_id"],
            ["food_items.id"],
            name=op.f("fk_food_derivations_food_id_food_items"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["parent_id"],
            ["food_items.id"],
            name=op.f("fk_food_derivations_parent_id_food_items"),
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("food_id", "parent_id", name=op.f("pk_food_derivations")),
    )
    op.create_table(
        "food_packages",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("food_id", sa.UUID(), nullable=False),
        sa.Column("size_g", sa.Float(), nullable=False),
        sa.CheckConstraint("size_g > 0", name=op.f("ck_food_packages_size_positive")),
        sa.ForeignKeyConstraint(
            ["food_id"],
            ["food_items.id"],
            name=op.f("fk_food_packages_food_id_food_items"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_food_packages")),
    )
    op.create_table(
        "food_portions",
        sa.Column("food_id", sa.UUID(), nullable=False),
        sa.Column("unit", sa.Text(), nullable=False),
        sa.Column("grams", sa.Float(), nullable=False),
        sa.CheckConstraint("grams > 0", name=op.f("ck_food_portions_grams_positive")),
        sa.ForeignKeyConstraint(
            ["food_id"],
            ["food_items.id"],
            name=op.f("fk_food_portions_food_id_food_items"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("food_id", "unit", name=op.f("pk_food_portions")),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("food_portions")
    op.drop_table("food_packages")
    op.drop_table("food_derivations")
    op.drop_index(
        "ix_food_aliases_alias_folded_trgm",
        table_name="food_aliases",
        postgresql_using="gin",
        postgresql_ops={"alias_folded": "gin_trgm_ops"},
    )
    op.drop_table("food_aliases")
    op.drop_table("food_items")
    # ### end Alembic commands ###
