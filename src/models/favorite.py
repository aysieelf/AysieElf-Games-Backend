from src.models.base import Base

from sqlalchemy import TIMESTAMP, UUID, Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Favorite(Base):
    __tablename__ = "favorites"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    game_id = Column(UUID(as_uuid=True), ForeignKey("games.id"), primary_key=True)
    added_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="favorites")
    game = relationship("Game", back_populates="favorites")
