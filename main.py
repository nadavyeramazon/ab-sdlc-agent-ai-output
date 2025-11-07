"""FastAPI Hello World Application

A simple Hello World API built with FastAPI.
This application demonstrates basic FastAPI functionality with multiple endpoints.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn

# Create FastAPI application instance
app = FastAPI(
    title="Hello World API",
    description="A simple FastAPI Hello World application",
    version="1.0.0"
)


class GreetingRequest(BaseModel):
    """Request model for personalized greeting"""
    name: str
    language: Optional[str] = "en"


class GreetingResponse(BaseModel):
    """Response model for greeting"""
    message: str
    status: str = "success"


@app.get("/", response_model=GreetingResponse)
async def root():
    """
    Root endpoint that returns a simple Hello World message.
    
    Returns:
        dict: A welcome message
    """
    return {
        "message": "Hello World! Welcome to FastAPI",
        "status": "success"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring.
    
    Returns:
        dict: Application health status
    """
    return {
        "status": "healthy",
        "message": "Application is running"
    }


@app.get("/hello/{name}", response_model=GreetingResponse)
async def hello_name(name: str):
    """
    Personalized greeting endpoint.
    
    Args:
        name: The name to greet
        
    Returns:
        dict: Personalized greeting message
    """
    return {
        "message": f"Hello, {name}! Welcome to FastAPI",
        "status": "success"
    }


@app.post("/greet", response_model=GreetingResponse)
async def custom_greeting(greeting_request: GreetingRequest):
    """
    Create a custom greeting in different languages.
    
    Args:
        greeting_request: GreetingRequest object containing name and language
        
    Returns:
        dict: Greeting in specified language
    """
    # Dictionary of greetings in different languages
    greetings = {
        "en": "Hello",
        "es": "Hola",
        "fr": "Bonjour",
        "de": "Hallo",
        "it": "Ciao",
        "pt": "Olá",
        "ja": "こんにちは",
        "zh": "你好",
        "ko": "안녕하세요",
        "ar": "مرحبا"
    }
    
    # Get the greeting in the requested language, default to English
    greeting = greetings.get(greeting_request.language.lower(), greetings["en"])
    
    return {
        "message": f"{greeting}, {greeting_request.name}!",
        "status": "success"
    }


@app.get("/info")
async def get_info():
    """
    Get API information.
    
    Returns:
        dict: API information and available endpoints
    """
    return {
        "api_name": "Hello World API",
        "version": "1.0.0",
        "description": "A simple FastAPI Hello World application",
        "endpoints": [
            {
                "path": "/",
                "method": "GET",
                "description": "Root endpoint with welcome message"
            },
            {
                "path": "/health",
                "method": "GET",
                "description": "Health check endpoint"
            },
            {
                "path": "/hello/{name}",
                "method": "GET",
                "description": "Personalized greeting endpoint"
            },
            {
                "path": "/greet",
                "method": "POST",
                "description": "Custom greeting in different languages"
            },
            {
                "path": "/info",
                "method": "GET",
                "description": "API information endpoint"
            }
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
