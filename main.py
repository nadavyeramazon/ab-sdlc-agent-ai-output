"""FastAPI Hello World Application

This module implements a simple Hello World API using FastAPI.
It provides a basic endpoint that returns a greeting message.
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn

# Initialize FastAPI application
app = FastAPI(
    title="Hello World API",
    description="A simple Hello World API built with FastAPI",
    version="1.0.0"
)


@app.get("/")
async def root():
    """Root endpoint that returns a welcome message.
    
    Returns:
        dict: A JSON response with a greeting message
    """
    return {
        "message": "Hello World!",
        "status": "success",
        "api": "FastAPI Hello World"
    }


@app.get("/hello")
async def hello():
    """Hello endpoint that returns a simple hello message.
    
    Returns:
        dict: A JSON response with a hello message
    """
    return {"message": "Hello World!"}


@app.get("/hello/{name}")
async def hello_name(name: str):
    """Personalized hello endpoint.
    
    Args:
        name (str): The name to greet
        
    Returns:
        dict: A JSON response with a personalized greeting
    """
    return {
        "message": f"Hello {name}!",
        "name": name
    }


@app.get("/health")
async def health_check():
    """Health check endpoint to verify API is running.
    
    Returns:
        dict: A JSON response indicating the API health status
    """
    return {
        "status": "healthy",
        "service": "Hello World API"
    }


if __name__ == "__main__":
    # Run the application with uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
