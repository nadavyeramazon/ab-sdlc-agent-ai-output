from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
from datetime import datetime
import re
import html

app = FastAPI(
    title="Greeting API",
    description="A simple greeting API with green-themed UI",
    version="1.0.0"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GreetingRequest(BaseModel):
    name: str
    
    @validator('name')
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Name cannot be empty')
        
        # Remove extra whitespace
        v = v.strip()
        
        # Check length (reasonable limits)
        if len(v) < 1:
            raise ValueError('Name must be at least 1 character long')
        if len(v) > 100:
            raise ValueError('Name must be less than 100 characters long')
        
        # Basic sanitization - allow only letters, spaces, hyphens, apostrophes
        if not re.match(r"^[a-zA-Z\s\-\']+$", v):
            raise ValueError('Name can only contain letters, spaces, hyphens, and apostrophes')
        
        # HTML escape for additional security
        v = html.escape(v)
        
        return v

class GreetingResponse(BaseModel):
    message: str
    timestamp: str
    name: str

@app.get("/")
async def root():
    """Root endpoint providing API information"""
    return {
        "message": "Welcome to the Greeting API",
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "/greet": "POST - Send a greeting request",
            "/health": "GET - Check API health",
            "/docs": "GET - API documentation"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "greeting-api"
    }

@app.post("/greet", response_model=GreetingResponse)
async def greet_user(request: GreetingRequest):
    """
    Greet a user by name with enhanced security and validation
    """
    try:
        # Additional server-side validation
        if len(request.name.strip()) == 0:
            raise HTTPException(status_code=400, detail="Name cannot be empty")
        
        # Create personalized greeting
        current_time = datetime.now()
        hour = current_time.hour
        
        # Time-based greeting
        if 5 <= hour < 12:
            time_greeting = "Good morning"
        elif 12 <= hour < 17:
            time_greeting = "Good afternoon"
        elif 17 <= hour < 22:
            time_greeting = "Good evening"
        else:
            time_greeting = "Good night"
        
        greeting_message = f"{time_greeting}, {request.name}! Welcome to our green-themed greeting service! 🌿"
        
        return GreetingResponse(
            message=greeting_message,
            timestamp=current_time.isoformat(),
            name=request.name
        )
    
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error occurred")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)