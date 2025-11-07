"""FastAPI Hello World Application

A simple FastAPI application that provides a Hello World endpoint.
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
        dict: A dictionary containing a hello world message
    """
    return {"message": "Hello World!"}


@app.get("/hello")
async def hello():
    """Hello endpoint that returns a greeting.
    
    Returns:
        dict: A dictionary containing a hello message
    """
    return {"greeting": "Hello", "target": "World"}


@app.get("/hello/{name}")
async def hello_name(name: str):
    """Personalized hello endpoint.
    
    Args:
        name (str): The name to greet
    
    Returns:
        dict: A dictionary containing a personalized greeting
    """
    return {"message": f"Hello {name}!"}


@app.get("/health")
async def health_check():
    """Health check endpoint.
    
    Returns:
        dict: A dictionary indicating the service status
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
