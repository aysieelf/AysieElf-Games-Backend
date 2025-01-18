from src.models.base import Base

from sqlalchemy import TIMESTAMP, UUID, Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Friendship(Base):
    __tablename__ = "friendships"

    user1_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    user2_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    user1 = relationship(
        "User", foreign_keys=[user1_id], back_populates="friends_as_user1"
    )
    user2 = relationship(
        "User", foreign_keys=[user2_id], back_populates="friends_as_user2"
    )
