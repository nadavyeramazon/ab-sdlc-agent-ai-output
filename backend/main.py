from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Hello World Backend API",
    description="Green Theme Hello World Fullstack Application Backend",
    version="1.0.0"
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request, call_next):
    """Log all incoming requests with timestamp and endpoint"""
    logger.info(f"Request: {request.method} {request.url.path}")
    response = await call_next(request)
    return response


@app.get("/api/hello")
async def get_hello():
    """
    Returns a greeting message with ISO 8601 timestamp.
    
    Returns:
        dict: JSON response with message and timestamp
    """
    current_time = datetime.utcnow().isoformat() + "Z"
    logger.info(f"Returning hello message at {current_time}")
    return {
        "message": "Hello World from Backend!",
        "timestamp": current_time
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify backend service availability.
    
    Returns:
        dict: JSON response with health status
    """
    logger.info("Health check requested")
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
