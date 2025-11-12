"""FastAPI Backend for Green Theme Hello World Application

Provides REST API endpoints for the frontend application.
"""
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Create FastAPI app
app = FastAPI(
    title="Hello World Backend API",
    description="Backend API for Green Theme Hello World Application",
    version="1.0.0"
)

# Configure CORS to allow frontend communication
# Supports both Docker service name and localhost for development
origins = [
    "http://frontend:3000",
    "http://localhost:3000",
    "http://localhost:5173",  # Vite dev server default port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Response models
class HelloResponse(BaseModel):
    """Response model for /api/hello endpoint"""
    message: str
    timestamp: str


class HealthResponse(BaseModel):
    """Response model for /health endpoint"""
    status: str


@app.get("/api/hello", response_model=HelloResponse)
async def get_hello() -> HelloResponse:
    """Return hello message with timestamp
    
    Returns:
        HelloResponse: JSON with message and timestamp
    """
    return HelloResponse(
        message="Hello World from Backend!",
        timestamp=datetime.now().isoformat()
    )


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint
    
    Returns:
        HealthResponse: JSON with status
    """
    return HealthResponse(status="healthy")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
