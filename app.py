"""FastAPI Hello World Application

A simple FastAPI application that provides a hello world endpoint.
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn

# Initialize FastAPI application
app = FastAPI(
    title="Hello World API",
    description="A simple FastAPI hello world application",
    version="1.0.0"
)


@app.get("/")
async def root():
    """Root endpoint that returns a hello world message.
    
    Returns:
        dict: A JSON response with a hello world message
    """
    return {"message": "Hello World"}


@app.get("/health")
async def health_check():
    """Health check endpoint.
    
    Returns:
        dict: A JSON response indicating the service is healthy
    """
    return {"status": "healthy"}


@app.get("/hello/{name}")
async def hello_name(name: str):
    """Personalized hello endpoint.
    
    Args:
        name (str): The name to greet
        
    Returns:
        dict: A JSON response with a personalized greeting
    """
    return {"message": f"Hello {name}!"}


if __name__ == "__main__":
    # Run the application with uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
