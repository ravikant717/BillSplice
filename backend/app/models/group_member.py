import uuid
from datetime import datetime

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func


class GroupMember(SQLModel, table=True):
    __tablename__ = "group_members"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )

    group_id: uuid.UUID = Field(
        foreign_key="groups.id",
        nullable=False
    )

    user_id: uuid.UUID = Field(
        foreign_key="users.id",
        nullable=False
    )

    joined_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now()
        )
    )