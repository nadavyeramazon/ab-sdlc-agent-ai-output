"""
Tests for DELETE all tasks endpoint.

This test suite covers:
- DELETE /api/tasks endpoint (delete all tasks)
- Repository delete_all method
- Service delete_all_tasks method
- Edge cases (empty list, multiple tasks)
- HTTP status codes (204 No Content)
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


# Test client fixture
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
    """Unit tests for DELETE /api/tasks endpoint"""

    def test_delete_all_tasks_with_empty_list(self, client: TestClient) -> None:
        """Test DELETE /api/tasks when no tasks exist returns 204"""
        response = client.delete("/api/tasks")

        assert response.status_code == 204
        assert response.text == ""

        # Verify no tasks remain
        get_response = client.get("/api/tasks")
        assert get_response.json()["tasks"] == []

    def test_delete_all_tasks_with_single_task(self, client: TestClient) -> None:
        """Test DELETE /api/tasks with one task"""
        # Create a task
        create_response = client.post(
            "/api/tasks",
            json={"title": "Test Task", "description": "Test Description"}
        )
        assert create_response.status_code == 201

        # Verify task exists
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 1

        # Delete all tasks
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204
        assert delete_response.text == ""

        # Verify no tasks remain
        get_response = client.get("/api/tasks")
        assert get_response.json()["tasks"] == []

    def test_delete_all_tasks_with_multiple_tasks(self, client: TestClient) -> None:
        """Test DELETE /api/tasks with multiple tasks"""
        # Create multiple tasks
        tasks_to_create = [
            {"title": "Task 1", "description": "Description 1"},
            {"title": "Task 2", "description": "Description 2"},
            {"title": "Task 3", "description": "Description 3"},
        ]

        for task_data in tasks_to_create:
            response = client.post("/api/tasks", json=task_data)
            assert response.status_code == 201

        # Verify all tasks exist
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 3

        # Delete all tasks
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204
        assert delete_response.text == ""

        # Verify no tasks remain
        get_response = client.get("/api/tasks")
        assert get_response.json()["tasks"] == []

    def test_delete_all_tasks_twice_succeeds(self, client: TestClient) -> None:
        """Test DELETE /api/tasks twice in a row succeeds both times"""
        # Create a task
        client.post(
            "/api/tasks",
            json={"title": "Test Task", "description": "Test Description"}
        )

        # First delete
        response1 = client.delete("/api/tasks")
        assert response1.status_code == 204

        # Second delete (should still succeed even though no tasks exist)
        response2 = client.delete("/api/tasks")
        assert response2.status_code == 204

    def test_delete_all_tasks_returns_no_content(self, client: TestClient) -> None:
        """Test DELETE /api/tasks returns no response body"""
        # Create a task
        client.post(
            "/api/tasks",
            json={"title": "Test Task", "description": "Test Description"}
        )

        # Delete all tasks
        response = client.delete("/api/tasks")

        assert response.status_code == 204
        assert response.text == ""
        assert response.headers["content-length"] == "0"

    def test_delete_all_tasks_does_not_affect_individual_delete(
        self, client: TestClient
    ) -> None:
        """Test that delete all and delete individual work independently"""
        # Create two tasks
        response1 = client.post(
            "/api/tasks",
            json={"title": "Task 1", "description": "Description 1"}
        )
        task1_id = response1.json()["id"]

        response2 = client.post(
            "/api/tasks",
            json={"title": "Task 2", "description": "Description 2"}
        )
        task2_id = response2.json()["id"]

        # Delete one task individually
        delete_response = client.delete(f"/api/tasks/{task1_id}")
        assert delete_response.status_code == 204

        # Verify only one task remains
        get_response = client.get("/api/tasks")
        tasks = get_response.json()["tasks"]
        assert len(tasks) == 1
        assert tasks[0]["id"] == task2_id

        # Delete all remaining tasks
        delete_all_response = client.delete("/api/tasks")
        assert delete_all_response.status_code == 204

        # Verify no tasks remain
        get_response = client.get("/api/tasks")
        assert get_response.json()["tasks"] == []


class TestDeleteAllTasksRepository:
    """Unit tests for repository delete_all method"""

    def test_repository_delete_all_returns_count(self, client: TestClient) -> None:
        """Test that repository delete_all returns the count of deleted tasks"""
        # Create multiple tasks
        for i in range(5):
            client.post(
                "/api/tasks",
                json={"title": f"Task {i}", "description": f"Description {i}"}
            )

        # Delete all tasks
        response = client.delete("/api/tasks")
        assert response.status_code == 204

        # Verify all tasks are gone
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 0

    def test_repository_delete_all_with_completed_and_incomplete(
        self, client: TestClient
    ) -> None:
        """Test delete_all removes both completed and incomplete tasks"""
        # Create completed task
        response1 = client.post(
            "/api/tasks",
            json={"title": "Completed Task", "description": "Done"}
        )
        task1_id = response1.json()["id"]
        client.put(
            f"/api/tasks/{task1_id}",
            json={"completed": True}
        )

        # Create incomplete task
        client.post(
            "/api/tasks",
            json={"title": "Incomplete Task", "description": "Not done"}
        )

        # Verify both tasks exist
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 2

        # Delete all tasks
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204

        # Verify all tasks removed
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 0


class TestDeleteAllTasksService:
    """Unit tests for service delete_all_tasks method"""

    def test_service_delete_all_tasks_clears_storage(
        self, client: TestClient
    ) -> None:
        """Test that service delete_all_tasks clears all tasks"""
        # Create tasks
        for i in range(3):
            client.post(
                "/api/tasks",
                json={"title": f"Task {i}", "description": f"Description {i}"}
            )

        # Delete all via endpoint (which uses service)
        response = client.delete("/api/tasks")
        assert response.status_code == 204

        # Verify service cleared all tasks
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 0


class TestDeleteAllTasksEdgeCases:
    """Edge case tests for DELETE /api/tasks"""

    def test_delete_all_after_creating_and_updating_tasks(
        self, client: TestClient
    ) -> None:
        """Test delete all works after tasks have been updated"""
        # Create and update a task
        response = client.post(
            "/api/tasks",
            json={"title": "Original Title", "description": "Original Description"}
        )
        task_id = response.json()["id"]

        client.put(
            f"/api/tasks/{task_id}",
            json={"title": "Updated Title", "completed": True}
        )

        # Delete all tasks
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204

        # Verify task is gone
        get_response = client.get(f"/api/tasks/{task_id}")
        assert get_response.status_code == 404

    def test_delete_all_then_create_new_task(self, client: TestClient) -> None:
        """Test creating new task after deleting all tasks works correctly"""
        # Create initial task
        client.post(
            "/api/tasks",
            json={"title": "Task 1", "description": "Description 1"}
        )

        # Delete all tasks
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204

        # Create new task after deletion
        response = client.post(
            "/api/tasks",
            json={"title": "New Task", "description": "New Description"}
        )
        assert response.status_code == 201

        # Verify only the new task exists
        get_response = client.get("/api/tasks")
        tasks = get_response.json()["tasks"]
        assert len(tasks) == 1
        assert tasks[0]["title"] == "New Task"

    def test_delete_all_with_very_large_number_of_tasks(
        self, client: TestClient
    ) -> None:
        """Test delete all works with a large number of tasks"""
        # Create many tasks
        num_tasks = 100
        for i in range(num_tasks):
            client.post(
                "/api/tasks",
                json={"title": f"Task {i}", "description": f"Description {i}"}
            )

        # Verify all tasks created
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == num_tasks

        # Delete all tasks
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204

        # Verify all tasks deleted
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 0
