"""FastAPI Backend Application

A comprehensive FastAPI backend with health checks, CORS, and example endpoints.
"""

from fastapi import FastAPI, HTTPException, status, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AB-SDLC Agent AI Backend",
    description="Backend service for the AB-SDLC Agent AI system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===========================
# Pydantic Models
# ===========================

class HealthResponse(BaseModel):
    """Health check response model"""
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(..., description="Current timestamp")
    version: str = Field(..., description="API version")


class ItemBase(BaseModel):
    """Base item model"""
    name: str = Field(..., min_length=1, max_length=100, description="Item name")
    description: Optional[str] = Field(None, max_length=500, description="Item description")
    price: float = Field(..., gt=0, description="Item price (must be positive)")
    tags: Optional[List[str]] = Field(default=[], description="Item tags")

    @validator('price')
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('Price must be positive')
        return round(v, 2)


class ItemCreate(ItemBase):
    """Model for creating items"""
    pass


class Item(ItemBase):
    """Full item model with ID"""
    id: int = Field(..., description="Unique item identifier")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Example Item",
                "description": "This is an example item",
                "price": 29.99,
                "tags": ["example", "demo"],
                "created_at": "2024-01-01T12:00:00",
                "updated_at": "2024-01-01T12:00:00"
            }
        }


class Message(BaseModel):
    """Generic message response"""
    message: str = Field(..., description="Response message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional details")


# ===========================
# In-Memory Data Store
# ===========================

items_db: Dict[int, Item] = {}
next_item_id = 1


# ===========================
# Helper Functions
# ===========================

def get_item_by_id(item_id: int) -> Item:
    """Retrieve an item by ID or raise 404"""
    if item_id not in items_db:
        logger.warning(f"Item with ID {item_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found"
        )
    return items_db[item_id]


# ===========================
# API Endpoints
# ===========================

@app.get("/", response_model=Message, tags=["Root"])
async def root():
    """Root endpoint with welcome message"""
    logger.info("Root endpoint accessed")
    return Message(
        message="Welcome to AB-SDLC Agent AI Backend API",
        details={
            "documentation": "/docs",
            "redoc": "/redoc",
            "health": "/health"
        }
    )


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    logger.info("Health check performed")
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        version="1.0.0"
    )


@app.get("/items", response_model=List[Item], tags=["Items"])
async def list_items(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of items to return"),
    tag: Optional[str] = Query(None, description="Filter by tag")
):
    """List all items with pagination and optional filtering"""
    logger.info(f"Listing items: skip={skip}, limit={limit}, tag={tag}")
    
    items = list(items_db.values())
    
    # Filter by tag if provided
    if tag:
        items = [item for item in items if tag in item.tags]
    
    # Apply pagination
    items = items[skip:skip + limit]
    
    logger.info(f"Returning {len(items)} items")
    return items


@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED, tags=["Items"])
async def create_item(item_data: ItemCreate):
    """Create a new item"""
    global next_item_id
    
    logger.info(f"Creating new item: {item_data.name}")
    
    now = datetime.utcnow()
    new_item = Item(
        id=next_item_id,
        name=item_data.name,
        description=item_data.description,
        price=item_data.price,
        tags=item_data.tags or [],
        created_at=now,
        updated_at=now
    )
    
    items_db[next_item_id] = new_item
    next_item_id += 1
    
    logger.info(f"Item created successfully with ID: {new_item.id}")
    return new_item


@app.get("/items/{item_id}", response_model=Item, tags=["Items"])
async def get_item(item_id: int):
    """Get a specific item by ID"""
    logger.info(f"Retrieving item with ID: {item_id}")
    item = get_item_by_id(item_id)
    return item


@app.put("/items/{item_id}", response_model=Item, tags=["Items"])
async def update_item(item_id: int, item_data: ItemCreate):
    """Update an existing item"""
    logger.info(f"Updating item with ID: {item_id}")
    
    existing_item = get_item_by_id(item_id)
    
    updated_item = Item(
        id=existing_item.id,
        name=item_data.name,
        description=item_data.description,
        price=item_data.price,
        tags=item_data.tags or [],
        created_at=existing_item.created_at,
        updated_at=datetime.utcnow()
    )
    
    items_db[item_id] = updated_item
    
    logger.info(f"Item {item_id} updated successfully")
    return updated_item


@app.delete("/items/{item_id}", response_model=Message, tags=["Items"])
async def delete_item(item_id: int):
    """Delete an item"""
    logger.info(f"Deleting item with ID: {item_id}")
    
    item = get_item_by_id(item_id)
    del items_db[item_id]
    
    logger.info(f"Item {item_id} deleted successfully")
    return Message(
        message="Item deleted successfully",
        details={"id": item_id, "name": item.name}
    )


@app.get("/stats", response_model=Dict[str, Any], tags=["Statistics"])
async def get_statistics():
    """Get statistics about the items in the database"""
    logger.info("Retrieving statistics")
    
    if not items_db:
        return {
            "total_items": 0,
            "average_price": 0,
            "total_value": 0,
            "unique_tags": []
        }
    
    items = list(items_db.values())
    total_items = len(items)
    total_value = sum(item.price for item in items)
    average_price = total_value / total_items if total_items > 0 else 0
    
    # Collect unique tags
    all_tags = set()
    for item in items:
        all_tags.update(item.tags)
    
    stats = {
        "total_items": total_items,
        "average_price": round(average_price, 2),
        "total_value": round(total_value, 2),
        "unique_tags": sorted(list(all_tags))
    }
    
    logger.info(f"Statistics: {stats}")
    return stats


# ===========================
# Exception Handlers
# ===========================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    logger.error(f"HTTP Exception: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail, "status_code": exc.status_code}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler for unexpected errors"""
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": "An unexpected error occurred",
            "status_code": 500
        }
    )


# ===========================
# Startup/Shutdown Events
# ===========================

@app.on_event("startup")
async def startup_event():
    """Execute on application startup"""
    logger.info("="*50)
    logger.info("AB-SDLC Agent AI Backend starting...")
    logger.info("Version: 1.0.0")
    logger.info("="*50)
    
    # Initialize with some example data
    global next_item_id
    now = datetime.utcnow()
    
    example_items = [
        Item(
            id=1,
            name="Sample Product A",
            description="This is a sample product",
            price=19.99,
            tags=["sample", "demo"],
            created_at=now,
            updated_at=now
        ),
        Item(
            id=2,
            name="Sample Product B",
            description="Another sample product",
            price=39.99,
            tags=["sample", "premium"],
            created_at=now,
            updated_at=now
        )
    ]
    
    for item in example_items:
        items_db[item.id] = item
    
    next_item_id = len(items_db) + 1
    logger.info(f"Initialized with {len(items_db)} example items")


@app.on_event("shutdown")
async def shutdown_event():
    """Execute on application shutdown"""
    logger.info("="*50)
    logger.info("AB-SDLC Agent AI Backend shutting down...")
    logger.info("="*50)


# ===========================
# Main Entry Point
# ===========================

if __name__ == "__main__":
    import uvicorn
    
    # Run the application
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
