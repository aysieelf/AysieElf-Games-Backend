from datetime import UTC, datetime
from typing import Any, Dict

from database.session import engine
from src.core.config import settings

from fastapi import APIRouter, status
import psutil
from sqlalchemy import text

router = APIRouter()


@router.get("/health", status_code=status.HTTP_200_OK)
async def basic_health_check():
    """
    Basic health check endpoint that quickly verifies core service functionality.
    Returns 200 if healthy, 503 if unhealthy.
    """
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "healthy", "timestamp": datetime.now(UTC).isoformat()}
    except Exception:
        return {
            "status": "unhealthy",
            "timestamp": datetime.now(UTC).isoformat(),
        }, status.HTTP_503_SERVICE_UNAVAILABLE


@router.get("/health/details", status_code=status.HTTP_200_OK)
async def detailed_health_check() -> Dict[str, Any]:
    """
    Detailed health check that provides additional system information.
    Useful for debugging and monitoring.
    """
    db_status = "healthy"
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except Exception as e:
        db_status = str(e)

    # Basic system metrics
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    return {
        "service": {
            "name": settings.PROJECT_NAME,
            "environment": "development" if settings.DEBUG else "production",
            "timestamp": datetime.now(UTC).isoformat(),
        },
        "database": {
            "status": db_status,
        },
        "system": {
            "memory_usage_percent": memory.percent,
            "disk_usage_percent": disk.percent,
            "cpu_usage_percent": psutil.cpu_percent(interval=1),
        },
    }
