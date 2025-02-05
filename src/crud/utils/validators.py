from src.models.user import User

from fastapi import HTTPException, status
from sqlalchemy.orm import Session


def user_email_exists(db: Session, email: str):
    """
    Check if an email address already exists in the database.

    Args:
        db (Session): The database session.
        email (str): The email address to check.

    Raises:
        HTTPException: If the email address already exists.
    """
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="There is a user registered with this email address.",
        )


def user_username_exists(db: Session, username: str):
    """
    Check if a username already exists in the database.

    Args:
        db (Session): The database session.
        username (str): The username to check.

    Raises:
        HTTPException: If the username already exists.
    """
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="There is a user registered with this username.",
        )
