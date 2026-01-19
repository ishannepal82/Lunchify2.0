"""Initial migration for order tables."""

from alembic import op
import sqlalchemy as sa


revision = "001_initial_orders"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create initial schema for orders."""
    op.create_table(
        "orders",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("restaurant_id", sa.UUID(), nullable=False),
        sa.Column("items", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("total_price", sa.Float(), nullable=False),
        sa.Column("delivery_address", sa.String(), nullable=False),
        sa.Column("special_instructions", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_orders_user_id", "orders", ["user_id"])
    op.create_index("ix_orders_restaurant_id", "orders", ["restaurant_id"])
    op.create_index("ix_orders_status", "orders", ["status"])


def downgrade() -> None:
    """Drop orders table."""
    op.drop_index("ix_orders_status", "orders")
    op.drop_index("ix_orders_restaurant_id", "orders")
    op.drop_index("ix_orders_user_id", "orders")
    op.drop_table("orders")
