from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from src.schemas.game import GameReadAll


# Base configs
class BaseConfig(BaseModel):
    model_config = {"from_attributes": True}

class CategoryCreate(BaseConfig):

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