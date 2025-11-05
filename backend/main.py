from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

app = FastAPI(title="Backend API", version="1.0.0")

# Configure CORS with specific origins for security
# Get frontend URL from environment variable, default to localhost for development
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, "http://frontend:3000"],  # Specific origins for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint returning howdy message"""
    return {
        "message": "Howdy! from Backend!",
        "service": "backend",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "backend"}

@app.get("/api/greeting")
async def get_greeting(name: str = "World"):
    """Get a personalized greeting"""
    return {
        "greeting": f"Hello, {name}!",
        "from": "Backend Service"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
