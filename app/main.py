from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.config import settings
import os

load_dotenv()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Minimal FastAPI backend for AB SDLC Agent AI frontend client"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "ab-sdlc-agent-ai-backend",
        "version": settings.VERSION
    }


@app.get("/api/health")
async def health():
    """Detailed health check"""
    return {
        "status": "ok",
        "service": "ab-sdlc-agent-ai-backend",
        "version": settings.VERSION,
        "environment": "development" if settings.DEBUG else "production"
    }


@app.get("/api/status")
async def status():
    """Service status endpoint"""
    return {
        "online": True,
        "message": "Backend service is running"
    }
