from datetime import UTC, datetime

from fastapi import APIRouter

from database.session import engine
from src.core.config import settings

router = APIRouter()


@router.get("/health", status_code=200)
async def health_check():
    try:
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        return {
            "status": "healthy",
            "service": settings.PROJECT_NAME,
            "environment": "development" if settings.DEBUG else "production",
            "database": "connected",
            "timestamp": datetime.now(UTC).isoformat(),
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": settings.PROJECT_NAME,
            "environment": "development" if settings.DEBUG else "production",
            "database": str(e),
            "timestamp": datetime.now(UTC).isoformat(),
       }