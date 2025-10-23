"""API route handlers for the Hello World service."""
import logging
from typing import Dict
from fastapi import APIRouter, Depends, HTTPException

from .schemas import HelloRequest, HelloResponse
from .services import HelloWorldService
from .exceptions import HelloWorldError

logger = logging.getLogger(__name__)
router = APIRouter()

# Dependency injection
def get_service() -> HelloWorldService:
    """Get HelloWorldService instance.
    
    Returns:
        HelloWorldService: Service instance
    """
    return HelloWorldService()

@router.post(
    '/hello',
    response_model=HelloResponse,
    summary='Get a greeting',
    description='Generate a personalized greeting message'
)
async def get_greeting(
    request: HelloRequest,
    service: HelloWorldService = Depends(get_service)
) -> HelloResponse:
    """Handle greeting request.
    
    Args:
        request: Validated request model
        service: Injected service instance
        
    Returns:
        HelloResponse: Greeting response
        
    Raises:
        HTTPException: On validation or service errors
    """
    try:
        return service.get_greeting(request)
    except HelloWorldError as e:
        logger.error(f'Service error: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f'Unexpected error: {str(e)}')
        raise HTTPException(status_code=500, detail='Internal server error')

@router.get(
    '/stats',
    response_model=Dict,
    summary='Get service statistics',
    description='Retrieve service usage statistics'
)
async def get_stats(
    service: HelloWorldService = Depends(get_service)
) -> Dict:
    """Get service statistics.
    
    Args:
        service: Injected service instance
        
    Returns:
        Dict with service statistics
    """
    return service.get_stats()