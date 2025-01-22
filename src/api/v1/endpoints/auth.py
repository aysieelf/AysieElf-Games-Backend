from src.api.deps import get_db
from src.core.authentication import (
    add_token_to_blacklist,
    authenticate_user,
    create_access_token,
    oauth2_scheme,
)

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token = create_access_token(data={"user_id": str(user.id)})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": str(user.id),
        "role": user.role,
    }


@router.post("/logout")
def logout(db: Session = Depends(get_db), current_token: str = Depends(oauth2_scheme)):
    add_token_to_blacklist(db, current_token)
    return {"message": "Successfully logged out"}
