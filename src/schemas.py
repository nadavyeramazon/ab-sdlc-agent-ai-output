"""Pydantic models for request/response validation."""
from pydantic import BaseModel, Field

class HelloRequest(BaseModel):
    """Request model for hello endpoint.
    
    Attributes:
        name: Name to greet (optional)
    """
    name: str = Field(
        default='World',
        min_length=1,
        max_length=50,
        description='Name to greet'
    )

class HelloResponse(BaseModel):
    """Response model for hello endpoint.
    
    Attributes:
        message: Greeting message
        request_id: Unique request identifier
    """
    message: str = Field(..., description='Greeting message')
    request_id: str = Field(..., description='Unique request identifier')