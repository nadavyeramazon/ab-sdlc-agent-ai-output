"""
Task Repository for MySQL-based persistence.

This module provides a TaskRepository class that handles CRUD operations
for tasks with MySQL database persistence.
"""

import os
from contextlib import contextmanager
from typing import List, Optional

import mysql.connector
from mysql.connector import Error

from app.models.task import Task, TaskCreate, TaskUpdate


class TaskRepository:
    """
    Repository for managing task persistence with MySQL database.

    Handles database connections, table initialization, and CRUD operations.
    Uses environment variables for database configuration.
    """

    def __init__(self):
        """
        Initialize the task repository.
        Reads database configuration from environment variables.
        """
        self.db_config = {
            "host": os.getenv("DB_HOST", "localhost"),
            "port": int(os.getenv("DB_PORT", "3306")),
            "user": os.getenv("DB_USER", "taskuser"),
            "password": os.getenv("DB_PASSWORD", "taskpassword"),
            "database": os.getenv("DB_NAME", "taskmanager"),
        }
        self._initialize_database()

    @contextmanager
    def _get_connection(self):
        """
        Context manager for database connections.
        Ensures connections are properly closed after use.

        Yields:
            MySQL connection object
        """
        connection = None
        try:
            connection = mysql.connector.connect(**self.db_config)
            yield connection
        except Error as e:
            print(f"Database connection error: {e}")
            raise
        finally:
            if connection and connection.is_connected():
                connection.close()

    def _initialize_database(self) -> None:
        """
        Initialize the database schema.
        Creates the tasks table if it doesn't exist.
        """
        create_table_query = """
        CREATE TABLE IF NOT EXISTS tasks (
            id VARCHAR(36) PRIMARY KEY,
            title VARCHAR(200) NOT NULL,
            description TEXT,
            completed BOOLEAN DEFAULT FALSE,
            created_at VARCHAR(30) NOT NULL,
            updated_at VARCHAR(30) NOT NULL
        )
        """

        try:
            with self._get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(create_table_query)
                connection.commit()
                cursor.close()
        except Error as e:
            print(f"Error initializing database: {e}")
            raise

    def get_all(self) -> List[Task]:
        """
        Retrieve all tasks.

        Returns:
            List of all tasks, ordered by creation date (newest first)
        """
        query = (
            "SELECT id, title, description, completed, created_at, updated_at "
            "FROM tasks ORDER BY created_at DESC"
        )

        try:
            with self._get_connection() as connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute(query)
                results = cursor.fetchall()
                cursor.close()

                return [Task(**row) for row in results]
        except Error as e:
            print(f"Error retrieving all tasks: {e}")
            raise

    def get_by_id(self, task_id: str) -> Optional[Task]:
        """
        Retrieve a single task by ID.

        Args:
            task_id: The unique identifier of the task

        Returns:
            Task object if found, None otherwise
        """
        query = (
            "SELECT id, title, description, completed, created_at, updated_at "
            "FROM tasks WHERE id = %s"
        )

        try:
            with self._get_connection() as connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute(query, (task_id,))
                result = cursor.fetchone()
                cursor.close()

                if result:
                    return Task(**result)
                return None
        except Error as e:
            print(f"Error retrieving task {task_id}: {e}")
            raise

    def create(self, task_data: TaskCreate) -> Task:
        """
        Create a new task and persist it.

        Args:
            task_data: TaskCreate object with title and description

        Returns:
            The newly created Task object
        """
        task = Task.create_new(task_data)

        query = """
        INSERT INTO tasks (id, title, description, completed, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        try:
            with self._get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(
                    query,
                    (
                        task.id,
                        task.title,
                        task.description,
                        task.completed,
                        task.created_at,
                        task.updated_at,
                    ),
                )
                connection.commit()
                cursor.close()

                return task
        except Error as e:
            print(f"Error creating task: {e}")
            raise

    def update(self, task_id: str, task_data: TaskUpdate) -> Optional[Task]:
        """
        Update an existing task and persist the changes.

        Args:
            task_id: The unique identifier of the task to update
            task_data: TaskUpdate object with fields to update

        Returns:
            Updated Task object if found, None otherwise
        """
        existing_task = self.get_by_id(task_id)
        if existing_task is None:
            return None

        updated_task = existing_task.update_from(task_data)

        query = """
        UPDATE tasks
        SET title = %s, description = %s, completed = %s, updated_at = %s
        WHERE id = %s
        """

        try:
            with self._get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(
                    query,
                    (
                        updated_task.title,
                        updated_task.description,
                        updated_task.completed,
                        updated_task.updated_at,
                        task_id,
                    ),
                )
                connection.commit()
                cursor.close()

                return updated_task
        except Error as e:
            print(f"Error updating task {task_id}: {e}")
            raise

    def delete(self, task_id: str) -> bool:
        """
        Delete a task and persist the change.

        Args:
            task_id: The unique identifier of the task to delete

        Returns:
            True if task was deleted, False if task was not found
        """
        query = "DELETE FROM tasks WHERE id = %s"

        try:
            with self._get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(query, (task_id,))
                rows_affected = cursor.rowcount
                connection.commit()
                cursor.close()

                return rows_affected > 0
        except Error as e:
            print(f"Error deleting task {task_id}: {e}")
            raise

    def delete_all(self) -> None:
        """
        Delete all tasks from the database.
        """
        query = "DELETE FROM tasks"

        try:
            with self._get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(query)
                connection.commit()
                cursor.close()
        except Error as e:
            print(f"Error deleting all tasks: {e}")
            raise
