"""
Green Greeter Backend API

A FastAPI application that provides greeting functionality for users.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import html
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Green Greeter API",
    description="A simple greeting API with green theme",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

class GreetingRequest(BaseModel):
    """Request model for greeting endpoint."""
    name: str = Field(..., min_length=1, max_length=100, description="Name to greet")

class GreetingResponse(BaseModel):
    """Response model for greeting endpoint."""
    message: str = Field(..., description="The greeting message")

@app.get("/", response_model=dict)
async def root():
    """Root endpoint providing API information."""
    return {
        "message": "Welcome to Green Greeter API! 🌿",
        "endpoints": {
            "greet": "/greet",
            "health": "/health"
        }
    }

@app.post("/greet", response_model=GreetingResponse)
async def greet_user(request: GreetingRequest):
    """
    Greet a user with a personalized message.
    
    Args:
        request: The greeting request containing the user's name
        
    Returns:
        GreetingResponse: A greeting message for the user
        
    Raises:
        HTTPException: If the name is invalid or processing fails
    """
    try:
        # Sanitize input to prevent XSS
        clean_name = html.escape(request.name.strip())
        
        if not clean_name:
            raise HTTPException(status_code=400, detail="Name cannot be empty")
        
        # Generate greeting message
        greeting_message = f"Hello, {clean_name}! Welcome to our green-themed application! 🌿✨"
        
        logger.info(f"Generated greeting for user: {clean_name}")
        
        # Return response with 'message' key (not 'greeting')
        return GreetingResponse(message=greeting_message)
        
    except Exception as e:
        logger.error(f"Error generating greeting: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/health", response_model=dict)
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "green-greeter-backend"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)