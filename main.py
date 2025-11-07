"""FastAPI Hello World Application

A simple REST API that demonstrates FastAPI functionality with a hello world endpoint.
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn

# Initialize FastAPI application
app = FastAPI(
    title="Hello World API",
    description="A simple FastAPI application that provides a hello world endpoint",
    version="1.0.0"
)


@app.get("/")
async def root():
    """Root endpoint that returns a welcome message.
    
    Returns:
        dict: A JSON response with a welcome message
    """
    return {
        "message": "Welcome to the Hello World API!",
        "status": "success"
    }


@app.get("/hello")
async def hello_world():
    """Hello World endpoint.
    
    Returns:
        dict: A JSON response with a hello world message
    """
    return {
        "message": "Hello, World!",
        "status": "success"
    }


@app.get("/hello/{name}")
async def hello_name(name: str):
    """Personalized hello endpoint.
    
    Args:
        name (str): The name to greet
        
    Returns:
        dict: A JSON response with a personalized greeting
    """
    return {
        "message": f"Hello, {name}!",
        "name": name,
        "status": "success"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint to verify the API is running.
    
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
