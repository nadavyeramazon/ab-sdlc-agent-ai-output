"""Minimal FastAPI backend for Yellow Theme Hello World application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pydantic import BaseModel, validator

app = FastAPI()

# Enable CORS for frontend running on localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GreetRequest(BaseModel):
    name: str
    
    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()


@app.get("/api/hello")
async def get_hello():
    """
    Hello World endpoint.
    
    Returns a greeting message with the current timestamp in ISO-8601 format.
    """
    return {
        "message": "Hello World from Backend!",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns the health status of the backend service.
    """
    return {"status": "healthy"}


@app.post("/api/greet")
async def greet_user(request: GreetRequest):
    """
    Personalized greeting endpoint.
    
    Accepts a name and returns a personalized greeting with timestamp.
    """
    greeting_message = f"Hello, {request.name}! Welcome to our blue-themed app!"
    return {
        "greeting": greeting_message,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
