from uuid import UUID

from pydantic import BaseModel


class SettlementCreate(BaseModel):
    group_id: UUID
    to_user_id: UUID
    amount: float


class SettlementResponse(BaseModel):
    id: UUID
    group_id: UUID
    from_user_id: UUID
    to_user_id: UUID
    amount: float

    model_config = {
        "from_attributes": True
    }
    
class SuggestedSettlementResponse(BaseModel):
    from_user: str
    from_user_id: UUID

    to_user: str
    to_user_id: UUID

    amount: float