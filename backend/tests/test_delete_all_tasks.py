"""
Tests for delete all tasks endpoint.

This test suite verifies the DELETE /api/tasks/all endpoint functionality.
"""

from typing import Generator
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.models.task import Task, TaskCreate


# Mock task storage
mock_tasks = {}


def mock_get_connection():
    """Mock database connection context manager"""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_conn.is_connected.return_value = True
    return mock_conn


def create_mock_repository():
    """Create a mock repository with in-memory storage"""
    from app.repositories.task_repository import TaskRepository

    repo = TaskRepository.__new__(TaskRepository)
    repo.db_config = {}

    # Mock the _get_connection method
    def mock_connection_context():
        from contextlib import contextmanager

        @contextmanager
        def _mock():
            yield mock_get_connection()
        return _mock()

    repo._get_connection = mock_connection_context

    # Override methods to use in-memory storage
    def get_all():
        return sorted(mock_tasks.values(), key=lambda t: t.created_at, reverse=True)

    def get_by_id(task_id: str):
        return mock_tasks.get(task_id)

    def create(task_data: TaskCreate):
        task = Task.create_new(task_data)
        mock_tasks[task.id] = task
        return task

    def update(task_id: str, task_data):
        existing = mock_tasks.get(task_id)
        if not existing:
            return None
        updated = existing.update_from(task_data)
        mock_tasks[task_id] = updated
        return updated

    def delete(task_id: str):
        if task_id in mock_tasks:
            del mock_tasks[task_id]
            return True
        return False

    def delete_all():
        count = len(mock_tasks)
        mock_tasks.clear()
        return count

    repo.get_all = get_all
    repo.get_by_id = get_by_id
    repo.create = create
    repo.update = update
    repo.delete = delete
    repo.delete_all = delete_all

    return repo


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """
    Create a TestClient instance for testing FastAPI endpoints.
    Uses mocked repository for unit tests.
    """
    global mock_tasks
    mock_tasks = {}

    # Create a single mock repository instance to reuse
    mock_repo = create_mock_repository()

    # Create app and override dependency
    from app.dependencies import get_task_repository
    test_app = create_app()
    test_app.dependency_overrides[get_task_repository] = lambda: mock_repo

    test_client = TestClient(test_app)
    yield test_client

    # Cleanup
    test_app.dependency_overrides.clear()
    mock_tasks = {}


class TestDeleteAllTasksEndpoint:
    """Test suite for DELETE /api/tasks/all endpoint"""

    def test_delete_all_tasks_empty_database(self, client: TestClient) -> None:
        """Test deleting all tasks when database is empty"""
        response = client.delete("/api/tasks/all")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["deletedCount"] == 0

    def test_delete_all_tasks_with_single_task(self, client: TestClient) -> None:
        """Test deleting all tasks when one task exists"""
        # Create a task first
        client.post("/api/tasks", json={
            "title": "Test Task",
            "description": "Test Description"
        })

        # Delete all tasks
        response = client.delete("/api/tasks/all")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["deletedCount"] == 1

        # Verify tasks are deleted
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 0

    def test_delete_all_tasks_with_multiple_tasks(self, client: TestClient) -> None:
        """Test deleting all tasks when multiple tasks exist"""
        # Create multiple tasks
        for i in range(5):
            client.post("/api/tasks", json={
                "title": f"Task {i}",
                "description": f"Description {i}"
            })

        # Verify tasks were created
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 5

        # Delete all tasks
        response = client.delete("/api/tasks/all")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["deletedCount"] == 5

        # Verify all tasks are deleted
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 0

    def test_delete_all_tasks_response_structure(self, client: TestClient) -> None:
        """Test that delete all endpoint returns correct response structure"""
        # Create a task
        client.post("/api/tasks", json={
            "title": "Test Task",
            "description": "Test Description"
        })

        # Delete all tasks
        response = client.delete("/api/tasks/all")

        assert response.status_code == 200
        data = response.json()

        # Verify response structure
        assert "success" in data
        assert "deletedCount" in data
        assert isinstance(data["success"], bool)
        assert isinstance(data["deletedCount"], int)
        assert data["success"] is True

    def test_delete_all_tasks_idempotence(self, client: TestClient) -> None:
        """Test that calling delete all multiple times is safe"""
        # Create tasks
        client.post("/api/tasks", json={
            "title": "Test Task 1",
            "description": "Description 1"
        })
        client.post("/api/tasks", json={
            "title": "Test Task 2",
            "description": "Description 2"
        })

        # First delete all
        response1 = client.delete("/api/tasks/all")
        assert response1.status_code == 200
        assert response1.json()["deletedCount"] == 2

        # Second delete all (should delete 0)
        response2 = client.delete("/api/tasks/all")
        assert response2.status_code == 200
        assert response2.json()["deletedCount"] == 0
        assert response2.json()["success"] is True

    def test_delete_all_tasks_after_mixed_operations(self, client: TestClient) -> None:
        """Test delete all after various CRUD operations"""
        # Create tasks
        task1 = client.post("/api/tasks", json={
            "title": "Task 1",
            "description": "Desc 1"
        }).json()

        task2 = client.post("/api/tasks", json={
            "title": "Task 2",
            "description": "Desc 2"
        }).json()

        client.post("/api/tasks", json={
            "title": "Task 3",
            "description": "Desc 3"
        })

        # Update one task
        client.put(f"/api/tasks/{task1['id']}", json={
            "title": "Updated Task 1",
            "completed": True
        })

        # Delete one task
        client.delete(f"/api/tasks/{task2['id']}")

        # Should have 2 tasks remaining
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 2

        # Delete all
        response = client.delete("/api/tasks/all")
        assert response.status_code == 200
        assert response.json()["deletedCount"] == 2

        # Verify all deleted
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 0
