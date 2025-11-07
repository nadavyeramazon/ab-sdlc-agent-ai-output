"""FastAPI Hello World Application

A simple Hello World API built with FastAPI.
This application demonstrates basic FastAPI functionality with a simple greeting endpoint.
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
        dict: A dictionary containing a welcome message
    """
    return {"message": "Hello World!"}


@app.get("/hello")
async def hello():
    """Hello endpoint that returns a greeting message.
    
    Returns:
        dict: A dictionary containing a greeting message
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
    """Health check endpoint to verify the API is running.
    
    Returns:
        dict: A dictionary containing the health status
    """
    return {"status": "healthy", "message": "API is running"}


if __name__ == "__main__":
    # Run the application with uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
