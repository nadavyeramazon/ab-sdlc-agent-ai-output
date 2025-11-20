from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
