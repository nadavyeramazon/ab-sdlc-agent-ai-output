"""Simple Hello World API with FastAPI

This module implements a basic FastAPI application with a Hello World endpoint.
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from typing import Dict
import uvicorn

# Initialize FastAPI application
app = FastAPI(
    title="Hello World API",
    description="A simple Hello World API built with FastAPI",
    version="1.0.0"
)


@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint that returns a Hello World message.
    
    Returns:
        Dict[str, str]: A dictionary containing the hello world message
    """
    return {"message": "Hello World!"}


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint to verify the API is running.
    
    Returns:
        Dict[str, str]: A dictionary containing the health status
    """
    return {"status": "healthy"}


@app.get("/hello/{name}")
async def hello_name(name: str) -> Dict[str, str]:
    """Personalized hello endpoint.
    
    Args:
        name: The name to greet
        
    Returns:
        Dict[str, str]: A dictionary containing a personalized greeting
    """
    return {"message": f"Hello {name}!"}


@app.get("/api/info")
async def api_info() -> Dict[str, str]:
    """Endpoint that returns API information.
    
    Returns:
        Dict[str, str]: A dictionary containing API metadata
    """
    return {
        "name": "Hello World API",
        "version": "1.0.0",
        "description": "A simple Hello World API built with FastAPI",
        "framework": "FastAPI"
    }


if __name__ == "__main__":
    # Run the application with uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
