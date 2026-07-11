from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import User
from app.api.dependencies import get_current_user
from app.schemas.user import UserRegister, UserResponse, UserLogin, Token
from app.services.auth_service import register_user, login_user
from app.db.database import get_db

router = APIRouter(
    prefix="/auth", 
    tags=["Authentication"]
)


@router.post("/register", response_model=UserResponse, status_code=201)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    user = register_user(user_data, db)
    return user 

@router.post(
    "/login",
    response_model=Token,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    return login_user(
        form_data.username,
        form_data.password,
        db,
    )

@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)): 
    return current_user