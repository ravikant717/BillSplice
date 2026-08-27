from uuid import UUID
from pydantic import EmailStr
from sqlmodel import SQLModel


class UserRegister(SQLModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(SQLModel):
    email: EmailStr
    password: str


class UserResponse(SQLModel):
    id: UUID
    name: str
    email: EmailStr


class Token(SQLModel):
    access_token: str
    token_type: str