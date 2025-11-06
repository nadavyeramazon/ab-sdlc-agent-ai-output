from fastapi import FastAPI
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
