from fastapi import APIRouter, Depends, Response
from sqlmodel import Session

from app.db.database import get_db, settings
from app.models.user import User
from app.routes.dependencies import get_current_user
from app.schemas.user import UserRegister, UserResponse, UserLogin
from app.services.auth_service import register_user, login_user, issue_token_for_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

IS_PRODUCTION = settings.ENVIRONMENT == "production"
COOKIE_MAX_AGE = 60 * 60 * 24 * 7  # 7 days

def set_auth_cookie(response: Response, access_token: str) -> None:
    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=COOKIE_MAX_AGE,
        path="/", 
        expires=COOKIE_MAX_AGE, 
        httponly=True,
        secure=IS_PRODUCTION,        # True in production (HTTPS). Required when samesite="none".
        samesite="none" if IS_PRODUCTION else "lax",
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
    user_data: UserLogin, 
    db: Session = Depends(get_db),
):
    user = login_user(
        user_data.email,
        user_data.password,
        db,
    )

    token = issue_token_for_user(user)

    set_auth_cookie(response, token["access_token"])

    return user

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        path="/",
        httponly=True,
        secure=IS_PRODUCTION,
        samesite="none" if IS_PRODUCTION else "lax"
    )

    return {
        "message": "Logged out"
    }
    
@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return current_user