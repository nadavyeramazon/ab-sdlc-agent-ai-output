"""Hello World API implementation with rate limiting and request tracking."""

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import uuid

from .config import settings

app = FastAPI(title="Hello World API",
             description="A simple Hello World API with rate limiting",
             version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    """Add a unique request ID to all responses."""
    request_id = str(uuid.uuid4())
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response

@app.get("/")
@limiter.limit(f"{settings.rate_limit_requests}/{settings.rate_limit_window}s")
async def hello_world(request: Request):
    """Return a Hello World message.
    
    Returns:
        dict: A greeting message
    """
    return {"message": "Hello, World!"}

@app.get("/health")
async def health_check():
    """Health check endpoint.
    
    Returns:
        dict: API health status
    """
    return {"status": "healthy"}

@app.exception_handler(404)
async def custom_404_handler(request: Request, exc):
    """Custom 404 error handler.
    
    Args:
        request (Request): The incoming request
        exc: The exception raised
    
    Returns:
        JSONResponse: Custom 404 error message
    """
    return JSONResponse(
        status_code=404,
        content={"error": "The requested resource was not found"}
    )
