from sqlmodel import SQLModel
from decimal import Decimal
from datetime import date as Date


class ReceiptItem(SQLModel):
    name: str
    price: Decimal


class ReceiptData(SQLModel):
    merchant: str | None = None
    date: Date | None = None
    total: Decimal | None = None
    items: list[ReceiptItem] = []