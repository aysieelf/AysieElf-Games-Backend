from typing import Optional

from src.core.security import get_password_hash
from src.crud.utils import validators as v
from src.models.user import User
from src.schemas.user import UserCreate, UserReadSingle

from fastapi import HTTPException, status
from sqlalchemy.orm import Session


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


def create_user(user: UserCreate, db: Session) -> UserReadSingle:
    """
    Create a new user with the provided data.

    Args:
        user (UserCreate): The user data to create.
        db (Session): The database session.

    Returns:
        User: The created user object.
    """
    v.user_email_exists(db, user.email)

    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # send_email_notification(
    #     email=user.email,
    #     subject="Account Created",
    #     message=f"Your account has been created with email {user.email}",
    # )
    return UserReadSingle(
        id=db_user.id,
        username=db_user.username,
        slug=db_user.slug,
        email=db_user.email,
        role=db_user.role,
        avatar=db_user.avatar,
        last_login=db_user.last_login,
        favorite_games=[],
        friends=[],
        game_activities=[],
    )
