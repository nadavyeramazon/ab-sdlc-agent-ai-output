from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import uuid4


router = APIRouter()


# In-memory storage (replace with database in production)
tasks_db = {}


class TaskBase(BaseModel):
    """Base task model."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: str = Field(default="pending", pattern="^(pending|in_progress|completed)$")


class TaskCreate(TaskBase):
    """Task creation model."""
    pass


class Task(TaskBase):
    """Task model with ID and timestamps."""
    id: str
    created_at: datetime
    updated_at: datetime


class TaskUpdate(BaseModel):
    """Task update model."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[str] = Field(None, pattern="^(pending|in_progress|completed)$")


@router.get("/tasks", response_model=List[Task])
async def list_tasks(
    status: Optional[str] = None,
    limit: int = 100,
    offset: int = 0
):
    """
    List all tasks with optional filtering.
    """
    tasks = list(tasks_db.values())
    
    # Filter by status if provided
    if status:
        tasks = [t for t in tasks if t["status"] == status]
    
    # Apply pagination
    tasks = tasks[offset:offset + limit]
    
    return tasks


@router.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: str):
    """
    Get a specific task by ID.
    """
    task = tasks_db.get(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return task


@router.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate):
    """
    Create a new task.
    """
    task_id = str(uuid4())
    now = datetime.utcnow()
    
    new_task = {
        "id": task_id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "created_at": now,
        "updated_at": now
    }
    
    tasks_db[task_id] = new_task
    return new_task


@router.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: str, task_update: TaskUpdate):
    """
    Update an existing task.
    """
    task = tasks_db.get(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    
    # Update only provided fields
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        task[field] = value
    
    task["updated_at"] = datetime.utcnow()
    tasks_db[task_id] = task
    
    return task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str):
    """
    Delete a task.
    """
    if task_id not in tasks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    
    del tasks_db[task_id]
    return None