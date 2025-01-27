from datetime import timedelta

from src.api.deps import get_db
from src.core.authentication import (
    add_token_to_blacklist,
    authenticate_user,
    create_access_token,
    oauth2_scheme, get_current_user, is_token_blacklisted, create_refresh_token,
)
from src.core.config import settings
from src.crud.user import create_user
from src.schemas.user import UserCreate, UserReadSingle

from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt

router = APIRouter()


@router.post("/login")
def login(
        response: Response,
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
        )

    access_token = create_access_token(data={"user_id": str(user.id)})

    refresh_token = create_refresh_token(data={"user_id": str(user.id)})

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=not settings.DEBUG,
        samesite="lax",
        max_age=settings.JWT_REFRESH_TOKEN_EXPIRE_MINUTES
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": str(user.id),
        "role": user.role,
    }


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(user, db)


@router.post("/logout")
def logout(db: Session = Depends(get_db), current_token: str = Depends(oauth2_scheme)):
    add_token_to_blacklist(db, current_token)
    return {"message": "Successfully logged out"}


@router.post("/refresh")
async def refresh_token(
        request: Request,
        response: Response,
        db: Session = Depends(get_db),
        current_user: UserReadSingle = Depends(get_current_user)
):
    old_refresh_token = request.cookies.get("refresh_token")
    if not old_refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token provided")

    try:
        payload = jwt.decode(
            old_refresh_token,
            settings.JWT_REFRESH_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        if is_token_blacklisted(db, old_refresh_token):
            raise HTTPException(status_code=401, detail="Refresh token has been revoked")

        add_token_to_blacklist(db, old_refresh_token)

        new_access_token = create_access_token(
            data={"user_id": str(current_user.id)}
        )
        new_refresh_token = create_refresh_token(
            data={"user_id": str(current_user.id)}
        )

        response.set_cookie(
            key="refresh_token",
            value=new_refresh_token,
            httponly=True,
            secure=settings.DEBUG,
            samesite="lax",
            max_age=settings.JWT_REFRESH_TOKEN_EXPIRE_MINUTES
        )

        return {
            "access_token": new_access_token,
            "token_type": "bearer",
            "user_id": str(current_user.id),
            "role": current_user.role,
        }

    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")