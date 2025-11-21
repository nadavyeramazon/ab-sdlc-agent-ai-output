from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

# Initialize FastAPI application
app = FastAPI()

# Configure CORS middleware to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


@app.get("/api/hello")
def get_hello():
    """Return hello message with current timestamp"""
    return {
        "message": "Hello World from Backend!",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@app.get("/health")
def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy"}
