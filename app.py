#!/usr/bin/env python3
"""Simple Hello World API with FastAPI"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn

# Initialize FastAPI application
app = FastAPI(
    title="Hello World API",
    description="A simple Hello World API built with FastAPI",
    version="1.0.0"
)


# Pydantic model for request body
class GreetingRequest(BaseModel):
    """Model for custom greeting requests"""
    name: str
    language: Optional[str] = "en"


# Root endpoint - Basic Hello World
@app.get("/")
async def root():
    """Root endpoint returning a simple Hello World message.
    
    Returns:
        dict: A welcome message
    """
    return {
        "message": "Hello World!",
        "status": "success",
        "api": "FastAPI Hello World API"
    }


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint to verify API is running.
    
    Returns:
        dict: Health status information
    """
    return {
        "status": "healthy",
        "message": "API is running smoothly"
    }


# Greeting endpoint with path parameter
@app.get("/hello/{name}")
async def greet_user(name: str):
    """Greet a user by name.
    
    Args:
        name (str): The name of the user to greet
    
    Returns:
        dict: Personalized greeting message
    """
    return {
        "message": f"Hello, {name}!",
        "name": name
    }


# Greeting endpoint with query parameters
@app.get("/greet")
async def greet_with_params(name: str = "World", greeting: str = "Hello"):
    """Greet with customizable greeting and name using query parameters.
    
    Args:
        name (str): The name to greet (default: "World")
        greeting (str): The greeting to use (default: "Hello")
    
    Returns:
        dict: Customized greeting message
    """
    return {
        "message": f"{greeting}, {name}!",
        "greeting": greeting,
        "name": name
    }


# POST endpoint for custom greetings
@app.post("/greet")
async def create_greeting(request: GreetingRequest):
    """Create a custom greeting in different languages.
    
    Args:
        request (GreetingRequest): Request body with name and language
    
    Returns:
        dict: Greeting message in specified language
    """
    # Dictionary of greetings in different languages
    greetings = {
        "en": "Hello",
        "es": "Hola",
        "fr": "Bonjour",
        "de": "Hallo",
        "it": "Ciao",
        "pt": "Olá",
        "ru": "Привет",
        "ja": "こんにちは",
        "zh": "你好"
    }
    
    # Get greeting in specified language or default to English
    greeting = greetings.get(request.language.lower(), greetings["en"])
    
    return {
        "message": f"{greeting}, {request.name}!",
        "name": request.name,
        "language": request.language,
        "greeting": greeting
    }


# Info endpoint
@app.get("/info")
async def get_api_info():
    """Get information about the API.
    
    Returns:
        dict: API information and available endpoints
    """
    return {
        "name": "Hello World API",
        "version": "1.0.0",
        "framework": "FastAPI",
        "description": "A simple Hello World API with multiple greeting endpoints",
        "endpoints": {
            "GET /": "Root endpoint - Basic Hello World",
            "GET /health": "Health check endpoint",
            "GET /hello/{name}": "Greet a specific user",
            "GET /greet": "Customizable greeting with query parameters",
            "POST /greet": "Create greeting in different languages",
            "GET /info": "API information",
            "GET /docs": "Interactive API documentation (Swagger UI)",
            "GET /redoc": "Alternative API documentation (ReDoc)"
        }
    }


# Run the application
if __name__ == "__main__":
    # Run with uvicorn server
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    )
