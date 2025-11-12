"""API route handlers."""

from fastapi import APIRouter, HTTPException
from app.models import HelloResponse, HealthResponse
from datetime import datetime
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()


@router.get(
    "/api/hello",
    response_model=HelloResponse,
    status_code=200,
    summary="Get hello message",
    description="Returns a hello world message with current timestamp"
)
async def get_hello() -> HelloResponse:
    """Get hello world message with timestamp.
    
    Returns:
        HelloResponse: Message and timestamp
        
    Raises:
        HTTPException: If an error occurs (500)
    """
    try:
        return HelloResponse(
            message="Hello World from Backend!",
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        logger.error(f"Error in get_hello endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=200,
    summary="Health check",
    description="Returns the health status of the service"
)
async def health_check() -> HealthResponse:
    """Check service health status.
    
    Returns:
        HealthResponse: Health status
    """
    return HealthResponse(status="healthy")
