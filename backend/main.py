from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="Greeting API",
    description="A simple FastAPI application that greets users by input",
    version="1.0.0"
)

# Configure CORS to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class GreetingRequest(BaseModel):
    name: str
    greeting_type: Optional[str] = "hello"

class GreetingResponse(BaseModel):
    message: str
    user_name: str
    greeting_type: str

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to the Greeting API!",
        "status": "running",
        "version": "1.0.0"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Main greeting endpoint
@app.post("/greet", response_model=GreetingResponse)
async def greet_user(request: GreetingRequest):
    """
    Greet a user by their input name with different greeting types
    """
    if not request.name.strip():
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    
    # Different greeting types
    greetings = {
        "hello": f"Hello, {request.name}! Welcome to our green-themed application!",
        "hi": f"Hi there, {request.name}! Great to see you!",
        "welcome": f"Welcome, {request.name}! We're excited to have you here!",
        "good_morning": f"Good morning, {request.name}! Hope you have a wonderful day!",
        "good_afternoon": f"Good afternoon, {request.name}! Hope your day is going well!",
        "good_evening": f"Good evening, {request.name}! Hope you had a great day!"
    }
    
    greeting_message = greetings.get(
        request.greeting_type, 
        f"Hello, {request.name}! Welcome to our application!"
    )
    
    return GreetingResponse(
        message=greeting_message,
        user_name=request.name,
        greeting_type=request.greeting_type
    )

# Get available greeting types
@app.get("/greeting-types")
async def get_greeting_types():
    return {
        "greeting_types": [
            {"key": "hello", "label": "Hello"},
            {"key": "hi", "label": "Hi"},
            {"key": "welcome", "label": "Welcome"},
            {"key": "good_morning", "label": "Good Morning"},
            {"key": "good_afternoon", "label": "Good Afternoon"},
            {"key": "good_evening", "label": "Good Evening"}
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
