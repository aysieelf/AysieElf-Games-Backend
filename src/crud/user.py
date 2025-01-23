from typing import Optional

from src.core.security import get_password_hash
from src.models.user import User
from src.schemas.user import UserCreate, UserReadSingle
from sqlalchemy.orm import Session
from src.crud.utils import validators as v
from fastapi import HTTPException
from fastapi import status



def get_by_id(db: Session, user_id: str) -> Optional[UserReadSingle]:
    """
    Retrieve a user by their ID.

    Args:
        db (Session): Database session dependency.
        user_id (str): The user's ID.

    Returns:
        UserReadSingle: The user object.

    Raises:
        HTTPException: If the user is not found.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return UserReadSingle.model_validate(db_user)

