from typing import Dict, Any
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

__version__ = '1.0.0'

app = FastAPI(
    title="Hello World API",
    description="A simple Hello World API with enhanced features",
    version=__version__,
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Rate limiter configuration
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_version_header(request: Request, call_next) -> Response:
    """Middleware to add API version header to all responses."""
    response = await call_next(request)
    response.headers["X-API-Version"] = __version__
    return response

@app.get("/", response_model=Dict[str, str])
@limiter.limit("5/minute")
async def hello_world(request: Request) -> Dict[str, str]:
    """Return a hello world message.
    
    Returns:
        Dict[str, str]: A dictionary containing a greeting message
    """
    return {"message": "Hello, World!"}

@app.get("/health", response_model=Dict[str, str])
async def health_check() -> Dict[str, str]:
    """Health check endpoint for monitoring.
    
    Returns:
        Dict[str, str]: A dictionary containing the API status
    """
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
