from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class HelloRequest(BaseModel):
    """Request model for hello endpoint"""
    name: str = Field(..., min_length=1, max_length=100, description="Name to greet")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe"
            }
        }


class HelloResponse(BaseModel):
    """Response model for hello endpoint"""
    message: str = Field(..., description="Hello message")
    timestamp: datetime = Field(..., description="Response timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Hello, World!",
                "timestamp": "2024-01-01T12:00:00"
            }
        }