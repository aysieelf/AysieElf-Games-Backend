from uuid import UUID

from pydantic import BaseModel


class BaseConfig(BaseModel):
    model_config = {"from_attributes": True}


class FriendshipCreate(BaseConfig):
    friend_id: UUID
