from src.models.base import Base

from sqlalchemy import TIMESTAMP, Column, String
from sqlalchemy.sql import func


class BlacklistedToken(Base):
    __tablename__ = "blacklisted_tokens"

    token = Column(String, primary_key=True, index=True)
    blacklisted_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    expires_at = Column(TIMESTAMP(timezone=True), nullable=False)
