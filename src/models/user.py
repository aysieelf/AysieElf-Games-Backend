from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Enum, DateTime
from sqlalchemy.sql import func
from src.models.base import Base
from src.models.enums import Roles


class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(320), unique=True, nullable=False)
    role = Column(Enum(Roles), nullable=False, default=Roles.USER)
    avatar = Column(String(2048), nullable=True)
    password_hash = Column(String(50), nullable=False) # TODO: check how long should it be
    created_at = Column(DateTime(timezone=True), server_default=func.now()) # TODO: research what is server_default
    last_login = Column(DateTime(timezone=True), nullable=True) # TODO: why is this nullable?

