"""FastAPI Hello World Application

A simple Hello World API demonstrating FastAPI basics.
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI(
    title="Hello World API",
    description="A simple Hello World API built with FastAPI",
    version="1.0.0"
)


@app.get("/")
async def root():
    """Root endpoint returning a hello world message.
    
    Returns:
        dict: A dictionary containing a hello world message
    """
    return {"message": "Hello World"}


@app.get("/health")
async def health_check():
    """Health check endpoint.
    
    Returns:
        dict: A dictionary containing the health status
    """
    return {"status": "healthy"}


@app.get("/hello/{name}")
async def hello_name(name: str):
    """Personalized hello endpoint.
    
    Args:
        name: The name to greet
        
    Returns:
        dict: A dictionary containing a personalized greeting
    """
    return {"message": f"Hello {name}!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
