"""
Task Service for business logic layer.

This module provides a TaskService class that orchestrates task operations
between the route layer and repository layer.
"""

from typing import List, Optional

from app.models.task import Task, TaskCreate, TaskUpdate
from app.repositories.task_repository import TaskRepository


class TaskService:
    """
    Service layer for task operations.

    Handles business logic and orchestrates operations between routes and repositories.
    Uses dependency injection to receive repository instances.
    """

    def __init__(self, repository: TaskRepository):
        """
        Initialize the task service with a repository.

        Args:
            repository: TaskRepository instance for data persistence
        """
        self.repository = repository

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks.

        Returns:
            List of all tasks
        """
        return self.repository.get_all()

    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """
        Retrieve a task by ID.

        Args:
            task_id: The unique identifier of the task

        Returns:
            Task object if found, None otherwise
        """
        return self.repository.get_by_id(task_id)

    def create_task(self, task_data: TaskCreate) -> Task:
        """
        Create a new task.

        Args:
            task_data: TaskCreate object with title and description

        Returns:
            The newly created Task object
        """
        return self.repository.create(task_data)

    def update_task(self, task_id: str, task_data: TaskUpdate) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: The unique identifier of the task to update
            task_data: TaskUpdate object with fields to update

        Returns:
            Updated Task object if found, None otherwise
        """
        return self.repository.update(task_id, task_data)

    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task.

        Args:
            task_id: The unique identifier of the task to delete

        Returns:
            True if task was deleted, False if task was not found
        """
        return self.repository.delete(task_id)

    def delete_all_tasks(self) -> None:
        """
        Delete all tasks.
        """
        self.repository.delete_all()
