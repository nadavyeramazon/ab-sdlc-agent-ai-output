"""Pydantic models for request/response validation."""

from pydantic import BaseModel, Field
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
