from uuid import UUID
from sqlmodel import SQLModel
from decimal import Decimal 

class ExpenseCreate(SQLModel):
    group_id: UUID
    title: str
    amount: Decimal
    receipt_url: str | None = None 
    


class ExpenseResponse(SQLModel):
    id: UUID
    title: str
    amount: Decimal
    paid_by: UUID
    receipt_url: str | None = None 
    

    model_config = {
        "from_attributes": True
    }
    
