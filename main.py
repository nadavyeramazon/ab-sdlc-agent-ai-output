import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="AB SDLC Agent AI Backend",
    description="Minimal FastAPI backend for AB SDLC Agent AI",
    version="1.0.0"
)

# CORS configuration with security best practices
# Default to localhost only; override with CORS_ORIGINS environment variable
allowed_origins = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:3000,http://localhost:5173"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    version: str = "1.0.0"

class MessageResponse(BaseModel):
    """Standard message response model"""
    message: str

@app.get("/", response_model=MessageResponse)
def root():
    """Root endpoint returning service information"""
    return {"message": "AB SDLC Agent AI Backend"}

@app.get("/health", response_model=HealthResponse)
def health():
    """Health check endpoint for monitoring"""
    return {"status": "ok", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)