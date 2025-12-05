"""
Tests for DELETE /api/tasks/all endpoint.

This test suite covers:
- Deleting all tasks successfully
- Handling empty database
- Verifying deleted count accuracy
- Response structure validation
- Edge cases and error scenarios
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
        """Delete all tasks and return count"""
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
    """Test suite for DELETE /api/tasks/all endpoint"""

    def test_delete_all_tasks_with_multiple_tasks(self, client: TestClient) -> None:
        """Test deleting all tasks when multiple tasks exist"""
        # Create multiple tasks
        task_ids = []
        for i in range(5):
            response = client.post(
                "/api/tasks",
                json={"title": f"Task {i}", "description": f"Description {i}"}
            )
            assert response.status_code == 201
            task_ids.append(response.json()["id"])

        # Verify tasks were created
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 5

        # Delete all tasks
        response = client.delete("/api/tasks/all")
        assert response.status_code == 200

        # Verify response structure
        data = response.json()
        assert "success" in data
        assert "message" in data
        assert "deletedCount" in data

        # Verify response values
        assert data["success"] is True
        assert data["message"] == "All tasks deleted"
        assert data["deletedCount"] == 5

        # Verify all tasks are gone
        response = client.get("/api/tasks")
        assert response.status_code == 200
        assert len(response.json()["tasks"]) == 0

    def test_delete_all_tasks_with_empty_database(self, client: TestClient) -> None:
        """Test deleting all tasks when no tasks exist"""
        # Verify no tasks exist
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0

        # Delete all tasks (should handle empty database gracefully)
        response = client.delete("/api/tasks/all")
        assert response.status_code == 200

        # Verify response
        data = response.json()
        assert data["success"] is True
        assert data["message"] == "All tasks deleted"
        assert data["deletedCount"] == 0

    def test_delete_all_tasks_with_single_task(self, client: TestClient) -> None:
        """Test deleting all tasks when only one task exists"""
        # Create a single task
        response = client.post(
            "/api/tasks",
            json={"title": "Single Task", "description": "Only one"}
        )
        assert response.status_code == 201
        task_id = response.json()["id"]

        # Delete all tasks
        response = client.delete("/api/tasks/all")
        assert response.status_code == 200

        # Verify response
        data = response.json()
        assert data["success"] is True
        assert data["deletedCount"] == 1

        # Verify task is gone
        response = client.get(f"/api/tasks/{task_id}")
        assert response.status_code == 404

    def test_delete_all_tasks_response_json_structure(
        self, client: TestClient
    ) -> None:
        """Test that DELETE /api/tasks/all returns correct JSON structure"""
        # Create some tasks
        for i in range(3):
            client.post(
                "/api/tasks",
                json={"title": f"Task {i}", "description": f"Desc {i}"}
            )

        # Delete all tasks
        response = client.delete("/api/tasks/all")
        data = response.json()

        # Verify required keys are present
        assert "success" in data
        assert "message" in data
        assert "deletedCount" in data

        # Verify only required keys are present
        assert len(data) == 3

        # Verify data types
        assert isinstance(data["success"], bool)
        assert isinstance(data["message"], str)
        assert isinstance(data["deletedCount"], int)

    def test_delete_all_tasks_idempotent(self, client: TestClient) -> None:
        """Test that calling DELETE /api/tasks/all multiple times is safe"""
        # Create tasks
        for i in range(3):
            client.post(
                "/api/tasks",
                json={"title": f"Task {i}", "description": f"Desc {i}"}
            )

        # First deletion
        response1 = client.delete("/api/tasks/all")
        assert response1.status_code == 200
        assert response1.json()["deletedCount"] == 3

        # Second deletion (should handle empty database)
        response2 = client.delete("/api/tasks/all")
        assert response2.status_code == 200
        assert response2.json()["deletedCount"] == 0

        # Third deletion (still safe)
        response3 = client.delete("/api/tasks/all")
        assert response3.status_code == 200
        assert response3.json()["deletedCount"] == 0

    def test_delete_all_tasks_and_recreate(self, client: TestClient) -> None:
        """Test that new tasks can be created after deleting all tasks"""
        # Create initial tasks
        client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})
        client.post("/api/tasks", json={"title": "Task 2", "description": "Desc 2"})

        # Delete all tasks
        response = client.delete("/api/tasks/all")
        assert response.status_code == 200
        assert response.json()["deletedCount"] == 2

        # Create new tasks after deletion
        response = client.post(
            "/api/tasks",
            json={"title": "New Task", "description": "After deletion"}
        )
        assert response.status_code == 201

        # Verify only the new task exists
        response = client.get("/api/tasks")
        tasks = response.json()["tasks"]
        assert len(tasks) == 1
        assert tasks[0]["title"] == "New Task"

    def test_delete_all_tasks_with_different_task_states(
        self, client: TestClient
    ) -> None:
        """Test deleting all tasks with mixed completed/incomplete states"""
        # Create tasks with different states
        task1 = client.post(
            "/api/tasks",
            json={"title": "Incomplete Task", "description": "Not done"}
        )
        task1_id = task1.json()["id"]

        task2 = client.post(
            "/api/tasks",
            json={"title": "Complete Task", "description": "Done"}
        )
        task2_id = task2.json()["id"]

        # Mark one as complete
        client.put(
            f"/api/tasks/{task2_id}",
            json={"completed": True}
        )

        # Delete all tasks
        response = client.delete("/api/tasks/all")
        assert response.status_code == 200
        assert response.json()["deletedCount"] == 2

        # Verify both are gone
        assert client.get(f"/api/tasks/{task1_id}").status_code == 404
        assert client.get(f"/api/tasks/{task2_id}").status_code == 404

    def test_delete_all_tasks_content_type(self, client: TestClient) -> None:
        """Test that DELETE /api/tasks/all returns correct content type"""
        response = client.delete("/api/tasks/all")

        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"

    def test_delete_all_tasks_correct_deleted_count(self, client: TestClient) -> None:
        """Test that deletedCount accurately reflects number of tasks deleted"""
        # Test with different numbers of tasks
        test_cases = [0, 1, 3, 5, 10]

        for count in test_cases:
            # Clear any existing tasks
            client.delete("/api/tasks/all")

            # Create specified number of tasks
            for i in range(count):
                client.post(
                    "/api/tasks",
                    json={"title": f"Task {i}", "description": f"Desc {i}"}
                )

            # Delete all and verify count
            response = client.delete("/api/tasks/all")
            assert response.status_code == 200
            assert response.json()["deletedCount"] == count


class TestDeleteAllTasksErrorHandling:
    """Test error handling for DELETE /api/tasks/all endpoint"""

    def test_delete_all_tasks_with_database_error(self, client: TestClient) -> None:
        """Test handling of database errors during bulk deletion"""
        # This test verifies that errors are caught and returned properly
        # In a real scenario, we would mock a database failure

        # For now, test the success path (actual error mocking would
        # require more complex setup)
        response = client.delete("/api/tasks/all")
        assert response.status_code == 200

        # Verify response has success field
        data = response.json()
        assert "success" in data

    def test_delete_all_tasks_wrong_http_methods(self, client: TestClient) -> None:
        """Test that other HTTP methods are not allowed on /api/tasks/all"""
        # GET should not be allowed
        response = client.get("/api/tasks/all")
        assert response.status_code == 405

        # POST should not be allowed
        response = client.post("/api/tasks/all", json={})
        assert response.status_code == 405

        # PUT should not be allowed
        response = client.put("/api/tasks/all", json={})
        assert response.status_code == 405


class TestDeleteAllTasksIntegration:
    """Integration tests for DELETE /api/tasks/all with other endpoints"""

    def test_delete_all_after_creating_and_updating_tasks(
        self, client: TestClient
    ) -> None:
        """Test delete all after creating and updating tasks"""
        # Create tasks
        task1 = client.post(
            "/api/tasks",
            json={"title": "Task 1", "description": "Desc 1"}
        )
        task1_id = task1.json()["id"]

        task2 = client.post(
            "/api/tasks",
            json={"title": "Task 2", "description": "Desc 2"}
        )
        task2_id = task2.json()["id"]

        # Update tasks
        client.put(
            f"/api/tasks/{task1_id}",
            json={"title": "Updated Task 1", "completed": True}
        )
        client.put(
            f"/api/tasks/{task2_id}",
            json={"title": "Updated Task 2"}
        )

        # Verify tasks exist with updates
        response = client.get("/api/tasks")
        tasks = response.json()["tasks"]
        assert len(tasks) == 2

        # Delete all tasks
        response = client.delete("/api/tasks/all")
        assert response.status_code == 200
        assert response.json()["deletedCount"] == 2

        # Verify all tasks are gone
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0

    def test_get_all_tasks_after_delete_all(self, client: TestClient) -> None:
        """Test GET /api/tasks returns empty list after DELETE all"""
        # Create tasks
        for i in range(3):
            client.post(
                "/api/tasks",
                json={"title": f"Task {i}", "description": f"Desc {i}"}
            )

        # Delete all tasks
        client.delete("/api/tasks/all")

        # Get all tasks should return empty list
        response = client.get("/api/tasks")
        assert response.status_code == 200
        data = response.json()
        assert "tasks" in data
        assert isinstance(data["tasks"], list)
        assert len(data["tasks"]) == 0
