import uuid

from sqlalchemy import Column, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID

from app.db.database import Base


class ExpenseSplit(Base):
    __tablename__ = "expense_splits"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    expense_id = Column(
        UUID(as_uuid=True),
        ForeignKey("expenses.id"),
        nullable=False
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    amount = Column(
        Numeric,
        nullable=False
    )