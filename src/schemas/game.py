from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


# Base configs
class BaseConfig(BaseModel):
    model_config = {"from_attributes": True}

class GameCreate(BaseConfig):
    title: str
    icon: Optional[str] = None
    description: Optional[str] = None
    is_multiplayer: bool = False
    category_id: UUID

class GameReadAll(BaseConfig):
    id: UUID
    title: str
    icon: Optional[str]
    description: Optional[str]
    category_slug: str = Field(alias="category.slug")
    category_title: str = Field(alias="category.title")
