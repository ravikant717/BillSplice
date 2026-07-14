from uuid import UUID

from pydantic import BaseModel


class ExpenseCreate(BaseModel):
    group_id: UUID
    title: str
    amount: float


class ExpenseResponse(BaseModel):
    id: UUID
    title: str
    amount: float
    paid_by: UUID

    model_config = {
        "from_attributes": True
    }
    
