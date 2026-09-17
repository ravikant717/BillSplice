from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserRegister
from app.core.security import (hash_password, verify_password, create_access_token)

from fastapi import HTTPException


def _issue_token(user: User) -> dict:
    """Build a token response for an already-authenticated user.

    Centralizing this means register and login always produce a token
    the exact same way, instead of register re-querying the DB and
    re-verifying the password it just set.
    """
    access_token = create_access_token(
        {
            "sub": str(user.id)
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


def register_user(user_data: UserRegister, db: Session):

    # Check if email already exists
    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    # Hash the password
    hashed_password = hash_password(user_data.password)

    # Create a User
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=hashed_password
    )

    # Save to db
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # return the user
    return new_user


def login_user(
    email: str,
    password: str,
    db: Session,
):

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    if not verify_password(
        password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    return user


def issue_token_for_user(user: User) -> dict:
    return _issue_token(user)