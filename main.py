"""Simple Hello World FastAPI Application

This module implements a basic FastAPI application with a hello world endpoint.
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn

# Create FastAPI application instance
app = FastAPI(
    title="Hello World API",
    description="A simple FastAPI Hello World application",
    version="1.0.0"
)


@app.get("/")
async def root():
    """Root endpoint that returns a hello world message.
    
    Returns:
        dict: A dictionary containing a greeting message
    """
    return {"message": "Hello World!"}


@app.get("/hello")
async def hello():
    """Hello endpoint that returns a greeting.
    
    Returns:
        dict: A dictionary containing a hello message
    """
    return {"message": "Hello from FastAPI!"}


@app.get("/hello/{name}")
async def hello_name(name: str):
    """Personalized hello endpoint.
    
    Args:
        name (str): The name to greet
        
    Returns:
        dict: A dictionary containing a personalized greeting
    """
    return {"message": f"Hello, {name}!"}


@app.get("/health")
async def health_check():
    """Health check endpoint.
    
    Returns:
        dict: A dictionary indicating the service health status
    """
    return {"status": "healthy", "service": "Hello World API"}


if __name__ == "__main__":
    # Run the application with uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
