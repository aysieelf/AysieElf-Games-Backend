from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.core.config import settings
from src.models.base import Base

# engine is the connection between backend and database
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # only if DEBUG = True
    connect_args=(
        {"options": "-c timezone=UTC"} if "postgresql" in settings.DATABASE_URL else {}
    ),
)

# create a session - current transaction
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """
    Creates tables from all models
    """
    Base.metadata.create_all(bind=engine)
