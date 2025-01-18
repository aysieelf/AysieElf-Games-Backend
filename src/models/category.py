import re

from src.models.base import Base

from sqlalchemy import Column, UUID, String, Text, event
from sqlalchemy.orm import relationship


class Category(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True, index=True)
    slug = Column(String(50), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)

    games = relationship("Game", back_populates="category")

    @staticmethod
    def generate_slug(name: str) -> str:
        """Generate URL-friendly slug from title."""
        return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


# SQLAlchemy event listener to automatically generate slug before insert
@event.listens_for(Category, "before_insert")
def set_slug(mapper, connection, target):
    target.slug = Category.generate_slug(target.name)
