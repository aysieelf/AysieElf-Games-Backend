from datetime import datetime
from typing import Optional
from uuid import UUID

from src.models.enums import Role
from src.schemas.game import GameReadAll
from src.schemas.game_activity import GameActivityRead

from pydantic import BaseModel, EmailStr, Field, field_validator


# Base configs
class BaseConfig(BaseModel):
    model_config = {"from_attributes": True}


class UserCreate(BaseConfig):
    username: str = Field(
        min_length=4,
        max_length=15,
        pattern="^[a-zA-Z0-9_-]+$",
        examples=["example_user"],
    )
    email: EmailStr
    password: str = Field(min_length=4, max_length=36, examples=["Example123"])
    role: Role = Role.USER
    avatar: Optional[str] = None

    @field_validator("password")
    def validate_password(cls, value):
        if not (
            any(c.isupper() for c in value)
            and any(c.islower() for c in value)
            and any(c.isdigit() for c in value)
            and not any(c.isspace() for c in value)
        ):
            raise ValueError(
                "Password must contain at least "
                "one uppercase letter, one lowercase letter, "
                "one number, and must not contain any spaces"
            )
        return value


class UserReadFriends(BaseConfig):
    id: UUID
    username: str
    slug: str
    avatar: Optional[str]


class UserReadAll(BaseConfig):
    id: UUID
    username: str
    slug: str
    email: str
    role: Role
    avatar: Optional[str]
    last_login: Optional[datetime]


class UserReadSingle(UserReadAll):
    favorite_games: list[GameReadAll | None]
    friends: list[UserReadFriends | None]
    game_activities: list[GameActivityRead | None]


class UserUpdate(BaseConfig):
    username: Optional[str] = Field(
        None,
        min_length=4,
        max_length=15,
        pattern="^[a-zA-Z0-9_-]+$",
    )
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=4, max_length=36)
    role: Optional[Role] = None
    avatar: Optional[str] = None

    @field_validator("password")
    def validate_password(cls, value):
        if value is None:
            return value
        if not (
            any(c.isupper() for c in value)
            and any(c.islower() for c in value)
            and any(c.isdigit() for c in value)
            and not any(c.isspace() for c in value)
        ):
            raise ValueError(
                "Password must contain at least "
                "one uppercase letter, one lowercase letter, "
                "one number, and must not contain any spaces"
            )
        return value
