"""add query indexes

Revision ID: 9d4a7e2c1f6b
Revises: ff8ea26c7538
Create Date: 2026-09-05 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "9d4a7e2c1f6b"
down_revision: Union[str, Sequence[str], None] = "ff8ea26c7538"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(
        "ix_group_members_user_group",
        "group_members",
        ["user_id", "group_id"],
    )
    op.create_index(
        "ix_group_members_group_user",
        "group_members",
        ["group_id", "user_id"],
    )
    op.create_index(
        "ix_expenses_group_created_id",
        "expenses",
        ["group_id", "created_at", "id"],
    )
    op.create_index(
        "ix_expense_splits_expense_id",
        "expense_splits",
        ["expense_id"],
    )
    op.create_index(
        "ix_settlements_group_id",
        "settlements",
        ["group_id"],
    )
    op.create_index(
        "ix_settlements_from_user_group",
        "settlements",
        ["from_user_id", "group_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_settlements_from_user_group", table_name="settlements")
    op.drop_index("ix_settlements_group_id", table_name="settlements")
    op.drop_index("ix_expense_splits_expense_id", table_name="expense_splits")
    op.drop_index("ix_expenses_group_created_id", table_name="expenses")
    op.drop_index("ix_group_members_group_user", table_name="group_members")
    op.drop_index("ix_group_members_user_group", table_name="group_members")
