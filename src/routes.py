"""API routes definition module.

Defines all HTTP endpoints for the Hello World service.
"""

from fastapi import APIRouter, HTTPException
from .schemas import HelloResponse
from .services import HelloWorldService

router = APIRouter()
hello_service = HelloWorldService()

@router.get("/hello", response_model=HelloResponse)
async def get_hello() -> HelloResponse:
    """Get hello world message.

    Returns:
        HelloResponse: Response containing hello message

    Raises:
        HTTPException: If service is unable to generate message
    """
    try:
        message = hello_service.get_message()
        return HelloResponse(message=message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
