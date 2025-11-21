from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="Yellow Theme Hello World API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GreetingResponse(BaseModel):
    message: str
    theme: str
    timestamp: str

@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {
        "name": "Yellow Theme Hello World API",
        "version": "1.0.0",
        "description": "A simple FastAPI backend with yellow theme"
    }

@app.get("/api/greeting", response_model=GreetingResponse)
async def get_greeting():
    """Get a cheerful yellow-themed greeting."""
    return GreetingResponse(
        message="Hello World from Yellow Theme! 🌟",
        theme="yellow",
        timestamp=datetime.now().isoformat()
    )

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "backend"}
