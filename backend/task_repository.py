"""
Task Repository for file-based persistence.

This module provides a TaskRepository class that handles CRUD operations
for tasks with JSON file-based persistence and in-memory caching.
"""

import json
import os
from typing import List, Optional
from pathlib import Path
from main import Task, TaskCreate, TaskUpdate


class TaskRepository:
    """
    Repository for managing task persistence with file-based storage.
    
    Uses an in-memory cache for performance and writes through to a JSON file
    for persistence. Handles file I/O errors gracefully and ensures data
    directory exists.
    """
    
    def __init__(self, data_file: str = "/app/data/tasks.json"):
        """
        Initialize the task repository.
        
        Args:
            data_file: Path to the JSON file for task storage
        """
        self.data_file = data_file
        self._tasks: dict[str, Task] = {}
        self._ensure_data_directory()
        self._load()
    
    def _ensure_data_directory(self) -> None:
        """
        Ensure the data directory exists.
        Creates the directory if it doesn't exist.
        """
        data_dir = Path(self.data_file).parent
        try:
            data_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"Error creating data directory: {e}")
            raise
    
    def _load(self) -> None:
        """
        Load tasks from the JSON file into memory cache.
        Creates an empty file if it doesn't exist.
        Handles file I/O errors gracefully.
        """
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    # Convert list of dicts to dict of Task objects
                    self._tasks = {
                        task_dict['id']: Task(**task_dict)
                        for task_dict in data
                    }
            else:
                # Initialize empty file
                self._tasks = {}
                self._save()
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {self.data_file}: {e}")
            # Start with empty tasks on corrupt file
            self._tasks = {}
            self._save()
        except Exception as e:
            print(f"Error loading tasks from {self.data_file}: {e}")
            raise
    
    def _save(self) -> None:
        """
        Save tasks from memory cache to the JSON file.
        Handles file I/O errors gracefully.
        """
        try:
            # Convert dict of Task objects to list of dicts
            tasks_list = [task.dict() for task in self._tasks.values()]
            with open(self.data_file, 'w') as f:
                json.dump(tasks_list, f, indent=2)
        except Exception as e:
            print(f"Error saving tasks to {self.data_file}: {e}")
            raise
    
    def get_all(self) -> List[Task]:
        """
        Retrieve all tasks.
        
        Returns:
            List of all tasks, ordered by creation date (newest first)
        """
        tasks = list(self._tasks.values())
        # Sort by created_at descending (newest first)
        tasks.sort(key=lambda t: t.created_at, reverse=True)
        return tasks
    
    def get_by_id(self, task_id: str) -> Optional[Task]:
        """
        Retrieve a single task by ID.
        
        Args:
            task_id: The unique identifier of the task
            
        Returns:
            Task object if found, None otherwise
        """
        return self._tasks.get(task_id)
    
    def create(self, task_data: TaskCreate) -> Task:
        """
        Create a new task and persist it.
        
        Args:
            task_data: TaskCreate object with title and description
            
        Returns:
            The newly created Task object
        """
        task = Task.create_new(task_data)
        self._tasks[task.id] = task
        self._save()
        return task
    
    def update(self, task_id: str, task_data: TaskUpdate) -> Optional[Task]:
        """
        Update an existing task and persist the changes.
        
        Args:
            task_id: The unique identifier of the task to update
            task_data: TaskUpdate object with fields to update
            
        Returns:
            Updated Task object if found, None otherwise
        """
        existing_task = self._tasks.get(task_id)
        if existing_task is None:
            return None
        
        updated_task = existing_task.update_from(task_data)
        self._tasks[task_id] = updated_task
        self._save()
        return updated_task
    
    def delete(self, task_id: str) -> bool:
        """
        Delete a task and persist the change.
        
        Args:
            task_id: The unique identifier of the task to delete
            
        Returns:
            True if task was deleted, False if task was not found
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            self._save()
            return True
        return False
    
    def delete_all(self) -> int:
        """
        Delete all tasks and persist the change.
        
        Returns:
            The number of tasks that were deleted
        """
        count = len(self._tasks)
        self._tasks.clear()
        self._save()
        return count
