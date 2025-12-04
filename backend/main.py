"""
FastAPI Task Manager Application.

This module provides a RESTful API for managing tasks with CRUD operations.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import TaskCreate, TaskUpdate
from task_repository import TaskRepository

# Initialize FastAPI application with redirect_slashes disabled
# This ensures that routes with trailing slashes are not automatically redirected
# and will return 404 if not explicitly defined
app = FastAPI(
    title="Task Manager API",
    description="A RESTful API for managing tasks",
    version="1.0.0",
    redirect_slashes=False,
)

# Configure CORS middleware to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Initialize task repository (lazy initialization)
_task_repository: TaskRepository | None = None


def get_task_repository() -> TaskRepository:
    """Get or create the task repository instance."""
    global _task_repository
    if _task_repository is None:
        _task_repository = TaskRepository()
    return _task_repository


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    """
    Health check endpoint for monitoring.

    Returns:
        Dictionary with status information
    """
    return {"status": "healthy"}


@app.get("/api/tasks", tags=["Tasks"])
def get_all_tasks() -> dict[str, list[dict]]:
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
    return {"tasks": [task.model_dump() for task in tasks]}


@app.post("/api/tasks", status_code=201, tags=["Tasks"])
def create_task(task_data: TaskCreate) -> dict:
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
    return task.model_dump()


@app.get("/api/tasks/{task_id}", tags=["Tasks"])
def get_task(task_id: str) -> dict:
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
    return task.model_dump()


@app.put("/api/tasks/{task_id}", tags=["Tasks"])
def update_task(task_id: str, task_data: TaskUpdate) -> dict:
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
    return task.model_dump()


@app.delete("/api/tasks/{task_id}", status_code=204, tags=["Tasks"])
def delete_task(task_id: str) -> None:
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
