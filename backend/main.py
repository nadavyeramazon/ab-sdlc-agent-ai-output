from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Green Theme API",
    description="Backend API for the Green Theme Application",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class MessageRequest(BaseModel):
    message: str

class MessageResponse(BaseModel):
    received_message: str
    response: str
    timestamp: str

# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint - Returns welcome message
    """
    logger.info("Root endpoint called")
    return {
        "message": "Welcome to Green Theme API",
        "status": "active",
        "version": "1.0.0",
        "endpoints": [
            "/",
            "/health",
            "/message",
            "/docs"
        ]
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    logger.info("Health check called")
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

# Message endpoint
@app.post("/message", response_model=MessageResponse)
async def send_message(request: MessageRequest):
    """
    Receive and process a message from the frontend
    """
    logger.info(f"Message received: {request.message}")
    
    if not request.message or len(request.message.strip()) == 0:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    # Process the message (simple echo with enhancement)
    response_text = f"Thank you for your message! I received: '{request.message}'"
    
    return MessageResponse(
        received_message=request.message,
        response=response_text,
        timestamp=datetime.now().isoformat()
    )

# Data endpoint with sample data
@app.get("/data")
async def get_data():
    """
    Returns sample data
    """
    logger.info("Data endpoint called")
    return {
        "data": [
            {"id": 1, "name": "Green Leaf", "value": 100},
            {"id": 2, "name": "Forest", "value": 200},
            {"id": 3, "name": "Nature", "value": 300},
        ],
        "total": 3,
        "timestamp": datetime.now().isoformat()
    }

# Info endpoint
@app.get("/info")
async def get_info():
    """
    Returns application information
    """
    return {
        "app_name": "Green Theme Backend",
        "framework": "FastAPI",
        "python_version": "3.11",
        "features": [
            "RESTful API",
            "CORS enabled",
            "Automatic API documentation",
            "Request validation",
            "Docker ready"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)