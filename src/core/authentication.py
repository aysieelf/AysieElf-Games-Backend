from datetime import datetime, timedelta, timezone
from typing import Optional

from src.api.deps import get_db
from src.core.config import settings
from src.core.security import verify_password
from src.crud.user import get_by_id
from src.models.blacklisted_token import BlacklistedToken
from src.models.user import User
from src.schemas.user import UserReadSingle

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """
    Authenticate a user by username and password.
    Returns None if authentication fails.
    """
    user = db.query(User).filter(User.username == username).first()

    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    # Update last login time
    user.last_login = datetime.now(timezone.utc)
    db.commit()

    return user


def create_access_token(data: dict) -> str:
    """Create a new JWT access token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRATION)
    to_encode.update({"exp": expire})

    token = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )

    return token


def verify_token(token: str, db: Session) -> dict:
    """Verify a JWT token and return its payload."""
    try:
        if is_token_blacklisted(db, token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been blacklisted",
            )

        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        return payload

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> UserReadSingle:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_by_id(db, user_id)
    return user


def add_token_to_blacklist(
    db: Session, token: str, expire_minutes: int = settings.JWT_TOKEN_BLACKLIST_MINUTES
) -> None:
    """Add a token to the blacklist."""
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
    blacklisted_token = BlacklistedToken(token=token, expires_at=expires_at)
    db.add(blacklisted_token)
    db.commit()


def is_token_blacklisted(db: Session, token: str) -> bool:
    """Check if a token is blacklisted and not expired."""
    blacklisted = (
        db.query(BlacklistedToken)
        .filter(
            BlacklistedToken.token == token,
            BlacklistedToken.expires_at > datetime.now(timezone.utc),
        )
        .first()
    )
    return blacklisted is not None


def cleanup_expired_tokens(db: Session) -> int:
    """Remove expired tokens from blacklist. Returns number of tokens deleted."""
    deleted = (
        db.query(BlacklistedToken)
        .filter(BlacklistedToken.expires_at <= datetime.now(timezone.utc))
        .delete()
    )
    db.commit()
    return deleted


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.JWT_REFRESH_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_REFRESH_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )

    return encoded_jwt


def ensure_not_authenticated(token: str = Depends(oauth2_scheme)):
    if token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please logout first."
        )
