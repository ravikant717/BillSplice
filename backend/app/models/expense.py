import uuid
from decimal import Decimal
from datetime import datetime

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime, Numeric
from sqlalchemy.sql import func


class Expense(SQLModel, table=True):
    __tablename__ = "expenses"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )

    group_id: uuid.UUID = Field(
        foreign_key="groups.id",
        nullable=False
    )

    paid_by: uuid.UUID = Field(
        foreign_key="users.id",
        nullable=False
    )

    title: str = Field(
        nullable=False
    )

    amount: Decimal = Field(
        sa_column=Column(Numeric, nullable=False)
    )

    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now()
        )
    )