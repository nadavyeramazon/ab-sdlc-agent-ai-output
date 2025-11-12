"""FastAPI Backend for Purple Theme Hello World Application

Provides REST API endpoints for the frontend application.
"""
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator

# Create FastAPI app
app = FastAPI(
    title="Hello World Backend API",
    description="Backend API for Purple Theme Hello World Application",
    version="2.0.0"
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


# Request models
class GreetRequest(BaseModel):
    """Request model for /api/greet endpoint"""
    name: str
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate that name is not empty or whitespace-only"""
        if not v or not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()


# Response models
class HelloResponse(BaseModel):
    """Response model for /api/hello endpoint"""
    message: str
    timestamp: str


class GreetResponse(BaseModel):
    """Response model for /api/greet endpoint"""
    greeting: str
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


@app.post("/api/greet", response_model=GreetResponse)
async def post_greet(request: GreetRequest) -> GreetResponse:
    """Return personalized greeting with timestamp
    
    Args:
        request: GreetRequest with name field
        
    Returns:
        GreetResponse: JSON with personalized greeting and timestamp
        
    Raises:
        HTTPException: 400 if name is invalid
    """
    try:
        # The validator already ensures name is not empty/whitespace
        greeting_text = f"Hello, {request.name}! Welcome to our purple-themed app!"
        return GreetResponse(
            greeting=greeting_text,
            timestamp=datetime.now().isoformat()
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


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
