from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import User
from app.api.dependencies import get_current_user
from app.schemas.user import UserRegister, UserResponse, UserLogin, Token
from app.services.auth_service import register_user, login_user, issue_token_for_user
from app.db.database import get_db

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

COOKIE_MAX_AGE = 60 * 60 * 24 * 7  # 7 days


def set_auth_cookie(response: Response, access_token: str) -> None:
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,        # True in production (HTTPS). Required when samesite="none".
        samesite="none",
        max_age=COOKIE_MAX_AGE,
        path="/",
    )


@router.post("/register", response_model=UserResponse, status_code=201)
def register(
    response: Response,
    user_data: UserRegister,
    db: Session = Depends(get_db),
):
    user = register_user(user_data, db)

    token = issue_token_for_user(user)

    set_auth_cookie(response, token["access_token"])

    return user

@router.post("/login")
def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    token = login_user(
        form_data.username,
        form_data.password,
        db,
    )

    set_auth_cookie(response, token["access_token"])

    return {
        "message": "Login successful"
    }

@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        path="/",
        httponly=True,
        samesite="none",
        secure=True
    )

    return {
        "message": "Logged out"
    }