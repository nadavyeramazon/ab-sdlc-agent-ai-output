"""FastAPI Hello World Application

A simple FastAPI application that provides a hello world endpoint.
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn

# Create FastAPI application instance
app = FastAPI(
    title="Hello World API",
    description="A simple Hello World API built with FastAPI",
    version="1.0.0"
)


@app.get("/")
async def root():
    """Root endpoint that returns a welcome message.
    
    Returns:
        dict: A JSON response with a welcome message
    """
    return {"message": "Welcome to the Hello World API"}


@app.get("/hello")
async def hello():
    """Hello endpoint that returns a hello world message.
    
    Returns:
        dict: A JSON response with hello world message
    """
    return {"message": "Hello, World!"}


@app.get("/hello/{name}")
async def hello_name(name: str):
    """Hello endpoint with name parameter.
    
    Args:
        name (str): The name to greet
    
    Returns:
        dict: A JSON response with personalized greeting
    """
    return {"message": f"Hello, {name}!"}


@app.get("/health")
async def health_check():
    """Health check endpoint.
    
    Returns:
        dict: A JSON response indicating service health status
    """
    return {
        "status": "healthy",
        "service": "Hello World API",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    # Run the application with uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
