from typing import Optional

from pydantic import BaseModel, Field

from src.schemas.game import GameReadAll


# Base configs
class BaseConfig(BaseModel):
    model_config = {"from_attributes": True}

class CategoryCreate(BaseConfig):
    name: str
    description: Optional[str] = None

class CategoryReadAll(BaseConfig):
    name: str
    description: Optional[str]

class CategoryReadSingle(CategoryReadAll):
    games: list[GameReadAll]

class CategoryUpdate(BaseConfig):
    name: Optional[str] = None
    description: Optional[str] = None