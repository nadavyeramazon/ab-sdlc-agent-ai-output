from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os

app = FastAPI(
    title="Greeting API",
    description="A simple API that greets users by name",
    version="1.0.0"
)

# Configure CORS
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GreetingRequest(BaseModel):
    name: str
    message: Optional[str] = None

class GreetingResponse(BaseModel):
    greeting: str
    name: str
    timestamp: str

@app.get("/")
async def root():
    """Welcome endpoint"""
    return {
        "message": "Welcome to the Greeting API!",
        "version": "1.0.0",
        "endpoints": {
            "greet": "/greet (POST)",
            "health": "/health (GET)",
            "docs": "/docs (GET)"
        }
    }

@app.post("/greet", response_model=GreetingResponse)
async def greet_user(request: GreetingRequest):
    """Greet a user by name"""
    if not request.name or request.name.strip() == "":
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    
    # Clean the name
    clean_name = request.name.strip().title()
    
    # Create personalized greeting
    if request.message:
        greeting = f"Hello {clean_name}! {request.message}"
    else:
        greeting = f"Hello {clean_name}! Welcome to our green-themed application!"
    
    from datetime import datetime
    timestamp = datetime.now().isoformat()
    
    return GreetingResponse(
        greeting=greeting,
        name=clean_name,
        timestamp=timestamp
    )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "greeting-api",
        "version": "1.0.0"
    }

@app.get("/greet/{name}")
async def greet_user_get(name: str, message: Optional[str] = None):
    """Alternative GET endpoint for greeting"""
    request = GreetingRequest(name=name, message=message)
    return await greet_user(request)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)