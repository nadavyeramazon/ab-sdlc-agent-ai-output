from fastapi import APIRouter, HTTPException
from app.schemas.hello import HelloResponse, HelloRequest
from datetime import datetime

router = APIRouter()


@router.get("/", response_model=dict)
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Hello World API",
        "version": "1.0.0",
        "status": "active"
    }


@router.get("/health", response_model=dict)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/hello", response_model=HelloResponse)
async def get_hello():
    """Get hello world message"""
    return HelloResponse(
        message="Hello, World!",
        timestamp=datetime.utcnow()
    )


@router.post("/hello", response_model=HelloResponse)
async def post_hello(request: HelloRequest):
    """Post hello message with custom name"""
    if not request.name or len(request.name.strip()) == 0:
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    
    return HelloResponse(
        message=f"Hello, {request.name}!",
        timestamp=datetime.utcnow()
    )


@router.get("/hello/{name}", response_model=HelloResponse)
async def get_hello_name(name: str):
    """Get hello message with name parameter"""
    if not name or len(name.strip()) == 0:
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    
    return HelloResponse(
        message=f"Hello, {name}!",
        timestamp=datetime.utcnow()
    )