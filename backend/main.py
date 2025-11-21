from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone

# Create FastAPI app instance
app = FastAPI()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.get("/api/hello")
def hello():
    """Hello endpoint with timestamp"""
    return {
        "message": "Hello World from Backend!",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.post("/api/greet")
async def greet_user(request_body: dict):
    """
    Personalized greeting endpoint that accepts a name and returns a greeting.
    
    Request body:
    {
        "name": "John"
    }
    
    Returns:
    {
        "greeting": "Hello, [name]! Welcome to our purple-themed app!",
        "timestamp": "2024-01-15T14:30:00.123456Z"
    }
    """
    # Validation: Check if name field exists
    if "name" not in request_body:
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    
    name = request_body.get("name", "").strip()
    
    # Validation: Check if name is not empty or whitespace-only
    if not name:
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    
    # Generate personalized greeting
    greeting_message = f"Hello, {name}! Welcome to our purple-themed app!"
    
    # Get current timestamp in ISO-8601 format
    current_timestamp = datetime.utcnow().isoformat() + "Z"
    
    return {
        "greeting": greeting_message,
        "timestamp": current_timestamp
    }
