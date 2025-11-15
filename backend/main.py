"""FastAPI Backend for Green Theme Hello World Application

This module provides a simple REST API with two endpoints:
- /api/hello: Returns a hello world message with timestamp
- /health: Returns health check status

The API includes CORS middleware to allow requests from the React frontend.
"""

from datetime import datetime
from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# Pydantic models for request/response validation
class HelloResponse(BaseModel):
    """Response model for /api/hello endpoint"""
    message: str
    timestamp: str


class HealthResponse(BaseModel):
    """Response model for /health endpoint"""
    status: str


# Initialize FastAPI application
app = FastAPI(
    title="Green Theme Hello World API",
    description="Simple REST API for Hello World fullstack demo",
    version="1.0.0"
)

# Configure CORS middleware to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "http://frontend:3000",   # Docker service name
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)


@app.get("/api/hello", response_model=HelloResponse)
async def get_hello() -> Dict[str, str]:
    """Get hello world message with current timestamp
    
    Returns:
        Dictionary containing message and ISO 8601 formatted timestamp
    """
    return {
        "message": "Hello World from Backend!",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check() -> Dict[str, str]:
    """Health check endpoint for service monitoring
    
    Returns:
        Dictionary containing health status
    """
    return {"status": "healthy"}


@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint with API information
    
    Returns:
        Dictionary with welcome message and available endpoints
    """
    return {
        "message": "Green Theme Hello World API",
        "endpoints": {
            "hello": "/api/hello",
            "health": "/health",
            "docs": "/docs"
        }
    }
