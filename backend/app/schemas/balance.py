from pydantic import BaseModel

class OverallBalanceResponse(BaseModel):
    balance: float
class BalanceResponse(BaseModel): 
    user: str 
    balance: float

