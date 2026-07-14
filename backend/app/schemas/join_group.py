from pydantic import BaseModel

class JoinGroupRequest(BaseModel): 
    invite_code: str