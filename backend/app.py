from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import os

app = FastAPI(
    title="Green Greeter API",
    description="A simple FastAPI application that greets users with a green theme",
    version="1.0.0"
)

# Configure CORS with more restrictive settings for production
allowed_origins = [
    "http://localhost:3000",  # Frontend development server
    "http://localhost:8080",  # Frontend production server
    "http://frontend:8080",   # Docker container communication
]

# Allow all origins only in development
if os.getenv("ENVIRONMENT") == "development":
    allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

class GreetRequest(BaseModel):
    name: str

class GreetResponse(BaseModel):
    greeting: str
    timestamp: str

@app.get("/")
async def read_root():
    """Root endpoint that provides a welcome message."""
    return {"message": "Welcome to the Green Greeter API!"}

@app.get("/health")
async def health_check():
    """Health check endpoint for Docker health checks."""
    return {"status": "healthy"}

@app.post("/greet", response_model=GreetResponse)
async def greet_user(request: GreetRequest):
    """Greet a user with their provided name."""
    # Handle empty or whitespace-only names
    name = request.name.strip() if request.name else ""
    if not name:
        name = "Anonymous"
    
    greeting = f"🌿 Hello, {name}! Welcome to our green-themed greeter! 🌱"
    timestamp = datetime.now().isoformat()
    
    return GreetResponse(
        greeting=greeting,
        timestamp=timestamp
    )
