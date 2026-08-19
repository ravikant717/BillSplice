from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID


class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr

    model_config = {
        "from_attributes": True
    }



class Token(BaseModel):
    access_token: str
    token_type: str