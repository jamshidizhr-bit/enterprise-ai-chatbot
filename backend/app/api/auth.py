from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.services.auth_service import (
    create_user,
    login_user
)

from app.schemas.user import (
    UserRegister,
    UserResponse,
    UserLogin,
    Token
)

from app.services.auth_service import (
    create_user,
    login_user
)

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)

@router.post(
    "/login",
    response_model=Token
)
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    token = login_user(
        db,
        user.email,
        user.password
    )

    if token is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.post(
    "/register",
    response_model=UserResponse
)
def register(
    user: UserRegister,
    db: Session = Depends(get_db)
):

    new_user = create_user(db, user)

    if not new_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists."
        )

    return new_user