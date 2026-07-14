from uuid import UUID
from pydantic import BaseModel


class GroupDetailResponse(BaseModel):
    id: UUID
    name: str
    invite_code: str
    members: list[str]