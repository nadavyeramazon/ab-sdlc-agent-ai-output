"""FastAPI Hello World Application

A simple FastAPI application that demonstrates basic API endpoints.
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from typing import Dict
import uvicorn

# Create FastAPI application instance
app = FastAPI(
    title="Hello World API",
    description="A simple Hello World API built with FastAPI",
    version="1.0.0"
)


@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint that returns a hello world message.
    
    Returns:
        Dict[str, str]: A dictionary containing a greeting message
    """
    return {"message": "Hello World!"}


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint to verify the API is running.
    
    Returns:
        Dict[str, str]: A dictionary indicating the service status
    """
    return {"status": "healthy", "message": "Service is up and running"}


@app.get("/hello/{name}")
async def hello_name(name: str) -> Dict[str, str]:
    """Personalized greeting endpoint.
    
    Args:
        name (str): The name to greet
    
    Returns:
        Dict[str, str]: A dictionary containing a personalized greeting
    """
    return {"message": f"Hello, {name}!"}


@app.get("/info")
async def info() -> Dict[str, str]:
    """Information endpoint about the API.
    
    Returns:
        Dict[str, str]: A dictionary containing API information
    """
    return {
        "name": "Hello World API",
        "version": "1.0.0",
        "description": "A simple FastAPI Hello World application",
        "endpoints": [
            "/",
            "/health",
            "/hello/{name}",
            "/info"
        ]
    }


if __name__ == "__main__":
    # Run the application with uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
