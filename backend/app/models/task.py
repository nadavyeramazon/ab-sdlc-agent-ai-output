"""
Task data models for the Task Manager application.

This module contains Pydantic models for task-related operations including
request validation, response serialization, and data representation.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, field_validator


class TaskCreate(BaseModel):
    """Request model for creating a new task."""

    title: str
    description: str = ""

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
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
            raise ValueError("Title cannot be empty")
        if len(v.strip()) > 200:
            raise ValueError("Title cannot exceed 200 characters")
        return v.strip()

    @field_validator("description")
    @classmethod
    def description_length(cls, v: str) -> str:
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
            raise ValueError("Description cannot exceed 1000 characters")
        return v


class TaskUpdate(BaseModel):
    """Request model for updating an existing task."""

    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: Optional[str]) -> Optional[str]:
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
                raise ValueError("Title cannot be empty")
            if len(v.strip()) > 200:
                raise ValueError("Title cannot exceed 200 characters")
            return v.strip()
        return v

    @field_validator("description")
    @classmethod
    def description_length(cls, v: Optional[str]) -> Optional[str]:
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
            raise ValueError("Description cannot exceed 1000 characters")
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
        now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        return cls(
            id=str(uuid.uuid4()),
            title=task_data.title,
            description=task_data.description,
            completed=False,
            created_at=now,
            updated_at=now,
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
            updated_fields["title"] = update_data.title
        if update_data.description is not None:
            updated_fields["description"] = update_data.description
        if update_data.completed is not None:
            updated_fields["completed"] = update_data.completed

        updated_fields["updated_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

        return self.model_copy(update=updated_fields)
