# app/models/expense_split.py

import uuid
from decimal import Decimal

from sqlmodel import SQLModel, Field


class ExpenseSplit(SQLModel, table=True):
    __tablename__ = "expense_splits"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )

    expense_id: uuid.UUID = Field(
        foreign_key="expenses.id",
        nullable=False
    )

    user_id: uuid.UUID = Field(
        foreign_key="users.id",
        nullable=False
    )

    amount: Decimal = Field(
        nullable=False
    )