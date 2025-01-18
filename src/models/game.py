import re

from src.models.base import Base

from sqlalchemy import TIMESTAMP, UUID, Boolean, Column, ForeignKey, String, Text, event
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Game(Base):
    __tablename__ = "games"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    title = Column(String(100), nullable=False, unique=True, index=True)
    slug = Column(String(100), nullable=False, unique=True, index=True)
    icon = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    is_multiplayer = Column(Boolean, nullable=False, default=False, index=True)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )

    category_id = Column(
        UUID(as_uuid=True), ForeignKey("category.id"), nullable=False, index=True
    )
    category = relationship("Category", back_populates="games")

    @staticmethod
    def generate_slug(title: str) -> str:
        """Generate URL-friendly slug from title."""
        return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


# SQLAlchemy event listener to automatically generate slug before insert
@event.listens_for(Game, "before_insert")
def set_slug(mapper, connection, target):
    target.slug = Game.generate_slug(target.title)
