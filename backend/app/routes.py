"""API route handlers."""

from fastapi import APIRouter, HTTPException
from app.models import HelloResponse, HealthResponse, GreetRequest, GreetResponse
from datetime import datetime
import logging
from pydantic import ValidationError

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


@router.post(
    "/api/greet",
    response_model=GreetResponse,
    status_code=200,
    summary="Get personalized greeting",
    description="Returns a personalized greeting message for the provided name"
)
async def greet_user(request: GreetRequest) -> GreetResponse:
    """Get personalized greeting for user.
    
    Args:
        request: GreetRequest containing user's name
    
    Returns:
        GreetResponse: Personalized greeting and timestamp
        
    Raises:
        HTTPException: If validation fails (400) or an error occurs (500)
    """
    try:
        # The name validation is already handled by Pydantic model
        # Name will be trimmed and validated for non-empty string
        greeting_message = f"Hello, {request.name}! Welcome to our purple-themed app!"
        
        return GreetResponse(
            greeting=greeting_message,
            timestamp=datetime.utcnow()
        )
    except ValidationError as e:
        logger.warning(f"Validation error in greet_user endpoint: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail="Name cannot be empty"
        )
    except Exception as e:
        logger.error(f"Error in greet_user endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
