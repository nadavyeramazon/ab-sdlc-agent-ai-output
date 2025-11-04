from fastapi import APIRouter, status
from typing import Dict

router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=Dict[str, str],
    summary="Hello World endpoint",
    description="Returns a simple hello world message"
)
async def hello_world() -> Dict[str, str]:
    """
    Returns a hello world message.
    
    Returns:
        Dict containing message and status
    """
    return {
        "message": "Hello World from AB SDLC Agent AI Backend!",
        "status": "success"
    }


@router.get(
    "/greet/{name}",
    status_code=status.HTTP_200_OK,
    response_model=Dict[str, str],
    summary="Personalized greeting",
    description="Returns a personalized greeting message"
)
async def greet_user(name: str) -> Dict[str, str]:
    """
    Returns a personalized greeting.
    
    Args:
        name: Name of the person to greet
        
    Returns:
        Dict containing personalized message and status
    """
    return {
        "message": f"Hello {name}, welcome to AB SDLC Agent AI Backend!",
        "status": "success"
    }