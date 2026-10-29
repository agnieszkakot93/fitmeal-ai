"""recipes and recipe variants: foreign keys to users, deleted with the account

Before this, private recipes and variants pointed at users without a foreign
key, so account deletion depended on ``erase()`` remembering them. Rows whose
owner no longer exists are already orphans of a deleted account; they are
removed so the constraint can be added (GDPR Art. 17).

Revision ID: 0012
Revises: 0011
Create Date: 2026-10-29 12:00:00.000000

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0012"
down_revision: str | Sequence[str] | None = "0011"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        "DELETE FROM recipe_variants WHERE user_id IS NOT NULL"
        " AND user_id NOT IN (SELECT id FROM users)"
    )
    op.execute(
        "DELETE FROM recipes WHERE owner_user_id IS NOT NULL"
        " AND owner_user_id NOT IN (SELECT id FROM users)"
    )
    op.create_foreign_key(
        op.f("fk_recipes_owner_user_id_users"),
        "recipes",
        "users",
        ["owner_user_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        op.f("fk_recipe_variants_user_id_users"),
        "recipe_variants",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        op.f("fk_recipe_variants_user_id_users"), "recipe_variants", type_="foreignkey"
    )
    op.drop_constraint(op.f("fk_recipes_owner_user_id_users"), "recipes", type_="foreignkey")
