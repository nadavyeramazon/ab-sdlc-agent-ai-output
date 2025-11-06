from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

# Create FastAPI instance
app = FastAPI(
    title="User Greeting API",
    description="A FastAPI application that greets users with personalized messages",
    version="1.0.0"
)

# Add CORS middleware to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class GreetingRequest(BaseModel):
    name: str
    greeting_type: Optional[str] = "Hello"

class GreetingResponse(BaseModel):
    message: str
    name: str
    timestamp: str

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to the User Greeting API! Visit /docs for API documentation."}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Backend service is running"}

@app.post("/greet", response_model=GreetingResponse)
async def greet_user(request: GreetingRequest):
    """Greet a user with a personalized message"""
    try:
        if not request.name or len(request.name.strip()) == 0:
            raise HTTPException(status_code=400, detail="Name cannot be empty")
        
        name = request.name.strip().title()
        greeting_type = request.greeting_type or "Hello"
        
        # Create personalized greeting message
        message = f"{greeting_type}, {name}! Welcome to our green-themed application. We're delighted to have you here!"
        
        # Get current timestamp
        from datetime import datetime
        timestamp = datetime.now().isoformat()
        
        return GreetingResponse(
            message=message,
            name=name,
            timestamp=timestamp
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/greet/{name}")
async def greet_user_get(name: str, greeting_type: Optional[str] = "Hello"):
    """Greet a user via GET request (alternative endpoint)"""
    try:
        if not name or len(name.strip()) == 0:
            raise HTTPException(status_code=400, detail="Name cannot be empty")
        
        name = name.strip().title()
        message = f"{greeting_type}, {name}! Nice to meet you through our API!"
        
        from datetime import datetime
        timestamp = datetime.now().isoformat()
        
        return {
            "message": message,
            "name": name,
            "timestamp": timestamp
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)