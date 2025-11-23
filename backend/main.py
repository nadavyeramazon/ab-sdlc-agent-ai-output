from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pydantic import BaseModel, validator
from typing import Optional
import uuid

# Initialize FastAPI application with redirect_slashes disabled
# This ensures that routes with trailing slashes are not automatically redirected
# and will return 404 if not explicitly defined
app = FastAPI(redirect_slashes=False)

# Configure CORS middleware to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


# Task Manager Data Models

class TaskCreate(BaseModel):
    """Request model for creating a new task."""
    title: str
    description: str = ""
    
    @validator('title')
    def title_not_empty(cls, v):
        """
        Validate that title is not empty or whitespace-only.
        Automatically trims leading/trailing whitespace.
        Max length: 200 characters.
        
        Args:
            v: The title value to validate
            
        Returns:
            Trimmed title string
            
        Raises:
            ValueError: If title is empty, whitespace-only, or exceeds 200 characters
        """
        if not v or not v.strip():
            raise ValueError('Title cannot be empty')
        if len(v.strip()) > 200:
            raise ValueError('Title cannot exceed 200 characters')
        return v.strip()
    
    @validator('description')
    def description_length(cls, v):
        """
        Validate that description does not exceed maximum length.
        Max length: 1000 characters.
        
        Args:
            v: The description value to validate
            
        Returns:
            Description string
            
        Raises:
            ValueError: If description exceeds 1000 characters
        """
        if len(v) > 1000:
            raise ValueError('Description cannot exceed 1000 characters')
        return v


class TaskUpdate(BaseModel):
    """Request model for updating an existing task."""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    
    @validator('title')
    def title_not_empty(cls, v):
        """
        Validate that title is not empty or whitespace-only when provided.
        Automatically trims leading/trailing whitespace.
        Max length: 200 characters.
        
        Args:
            v: The title value to validate (can be None)
            
        Returns:
            Trimmed title string or None
            
        Raises:
            ValueError: If title is empty, whitespace-only, or exceeds 200 characters
        """
        if v is not None:
            if not v or not v.strip():
                raise ValueError('Title cannot be empty')
            if len(v.strip()) > 200:
                raise ValueError('Title cannot exceed 200 characters')
            return v.strip()
        return v
    
    @validator('description')
    def description_length(cls, v):
        """
        Validate that description does not exceed maximum length when provided.
        Max length: 1000 characters.
        
        Args:
            v: The description value to validate (can be None)
            
        Returns:
            Description string or None
            
        Raises:
            ValueError: If description exceeds 1000 characters
        """
        if v is not None and len(v) > 1000:
            raise ValueError('Description cannot exceed 1000 characters')
        return v


class Task(BaseModel):
    """Complete task model with all fields."""
    id: str
    title: str
    description: str = ""
    completed: bool = False
    created_at: str
    updated_at: str
    
    @classmethod
    def create_new(cls, task_data: TaskCreate) -> "Task":
        """
        Factory method to create a new Task from TaskCreate data.
        Automatically generates UUID and timestamps.
        
        Args:
            task_data: TaskCreate instance with title and description
            
        Returns:
            New Task instance with generated id and timestamps
        """
        now = datetime.utcnow().isoformat() + "Z"
        return cls(
            id=str(uuid.uuid4()),
            title=task_data.title,
            description=task_data.description,
            completed=False,
            created_at=now,
            updated_at=now
        )
    
    def update_from(self, update_data: TaskUpdate) -> "Task":
        """
        Create an updated copy of the task with new values.
        Only updates fields that are provided (not None).
        Automatically updates the updated_at timestamp.
        
        Args:
            update_data: TaskUpdate instance with fields to update
            
        Returns:
            New Task instance with updated values
        """
        updated_fields = {}
        if update_data.title is not None:
            updated_fields['title'] = update_data.title
        if update_data.description is not None:
            updated_fields['description'] = update_data.description
        if update_data.completed is not None:
            updated_fields['completed'] = update_data.completed
        
        updated_fields['updated_at'] = datetime.utcnow().isoformat() + "Z"
        
        return self.copy(update=updated_fields)


@app.get("/health")
def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy"}


# Task Manager API Endpoints

# Initialize task repository (lazy initialization to avoid circular import)
_task_repository = None

def get_task_repository():
    """Get or create the task repository instance."""
    global _task_repository
    if _task_repository is None:
        from task_repository import TaskRepository
        _task_repository = TaskRepository()
    return _task_repository


@app.get("/api/tasks")
def get_all_tasks():
    """
    Retrieve all tasks.
    
    Returns:
        JSON response containing list of all tasks ordered by creation date (newest first)
        
    Example:
        Response: {
            "tasks": [
                {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "title": "Buy groceries",
                    "description": "Milk, eggs, bread",
                    "completed": false,
                    "created_at": "2024-01-15T10:30:00.000000Z",
                    "updated_at": "2024-01-15T10:30:00.000000Z"
                }
            ]
        }
    """
    repository = get_task_repository()
    tasks = repository.get_all()
    return {"tasks": [task.dict() for task in tasks]}


@app.post("/api/tasks", status_code=201)
def create_task(task_data: TaskCreate):
    """
    Create a new task.
    
    Args:
        task_data: TaskCreate object with title and description
        
    Returns:
        Created task object with generated ID and timestamps
        
    Raises:
        HTTPException 422: If validation fails (empty title, too long, etc.)
        
    Example:
        Request: {"title": "Buy groceries", "description": "Milk, eggs, bread"}
        Response: {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "completed": false,
            "created_at": "2024-01-15T10:30:00.000000Z",
            "updated_at": "2024-01-15T10:30:00.000000Z"
        }
    """
    repository = get_task_repository()
    task = repository.create(task_data)
    return task.dict()


@app.get("/api/tasks/{task_id}")
def get_task(task_id: str):
    """
    Retrieve a single task by ID.
    
    Args:
        task_id: The unique identifier of the task
        
    Returns:
        Task object if found
        
    Raises:
        HTTPException 404: If task with given ID is not found
        
    Example:
        Response: {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "completed": false,
            "created_at": "2024-01-15T10:30:00.000000Z",
            "updated_at": "2024-01-15T10:30:00.000000Z"
        }
    """
    repository = get_task_repository()
    task = repository.get_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task.dict()


@app.put("/api/tasks/{task_id}")
def update_task(task_id: str, task_data: TaskUpdate):
    """
    Update an existing task.
    
    Args:
        task_id: The unique identifier of the task to update
        task_data: TaskUpdate object with fields to update
        
    Returns:
        Updated task object
        
    Raises:
        HTTPException 404: If task with given ID is not found
        HTTPException 422: If validation fails (empty title, too long, etc.)
        
    Example:
        Request: {"title": "Buy groceries and cook", "completed": true}
        Response: {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "title": "Buy groceries and cook",
            "description": "Milk, eggs, bread",
            "completed": true,
            "created_at": "2024-01-15T10:30:00.000000Z",
            "updated_at": "2024-01-15T10:35:00.000000Z"
        }
    """
    repository = get_task_repository()
    task = repository.update(task_id, task_data)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task.dict()


@app.delete("/api/tasks/{task_id}", status_code=204)
def delete_task(task_id: str):
    """
    Delete a task.
    
    Args:
        task_id: The unique identifier of the task to delete
        
    Returns:
        No content (204 status)
        
    Raises:
        HTTPException 404: If task with given ID is not found
        
    Example:
        Response: No content with 204 status code
    """
    repository = get_task_repository()
    success = repository.delete(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return None
