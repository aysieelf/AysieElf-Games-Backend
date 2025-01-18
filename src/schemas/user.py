from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, EmailStr, field_validator

from src.models.enums import Roles


# Base configs
class BaseConfig(BaseModel):
    model_config = {"from_attributes": True}

class UserCreate(BaseConfig):
    username: str = Field(
        min_length=5,
        max_length=15,
        pattern="^[a-zA-Z0-9_-]+$",
        examples=["example_user"],
    )
    email: EmailStr
    password: str = Field(min_length=4, max_length=36, examples=["Example123@"])
    role: Roles = Roles.USER
    avatar: Optional[str]
