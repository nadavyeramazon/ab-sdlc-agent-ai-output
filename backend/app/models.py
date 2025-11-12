"""Pydantic models for request/response validation."""

from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Literal


class HelloResponse(BaseModel):
    """Response model for hello endpoint."""
    message: str = Field(
        ...,
        description="Hello world message from backend",
        example="Hello World from Backend!"
    )
    timestamp: datetime = Field(
        ...,
        description="ISO-8601 formatted timestamp",
        example="2024-01-15T10:30:00Z"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Hello World from Backend!",
                "timestamp": "2024-01-15T10:30:00.000Z"
            }
        }


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    status: Literal["healthy", "unhealthy"] = Field(
        ...,
        description="Health status of the service",
        example="healthy"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy"
            }
        }


class GreetRequest(BaseModel):
    """Request model for greet endpoint."""
    name: str = Field(
        ...,
        description="User's name for personalized greeting",
        example="John Doe",
        min_length=1
    )

    @field_validator('name')
    @classmethod
    def validate_name_not_empty(cls, v: str) -> str:
        """Validate that name is not empty or whitespace only."""
        if not v or not v.strip():
            raise ValueError('Name cannot be empty')
        # Return trimmed value to sanitize input
        return v.strip()

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe"
            }
        }


class GreetResponse(BaseModel):
    """Response model for greet endpoint."""
    greeting: str = Field(
        ...,
        description="Personalized greeting message",
        example="Hello, John Doe! Welcome to our purple-themed app!"
    )
    timestamp: datetime = Field(
        ...,
        description="ISO-8601 formatted timestamp",
        example="2024-01-15T10:30:00Z"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "greeting": "Hello, John Doe! Welcome to our purple-themed app!",
                "timestamp": "2024-01-15T10:30:00.000Z"
            }
        }
