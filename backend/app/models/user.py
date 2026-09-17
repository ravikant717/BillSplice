import uuid
from datetime import datetime

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )

    name: str = Field(
        nullable=False
    )

    email: str = Field(
        unique=True,
        nullable=False,
        index=True
    )

    password_hash: str = Field(
        nullable=False
    )

    avatar_url: str | None = Field(
        default=None,
        nullable=True
    )

    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now()
        )
    )