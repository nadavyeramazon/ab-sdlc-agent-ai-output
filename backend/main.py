from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

# Initialize FastAPI application
app = FastAPI()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type"],
)


# Pydantic model for POST /api/greet request
class GreetRequest(BaseModel):
    name: str


@app.get("/api/hello")
def hello():
    """Return a greeting message with current timestamp"""
    return {
        "message": "Hello World from Backend!",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/health")
def health():
    """Return health status of the service"""
    return {"status": "healthy"}


@app.post("/api/greet")
async def greet_user(request: GreetRequest):
    """Return personalized greeting for the provided name"""
    # Strip whitespace from name
    name = request.name.strip()
    
    # Validate name is not empty
    if not name:
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    
    # Generate personalized greeting
    greeting_message = f"Hello, {name}! Welcome to our purple-themed app!"
    
    # Generate ISO-8601 timestamp
    timestamp = datetime.utcnow().isoformat() + "Z"
    
    # Return response
    return {
        "greeting": greeting_message,
        "timestamp": timestamp
    }
