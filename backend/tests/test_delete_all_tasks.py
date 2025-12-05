"""
Tests for DELETE /api/tasks/all endpoint.

This test suite covers:
- Successful deletion of all tasks
- Response format validation
- Error handling scenarios
- Edge cases (empty task list)
"""

from typing import Generator
from unittest.mock import MagicMock, patch

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

    def test_delete_all_tasks_success_with_tasks(self, client: TestClient) -> None:
        """Test successful deletion when tasks exist"""
        # Create multiple tasks
        client.post("/api/tasks", json={"title": "Task 1", "description": "Description 1"})
        client.post("/api/tasks", json={"title": "Task 2", "description": "Description 2"})
        client.post("/api/tasks", json={"title": "Task 3", "description": "Description 3"})

        # Verify tasks exist
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 3

        # Delete all tasks
        response = client.delete("/api/tasks/all")

        # Verify response
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["message"] == "All tasks deleted successfully"
        assert data["deletedCount"] == 3

        # Verify all tasks are deleted
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0

    def test_delete_all_tasks_success_empty_list(self, client: TestClient) -> None:
        """Test successful deletion when no tasks exist"""
        # Ensure no tasks exist
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0

        # Delete all tasks
        response = client.delete("/api/tasks/all")

        # Verify response
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["message"] == "All tasks deleted successfully"
        assert data["deletedCount"] == 0

    def test_delete_all_tasks_response_structure(self, client: TestClient) -> None:
        """Test that response has correct structure"""
        # Create a task
        client.post("/api/tasks", json={"title": "Test Task", "description": "Test"})

        response = client.delete("/api/tasks/all")

        assert response.status_code == 200
        data = response.json()

        # Verify all required fields are present
        assert "success" in data
        assert "message" in data
        assert "deletedCount" in data

        # Verify data types
        assert isinstance(data["success"], bool)
        assert isinstance(data["message"], str)
        assert isinstance(data["deletedCount"], int)

        # Verify values
        assert data["success"] is True
        assert data["deletedCount"] >= 0

    def test_delete_all_tasks_multiple_calls(self, client: TestClient) -> None:
        """Test multiple consecutive calls to delete all tasks"""
        # Create tasks
        client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})
        client.post("/api/tasks", json={"title": "Task 2", "description": "Desc 2"})

        # First delete
        response1 = client.delete("/api/tasks/all")
        assert response1.status_code == 200
        assert response1.json()["deletedCount"] == 2

        # Second delete (should delete 0 tasks)
        response2 = client.delete("/api/tasks/all")
        assert response2.status_code == 200
        assert response2.json()["deletedCount"] == 0

        # Verify no tasks exist
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0

    def test_delete_all_tasks_large_number(self, client: TestClient) -> None:
        """Test deletion with larger number of tasks"""
        # Create 10 tasks
        for i in range(10):
            client.post(
                "/api/tasks",
                json={"title": f"Task {i}", "description": f"Description {i}"}
            )

        # Verify tasks created
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 10

        # Delete all
        response = client.delete("/api/tasks/all")
        assert response.status_code == 200
        assert response.json()["deletedCount"] == 10

        # Verify all deleted
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0

    def test_delete_all_tasks_content_type(self, client: TestClient) -> None:
        """Test that response has correct content type"""
        response = client.delete("/api/tasks/all")

        assert response.status_code == 200
        assert "application/json" in response.headers["content-type"]


class TestDeleteAllTasksErrorHandling:
    """Test suite for error handling in DELETE /api/tasks/all endpoint"""

    def test_delete_all_tasks_database_error(self, client: TestClient) -> None:
        """Test error handling when database operation fails"""
        # Override the repository to raise an exception
        from app.dependencies import get_task_repository
        from app.repositories.task_repository import TaskRepository

        def failing_repo():
            repo = TaskRepository.__new__(TaskRepository)

            def delete_all():
                raise Exception("Database connection failed")

            repo.delete_all = delete_all
            return repo

        # Override dependency
        test_app = create_app()
        test_app.dependency_overrides[get_task_repository] = failing_repo

        test_client = TestClient(test_app)

        # Attempt to delete all tasks
        response = test_client.delete("/api/tasks/all")

        # Verify error response
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
        assert data["detail"]["success"] is False
        assert data["detail"]["message"] == "Error deleting tasks"
        assert "error" in data["detail"]

    def test_delete_all_tasks_wrong_http_method(self, client: TestClient) -> None:
        """Test that only DELETE method is allowed"""
        # Test GET method
        response = client.get("/api/tasks/all")
        assert response.status_code == 405

        # Test POST method
        response = client.post("/api/tasks/all")
        assert response.status_code == 405

        # Test PUT method
        response = client.put("/api/tasks/all")
        assert response.status_code == 405


class TestDeleteAllTasksIntegration:
    """Integration tests for DELETE /api/tasks/all endpoint"""

    def test_delete_all_after_various_operations(self, client: TestClient) -> None:
        """Test delete all after various CRUD operations"""
        # Create tasks
        task1 = client.post(
            "/api/tasks",
            json={"title": "Task 1", "description": "Description 1"}
        ).json()
        task2 = client.post(
            "/api/tasks",
            json={"title": "Task 2", "description": "Description 2"}
        ).json()
        task3 = client.post(
            "/api/tasks",
            json={"title": "Task 3", "description": "Description 3"}
        ).json()

        # Update a task
        client.put(
            f"/api/tasks/{task1['id']}",
            json={"title": "Updated Task 1", "completed": True}
        )

        # Delete one task
        client.delete(f"/api/tasks/{task2['id']}")

        # Verify 2 tasks remain
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 2

        # Delete all remaining tasks
        response = client.delete("/api/tasks/all")
        assert response.status_code == 200
        assert response.json()["deletedCount"] == 2

        # Verify all tasks deleted
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0

    def test_create_after_delete_all(self, client: TestClient) -> None:
        """Test creating tasks after deleting all"""
        # Create tasks
        client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})
        client.post("/api/tasks", json={"title": "Task 2", "description": "Desc 2"})

        # Delete all
        client.delete("/api/tasks/all")

        # Create new tasks after delete all
        response = client.post(
            "/api/tasks",
            json={"title": "New Task", "description": "New Description"}
        )
        assert response.status_code == 201

        # Verify only one task exists
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 1
        assert response.json()["tasks"][0]["title"] == "New Task"
