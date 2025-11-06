from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
import os
from typing import Optional
import re

app = FastAPI(
    title="Greeting API",
    description="A simple FastAPI application that greets users with customizable greetings",
    version="1.0.0"
)

# Secure CORS configuration
allowed_origins = [
    "http://localhost:3000",  # Frontend development
    "http://localhost:8080",  # Frontend production
    "http://frontend:8080",   # Docker internal communication
]

# Add environment variable for additional origins in production
if additional_origins := os.getenv("ADDITIONAL_CORS_ORIGINS"):
    allowed_origins.extend(additional_origins.split(","))

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

class GreetingRequest(BaseModel):
    name: str
    greeting_type: Optional[str] = "hello"
    
    @validator('name')
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Name cannot be empty')
        if len(v.strip()) > 100:
            raise ValueError('Name too long (max 100 characters)')
        # Basic XSS prevention
        if re.search(r'[<>"\']', v):
            raise ValueError('Name contains invalid characters')
        return v.strip()
    
    @validator('greeting_type')
    def validate_greeting_type(cls, v):
        valid_types = ["hello", "hi", "hey", "greetings", "welcome"]
        if v not in valid_types:
            raise ValueError(f'Invalid greeting type. Must be one of: {", ".join(valid_types)}')
        return v

class GreetingResponse(BaseModel):
    message: str
    name: str
    greeting_type: str

@app.get("/")
async def root():
    return {"message": "Welcome to the Greeting API! Use /greet to get personalized greetings."}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "greeting-api"}

@app.post("/greet", response_model=GreetingResponse)
async def greet_user(request: GreetingRequest):
    """
    Greet a user with a personalized message.
    
    - **name**: The name of the person to greet (required, max 100 chars)
    - **greeting_type**: Type of greeting (optional, defaults to 'hello')
    """
    try:
        greeting_messages = {
            "hello": f"Hello, {request.name}! Nice to meet you!",
            "hi": f"Hi there, {request.name}! How are you doing?",
            "hey": f"Hey {request.name}! What's up?",
            "greetings": f"Greetings, {request.name}! Hope you're having a great day!",
            "welcome": f"Welcome, {request.name}! We're glad you're here!"
        }
        
        message = greeting_messages.get(request.greeting_type, f"Hello, {request.name}!")
        
        return GreetingResponse(
            message=message,
            name=request.name,
            greeting_type=request.greeting_type
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/greet/{name}")
async def greet_user_get(name: str, greeting_type: str = "hello"):
    """
    Greet a user via GET request.
    
    - **name**: The name of the person to greet
    - **greeting_type**: Type of greeting (optional, defaults to 'hello')
    """
    try:
        # Create a request object for validation
        request = GreetingRequest(name=name, greeting_type=greeting_type)
        return await greet_user(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)