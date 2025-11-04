from fastapi import APIRouter, status
from typing import Dict
from datetime import datetime
from app.core.config import settings

router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=Dict,
    summary="Health check endpoint",
    description="Returns application health status"
)
async def health_check() -> Dict:
    """
    Health check endpoint.
    
    Returns:
        Dict containing health status and app information
    """
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "timestamp": datetime.utcnow().isoformat()
    }