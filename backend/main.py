from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone

# Create FastAPI app instance
app = FastAPI()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET"],
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
