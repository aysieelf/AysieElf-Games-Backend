from typing import Optional
from uuid import UUID

from src.schemas.game import GameReadAll

from pydantic import BaseModel, Field


# Base configs
class BaseConfig(BaseModel):
    model_config = {"from_attributes": True}


class CategoryCreate(BaseConfig):
    name: str = Field(
        min_length=5,
        max_length=50,
        examples=["Example Category"],
    )
    description: Optional[str] = None


class CategoryReadAll(BaseConfig):
    id: UUID
    name: str
    slug: str
    description: Optional[str]


class CategoryReadSingle(CategoryReadAll):
    games: list[GameReadAll]


class CategoryUpdate(BaseConfig):
    name: Optional[str] = None
    description: Optional[str] = None
