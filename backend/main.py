from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI(title="Simple Backend API", version="1.0.0")

# Enable CORS to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class Item(BaseModel):
    id: int
    name: str
    description: str

class ItemCreate(BaseModel):
    name: str
    description: str

class ItemUpdate(BaseModel):
    name: str = None
    description: str = None

# In-memory storage for demonstration
items: List[Item] = [
    Item(id=1, name="Sample Item 1", description="This is the first sample item"),
    Item(id=2, name="Sample Item 2", description="This is the second sample item"),
]

next_id = 3

@app.get("/")
def read_root():
    return {"message": "Welcome to the Simple Backend API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/items", response_model=List[Item])
def get_items():
    """Get all items"""
    return items

@app.post("/api/items", response_model=Item)
def create_item(item: ItemCreate):
    """Create a new item"""
    global next_id
    new_item = Item(id=next_id, name=item.name, description=item.description)
    items.append(new_item)
    next_id += 1
    return new_item

@app.get("/api/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    """Get item by ID"""
    for item in items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.put("/api/items/{item_id}", response_model=Item)
def update_item(item_id: int, item_update: ItemUpdate):
    """Update item by ID"""
    for i, item in enumerate(items):
        if item.id == item_id:
            if item_update.name is not None:
                item.name = item_update.name
            if item_update.description is not None:
                item.description = item_update.description
            items[i] = item
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/api/items/{item_id}")
def delete_item(item_id: int):
    """Delete item by ID"""
    for i, item in enumerate(items):
        if item.id == item_id:
            items.pop(i)
            return {"message": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")
