"""
Task management route module.

This module provides RESTful API endpoints for task CRUD operations.
"""

from fastapi import APIRouter, HTTPException, Depends

from app.models.task import TaskCreate, TaskUpdate
from app.services.task_service import TaskService
from app.dependencies import get_task_service

router = APIRouter(tags=["Tasks"])


@router.get("/tasks")
def get_all_tasks(
    service: TaskService = Depends(get_task_service)
) -> dict[str, list[dict]]:
    """
    Retrieve all tasks.

    Args:
        service: Injected TaskService instance

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
    tasks = service.get_all_tasks()
    return {"tasks": [task.model_dump() for task in tasks]}


@router.post("/tasks", status_code=201)
def create_task(
    task_data: TaskCreate,
    service: TaskService = Depends(get_task_service)
) -> dict:
    """
    Create a new task.

    Args:
        task_data: TaskCreate object with title and description
        service: Injected TaskService instance

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
    task = service.create_task(task_data)
    return task.model_dump()


@router.get("/tasks/{task_id}")
def get_task(
    task_id: str,
    service: TaskService = Depends(get_task_service)
) -> dict:
    """
    Retrieve a single task by ID.

    Args:
        task_id: The unique identifier of the task
        service: Injected TaskService instance

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
    task = service.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task.model_dump()


@router.put("/tasks/{task_id}")
def update_task(
    task_id: str,
    task_data: TaskUpdate,
    service: TaskService = Depends(get_task_service)
) -> dict:
    """
    Update an existing task.

    Args:
        task_id: The unique identifier of the task to update
        task_data: TaskUpdate object with fields to update
        service: Injected TaskService instance

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
    task = service.update_task(task_id, task_data)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task.model_dump()


@router.delete("/tasks/{task_id}", status_code=204)
def delete_task(
    task_id: str,
    service: TaskService = Depends(get_task_service)
) -> None:
    """
    Delete a task.

    Args:
        task_id: The unique identifier of the task to delete
        service: Injected TaskService instance

    Returns:
        No content (204 status)

    Raises:
        HTTPException 404: If task with given ID is not found

    Example:
        Response: No content with 204 status code
    """
    success = service.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return None


@router.delete("/tasks", status_code=204)
def delete_all_tasks(
    service: TaskService = Depends(get_task_service)
) -> None:
    """
    Delete all tasks.

    Args:
        service: Injected TaskService instance

    Returns:
        No content (204 status)

    Raises:
        HTTPException 500: If deletion fails

    Example:
        Response: No content with 204 status code
    """
    try:
        service.delete_all_tasks()
        return None
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to delete tasks")
