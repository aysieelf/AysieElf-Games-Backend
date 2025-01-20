from src.models.base import Base

from sqlalchemy import TIMESTAMP, UUID, Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class GameActivity(Base):
    __tablename__ = "game_activities"
    __table_args__ = (
        UniqueConstraint('user_id', 'game_id', 'played_at', name='uix_activity'),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, server_default=func.uuid_generate_v4())
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    game_id = Column(UUID(as_uuid=True), ForeignKey("games.id"), nullable=False)
    played_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="game_activities")
    game = relationship("Game", back_populates="game_activities")