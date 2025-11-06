from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn
import logging
import asyncio
from typing import Optional
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Greeting Service", 
    description="A resilient greeting API with error handling",
    version="1.0.0"
)

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GreetingRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="User name to greet")

class GreetingResponse(BaseModel):
    message: str
    name: str
    status: str = "success"

class ErrorResponse(BaseModel):
    error: str
    message: str
    status: str = "error"

# Global exception handler for service unavailable exceptions
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    
    # Handle specific service unavailable scenarios
    if "serviceUnavailableException" in str(exc) or "Bedrock" in str(exc):
        logger.warning("Service unavailable exception detected, using fallback response")
        return JSONResponse(
            status_code=503,
            content={
                "error": "service_unavailable",
                "message": "External service temporarily unavailable. Using fallback response.",
                "status": "error"
            }
        )
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "message": "An unexpected error occurred. Please try again later.",
            "status": "error"
        }
    )

# Health check with detailed status
@app.get("/health")
async def health_check():
    """Enhanced health check endpoint"""
    try:
        # Simulate any external dependencies check
        await asyncio.sleep(0.1)  # Simulate health check delay
        
        return {
            "status": "healthy",
            "service": "greeting-api",
            "version": "1.0.0",
            "timestamp": "2024-01-01T00:00:00Z",
            "dependencies": {
                "database": "not_required",
                "external_services": "not_required"
            }
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service unhealthy")

@app.get("/")
async def root():
    """Root endpoint with service information"""
    return {
        "message": "Welcome to the Resilient Greeting Service API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "greet_post": "/greet",
            "greet_get": "/greet/{name}"
        }
    }

async def generate_greeting_with_fallback(name: str) -> str:
    """Generate greeting with fallback mechanism for service unavailable scenarios"""
    try:
        # Primary greeting logic (could integrate with external services)
        greeting_templates = [
            f"Hello, {name}! Welcome to our green-themed application!",
            f"Greetings, {name}! Enjoy your visit to our eco-friendly platform!",
            f"Hi {name}! Thanks for using our sustainable greeting service!",
            f"Welcome, {name}! We're delighted to see you in our green space!",
        ]
        
        # Use a simple hash to pick a consistent greeting for the same name
        greeting_index = hash(name) % len(greeting_templates)
        return greeting_templates[greeting_index]
        
    except Exception as e:
        logger.warning(f"Primary greeting generation failed: {str(e)}, using fallback")
        # Fallback greeting in case of any service issues
        return f"Hello, {name}! Welcome! (Fallback mode active)"

@app.post("/greet", response_model=GreetingResponse)
async def greet_user(request: GreetingRequest):
    """Greet a user by their name with enhanced error handling"""
    try:
        logger.info(f"Greeting request received for user: {request.name}")
        
        # Validate input
        if not request.name or not request.name.strip():
            raise HTTPException(status_code=400, detail="Name cannot be empty")
        
        # Clean the name
        clean_name = request.name.strip()
        
        # Generate greeting with fallback
        greeting_message = await generate_greeting_with_fallback(clean_name)
        
        logger.info(f"Greeting generated successfully for user: {clean_name}")
        
        return GreetingResponse(
            message=greeting_message, 
            name=clean_name,
            status="success"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in greet_user: {str(e)}", exc_info=True)
        
        # Handle service unavailable scenarios specifically
        if "serviceUnavailableException" in str(e) or "Bedrock" in str(e):
            logger.warning("Bedrock service unavailable, using fallback greeting")
            fallback_message = f"Hello, {request.name}! Welcome! (Service temporarily unavailable)"
            return GreetingResponse(
                message=fallback_message,
                name=request.name,
                status="success"
            )
        
        raise HTTPException(status_code=500, detail="Internal server error occurred")

@app.get("/greet/{name}", response_model=GreetingResponse)
async def greet_user_get(name: str):
    """Greet a user by their name via GET request with enhanced error handling"""
    try:
        logger.info(f"GET greeting request received for user: {name}")
        
        # Validate input
        if not name or not name.strip():
            raise HTTPException(status_code=400, detail="Name cannot be empty")
        
        if len(name) > 100:
            raise HTTPException(status_code=400, detail="Name too long")
        
        # Clean the name
        clean_name = name.strip()
        
        # Generate greeting with fallback
        greeting_message = await generate_greeting_with_fallback(clean_name)
        
        logger.info(f"GET greeting generated successfully for user: {clean_name}")
        
        return GreetingResponse(
            message=greeting_message, 
            name=clean_name,
            status="success"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in greet_user_get: {str(e)}", exc_info=True)
        
        # Handle service unavailable scenarios specifically
        if "serviceUnavailableException" in str(e) or "Bedrock" in str(e):
            logger.warning("Bedrock service unavailable, using fallback greeting")
            fallback_message = f"Hello, {name}! Welcome! (Service temporarily unavailable)"
            return GreetingResponse(
                message=fallback_message,
                name=name,
                status="success"
            )
        
        raise HTTPException(status_code=500, detail="Internal server error occurred")

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("🌿 Greeting Service starting up...")
    logger.info("✅ Service startup completed successfully")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🛑 Greeting Service shutting down...")
    logger.info("✅ Service shutdown completed successfully")

if __name__ == "__main__":
    logger.info("Starting Greeting Service...")
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_level="info",
        access_log=True
    )