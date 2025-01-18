from typing import Optional

from pydantic import BaseModel, Field


# Base configs
class BaseConfig(BaseModel):
    model_config = {"from_attributes": True}

class CategoryCreate(BaseConfig):
    name: str
    description: Optional[str] = None

class CategoryReadAll(BaseConfig):
    name: str
    description: Optional[str]