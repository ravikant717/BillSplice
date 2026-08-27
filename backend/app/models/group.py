import uuid
from datetime import datetime

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func


class Group(SQLModel, table=True):
    __tablename__ = "groups"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )

    name: str = Field(
        nullable=False
    )

    invite_code: str = Field(
        unique=True,
        nullable=False
    )

    created_by: uuid.UUID = Field(
        foreign_key="users.id",
        nullable=False
    )

    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now()
        )
    )