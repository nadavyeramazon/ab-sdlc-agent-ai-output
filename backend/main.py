from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pydantic import BaseModel, validator

# Initialize FastAPI application with redirect_slashes disabled
# This ensures that routes with trailing slashes are not automatically redirected
# and will return 404 if not explicitly defined
app = FastAPI(redirect_slashes=False)

# Configure CORS middleware to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


# Pydantic model for greeting request validation
class GreetRequest(BaseModel):
    """Request model for personalized greeting endpoint."""
    name: str
    
    @validator('name')
    def name_not_empty(cls, v):
        """
        Validate that name is not empty or whitespace-only.
        Automatically trims leading/trailing whitespace.
        
        Args:
            v: The name value to validate
            
        Returns:
            Trimmed name string
            
        Raises:
            ValueError: If name is empty or whitespace-only
        """
        if not v or not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()


@app.get("/api/hello")
def get_hello():
    """Return hello message with current timestamp"""
    return {
        "message": "Hello World from Backend!",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@app.post("/api/greet")
async def greet_user(request: GreetRequest):
    """
    Personalized greeting endpoint for purple-themed app.
    
    This endpoint accepts a user's name and returns a personalized greeting
    message along with a timestamp. The name is automatically validated and
    trimmed of whitespace.
    
    Args:
        request: GreetRequest containing user's name (validated, non-empty)
        
    Returns:
        JSON response containing:
        - greeting: Personalized greeting message with user's name
        - timestamp: Current UTC timestamp in ISO-8601 format
        
    Raises:
        HTTPException 422: If name validation fails (empty or whitespace-only)
        
    Example:
        Request: {"name": "Alice"}
        Response: {
            "greeting": "Hello, Alice! Welcome to our purple-themed app!",
            "timestamp": "2024-01-15T10:30:00.000000Z"
        }
    """
    greeting_text = f"Hello, {request.name}! Welcome to our purple-themed app!"
    return {
        "greeting": greeting_text,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@app.get("/health")
def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy"}
