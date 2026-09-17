from typing import Generic, TypeVar

from pydantic import BaseModel, Field

ItemT = TypeVar("ItemT")


class PaginatedResponse(BaseModel, Generic[ItemT]):
    items: list[ItemT]
    page: int
    page_size: int
    total: int
    pages: int


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)