
from src.models.base import Base
from src.models.enums import Roles

from sqlalchemy import Boolean, Column, DateTime, Enum, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(320), unique=True, nullable=False, index=True)
    password_hash = Column(
        String(60), nullable=False
    )  # bcrypt hashed password is 60 characters long
    role = Column(Enum(Roles), nullable=False, default=Roles.USER)
    avatar = Column(String(2048), nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now()
    )  # can be used for future achievements and badges
    last_login = Column(DateTime(timezone=True), nullable=True)
    is_verified = Column(Boolean, nullable=False, default=False)
