import re

from src.models.base import Base
from src.models.enums import Roles
from src.models.friendship import Friendship

from sqlalchemy import TIMESTAMP, Boolean, Column, Enum, String, event
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        server_default=func.uuid_generate_v4(),
    )
    username = Column(String(50), unique=True, nullable=False, index=True)
    slug = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(320), unique=True, nullable=False, index=True)
    password_hash = Column(
        String(60), nullable=False
    )  # bcrypt hashed password is 60 characters long
    role = Column(Enum(Roles), nullable=False, default=Roles.USER)
    avatar = Column(String(255), nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False,
    )  # can be used for future achievements and badges
    last_login = Column(TIMESTAMP(timezone=True), nullable=True)
    is_verified = Column(Boolean, nullable=False, default=False)

    friends_as_user1 = relationship(
        "Friendship", foreign_keys=[Friendship.user1_id], back_populates="user1"
    )
    friends_as_user2 = relationship(
        "Friendship", foreign_keys=[Friendship.user2_id], back_populates="user2"
    )
    game_activities = relationship("GameActivity", back_populates="user")
    upvotes = relationship("Upvote", back_populates="user")
    favorites = relationship("Favorite", back_populates="user")

    @property
    def friends(self):
        """Get all friends regardless of user1/user2 position"""
        return [f.user2 for f in self.friends_as_user1] + [
            f.user1 for f in self.friends_as_user2
        ]

    @staticmethod
    def generate_slug(username: str) -> str:
        """Generate URL-friendly slug from username."""
        return re.sub(r"[^a-z0-9]+", "-", username.lower()).strip("-")


# SQLAlchemy event listener to automatically generate slug before insert
@event.listens_for(User, "before_insert")
def set_slug(mapper, connection, target):
    target.slug = User.generate_slug(target.username)
