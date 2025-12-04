"""
Dependency injection module for FastAPI.

This module provides dependency functions that FastAPI uses to inject
dependencies into route handlers. This enables loose coupling and
makes components easily testable.
"""

from fastapi import Depends

from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService


def get_task_repository() -> TaskRepository:
    """
    Dependency that provides TaskRepository instance.

    This function is used by FastAPI's dependency injection system
    to provide repository instances to route handlers and services.

    Returns:
        TaskRepository instance configured with database settings
    """
    return TaskRepository()


def get_task_service(
    repository: TaskRepository = Depends(get_task_repository)
) -> TaskService:
    """
    Dependency that provides TaskService instance with injected repository.

    This function is used by FastAPI's dependency injection system
    to provide service instances to route handlers. The repository
    is automatically injected by FastAPI.

    Args:
        repository: TaskRepository instance (injected by FastAPI)

    Returns:
        TaskService instance with repository dependency injected
    """
    return TaskService(repository)
