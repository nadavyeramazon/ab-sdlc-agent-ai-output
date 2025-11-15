"""FastAPI backend for Hello World fullstack application.

Provides two endpoints:
- /api/hello: Returns greeting message with timestamp
- /health: Health check endpoint for monitoring
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Hello World API",
    description="A simple API that returns greeting messages",
    version="1.0.0"
)

# Configure CORS to allow requests from frontend
origins = [
    "http://localhost:3000",  # React development server
    "http://127.0.0.1:3000",  # Alternative localhost
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)


@app.get("/api/hello")
async def hello():
    """Return greeting message with current timestamp.
    
    Returns:
        dict: JSON object with message and ISO 8601 timestamp
    """
    timestamp = datetime.utcnow().isoformat() + "Z"
    logger.info(f"Hello endpoint called at {timestamp}")
    return {
        "message": "Hello World from Backend!",
        "timestamp": timestamp
    }


@app.get("/health")
async def health():
    """Health check endpoint for monitoring.
    
    Returns:
        dict: JSON object with health status
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
