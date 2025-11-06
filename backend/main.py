from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from typing import List, Optional
import re

# Pydantic models for input validation
class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = ""
    price: float
    category: str
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Name cannot be empty')
        if len(v) > 100:
            raise ValueError('Name cannot exceed 100 characters')
        # Basic sanitization - remove any potentially harmful characters
        if re.search(r'[<>"\'\/]', v):
            raise ValueError('Name contains invalid characters')
        return v.strip()
    
    @field_validator('description')
    @classmethod
    def validate_description(cls, v):
        if v and len(v) > 500:
            raise ValueError('Description cannot exceed 500 characters')
        return v.strip() if v else ""
    
    @field_validator('price')
    @classmethod
    def validate_price(cls, v):
        if v < 0:
            raise ValueError('Price cannot be negative')
        if v > 999999.99:
            raise ValueError('Price cannot exceed 999999.99')
        return round(v, 2)
    
    @field_validator('category')
    @classmethod
    def validate_category(cls, v):
        allowed_categories = ['electronics', 'clothing', 'food', 'books', 'home', 'sports', 'other']
        if v.lower() not in allowed_categories:
            raise ValueError(f'Category must be one of: {", ".join(allowed_categories)}')
        return v.lower()

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if v is not None:
            if not v or len(v.strip()) == 0:
                raise ValueError('Name cannot be empty')
            if len(v) > 100:
                raise ValueError('Name cannot exceed 100 characters')
            if re.search(r'[<>"\'\/]', v):
                raise ValueError('Name contains invalid characters')
            return v.strip()
        return v
    
    @field_validator('description')
    @classmethod
    def validate_description(cls, v):
        if v is not None and len(v) > 500:
            raise ValueError('Description cannot exceed 500 characters')
        return v.strip() if v else ""
    
    @field_validator('price')
    @classmethod
    def validate_price(cls, v):
        if v is not None:
            if v < 0:
                raise ValueError('Price cannot be negative')
            if v > 999999.99:
                raise ValueError('Price cannot exceed 999999.99')
            return round(v, 2)
        return v
    
    @field_validator('category')
    @classmethod
    def validate_category(cls, v):
        if v is not None:
            allowed_categories = ['electronics', 'clothing', 'food', 'books', 'home', 'sports', 'other']
            if v.lower() not in allowed_categories:
                raise ValueError(f'Category must be one of: {", ".join(allowed_categories)}')
            return v.lower()
        return v

class Item(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category: str

# Initialize FastAPI app
app = FastAPI(
    title="Simple Item Management API",
    description="A simple API for managing items with CRUD operations",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],  # Restrict to known origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# In-memory storage (replace with database in production)
items: List[Item] = []
next_id = 1

@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint"""
    return {"message": "Item Management API is running", "status": "healthy"}

@app.get("/items", response_model=List[Item], tags=["Items"])
async def get_items():
    """Get all items"""
    try:
        return items
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve items"
        )

@app.get("/items/{item_id}", response_model=Item, tags=["Items"])
async def get_item(item_id: int):
    """Get a specific item by ID"""
    try:
        if item_id < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Item ID must be a positive integer"
            )
        
        for item in items:
            if item.id == item_id:
                return item
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve item"
        )

@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED, tags=["Items"])
async def create_item(item: ItemCreate):
    """Create a new item"""
    global next_id
    try:
        new_item = Item(
            id=next_id,
            name=item.name,
            description=item.description,
            price=item.price,
            category=item.category
        )
        items.append(new_item)
        next_id += 1
        return new_item
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create item"
        )

@app.put("/items/{item_id}", response_model=Item, tags=["Items"])
async def update_item(item_id: int, item_update: ItemUpdate):
    """Update an existing item"""
    try:
        if item_id < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Item ID must be a positive integer"
            )
        
        for i, item in enumerate(items):
            if item.id == item_id:
                update_data = item_update.model_dump(exclude_unset=True)
                if not update_data:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="No fields to update"
                    )
                
                updated_item = item.model_copy(update=update_data)
                items[i] = updated_item
                return updated_item
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update item"
        )

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Items"])
async def delete_item(item_id: int):
    """Delete an item"""
    try:
        if item_id < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Item ID must be a positive integer"
            )
        
        for i, item in enumerate(items):
            if item.id == item_id:
                items.pop(i)
                return
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item"
        )