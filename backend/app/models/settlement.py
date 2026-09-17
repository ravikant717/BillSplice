import uuid
from datetime import datetime
from decimal import Decimal

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime, Numeric
from sqlalchemy.sql import func


class Settlement(SQLModel, table=True):
    __tablename__ = "settlements"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )

    group_id: uuid.UUID = Field(
        foreign_key="groups.id",
        nullable=False
    )

    from_user_id: uuid.UUID = Field(
        foreign_key="users.id",
        nullable=False
    )

    to_user_id: uuid.UUID = Field(
        foreign_key="users.id",
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