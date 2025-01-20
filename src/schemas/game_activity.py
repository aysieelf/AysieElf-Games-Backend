from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

# Base configs
class BaseConfig(BaseModel):
    model_config = {"from_attributes": True}


class GameActivityRead(BaseConfig):
    id: UUID
    user_id: UUID
    game_id: UUID
    played_at: datetime
    duration: int  # in seconds
