"""
Unit and integration tests for Delete All Tasks functionality.

This test suite covers:
- Repository layer delete_all() method
- Service layer delete_all_tasks() method
- API endpoint DELETE /api/tasks
- Edge cases (empty database, multiple tasks)
"""

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
def client():
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


class TestDeleteAllTasksRepository:
    """Unit tests for repository layer delete_all method"""

    def test_delete_all_returns_count_of_deleted_tasks(self, client: TestClient):
        """Test that delete_all returns the count of deleted tasks"""
        # Create multiple tasks
        client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})
        client.post("/api/tasks", json={"title": "Task 2", "description": "Desc 2"})
        client.post("/api/tasks", json={"title": "Task 3", "description": "Desc 3"})

        # Verify 3 tasks exist
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 3

        # Delete all tasks
        response = client.delete("/api/tasks")
        assert response.status_code == 204

        # Verify no tasks remain
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0

    def test_delete_all_on_empty_database(self, client: TestClient):
        """Test that delete_all works on empty database"""
        # Verify database is empty
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0

        # Delete all tasks (should succeed even with empty DB)
        response = client.delete("/api/tasks")
        assert response.status_code == 204

        # Verify database is still empty
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0

    def test_delete_all_removes_all_tasks(self, client: TestClient):
        """Test that delete_all removes all tasks regardless of count"""
        # Create 10 tasks
        for i in range(10):
            client.post(
                "/api/tasks",
                json={"title": f"Task {i}", "description": f"Description {i}"}
            )

        # Verify 10 tasks exist
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 10

        # Delete all tasks
        response = client.delete("/api/tasks")
        assert response.status_code == 204

        # Verify all tasks were deleted
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0


class TestDeleteAllTasksEndpoint:
    """Integration tests for DELETE /api/tasks endpoint"""

    def test_delete_all_endpoint_returns_204(self, client: TestClient):
        """Test that DELETE /api/tasks returns 204 No Content"""
        # Create a task
        client.post("/api/tasks", json={"title": "Test Task", "description": "Test"})

        # Delete all tasks
        response = client.delete("/api/tasks")
        assert response.status_code == 204

    def test_delete_all_endpoint_returns_empty_body(self, client: TestClient):
        """Test that DELETE /api/tasks returns empty response body"""
        # Create a task
        client.post("/api/tasks", json={"title": "Test Task", "description": "Test"})

        # Delete all tasks
        response = client.delete("/api/tasks")
        assert response.status_code == 204
        assert response.text == ""

    def test_delete_all_endpoint_different_from_delete_single(self, client: TestClient):
        """Test that DELETE /api/tasks is different from DELETE /api/tasks/{id}"""
        # Create two tasks
        response1 = client.post(
            "/api/tasks",
            json={"title": "Task 1", "description": "Desc 1"}
        )
        task1_id = response1.json()["id"]

        response2 = client.post(
            "/api/tasks",
            json={"title": "Task 2", "description": "Desc 2"}
        )
        task2_id = response2.json()["id"]

        # Delete single task
        response = client.delete(f"/api/tasks/{task1_id}")
        assert response.status_code == 204

        # Verify one task remains
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 1
        assert response.json()["tasks"][0]["id"] == task2_id

        # Delete all remaining tasks
        response = client.delete("/api/tasks")
        assert response.status_code == 204

        # Verify no tasks remain
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0

    def test_delete_all_endpoint_can_be_called_multiple_times(
        self, client: TestClient
    ):
        """Test that DELETE /api/tasks can be called multiple times"""
        # Create tasks
        client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})
        client.post("/api/tasks", json={"title": "Task 2", "description": "Desc 2"})

        # Delete all tasks first time
        response = client.delete("/api/tasks")
        assert response.status_code == 204

        # Delete all tasks second time (empty database)
        response = client.delete("/api/tasks")
        assert response.status_code == 204

        # Create more tasks
        client.post("/api/tasks", json={"title": "Task 3", "description": "Desc 3"})

        # Delete all tasks third time
        response = client.delete("/api/tasks")
        assert response.status_code == 204

        # Verify database is empty
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0


class TestDeleteAllTasksWorkflow:
    """Integration tests for complete delete all workflow"""

    def test_create_and_delete_all_workflow(self, client: TestClient):
        """Test complete workflow: create tasks → verify → delete all → verify"""
        # Create multiple tasks
        tasks_data = [
            {"title": "Buy groceries", "description": "Milk, eggs, bread"},
            {"title": "Write report", "description": "Q4 financial report"},
            {"title": "Call dentist", "description": "Schedule appointment"},
        ]

        for task_data in tasks_data:
            response = client.post("/api/tasks", json=task_data)
            assert response.status_code == 201

        # Verify all tasks were created
        response = client.get("/api/tasks")
        assert response.status_code == 200
        assert len(response.json()["tasks"]) == 3

        # Delete all tasks
        response = client.delete("/api/tasks")
        assert response.status_code == 204

        # Verify all tasks were deleted
        response = client.get("/api/tasks")
        assert response.status_code == 200
        assert len(response.json()["tasks"]) == 0
        assert response.json()["tasks"] == []

    def test_delete_all_does_not_affect_subsequent_creates(
        self, client: TestClient
    ):
        """Test that delete all doesn't affect ability to create new tasks"""
        # Create and delete tasks
        client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})
        client.delete("/api/tasks")

        # Create new task after delete all
        response = client.post(
            "/api/tasks",
            json={"title": "New Task", "description": "After delete"}
        )
        assert response.status_code == 201

        # Verify new task exists
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 1
        assert response.json()["tasks"][0]["title"] == "New Task"

    def test_delete_all_with_mixed_completion_status(self, client: TestClient):
        """Test that delete all removes tasks regardless of completion status"""
        # Create completed and incomplete tasks
        response1 = client.post(
            "/api/tasks",
            json={"title": "Completed Task", "description": "Done"}
        )
        task1_id = response1.json()["id"]
        client.put(f"/api/tasks/{task1_id}", json={"completed": True})

        client.post(
            "/api/tasks",
            json={"title": "Incomplete Task", "description": "Not done"}
        )

        # Verify both tasks exist
        response = client.get("/api/tasks")
        tasks = response.json()["tasks"]
        assert len(tasks) == 2
        assert any(t["completed"] for t in tasks)
        assert any(not t["completed"] for t in tasks)

        # Delete all tasks
        response = client.delete("/api/tasks")
        assert response.status_code == 204

        # Verify all tasks were deleted
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0


class TestDeleteAllTasksEdgeCases:
    """Edge case tests for delete all functionality"""

    def test_delete_all_with_single_task(self, client: TestClient):
        """Test delete all with only one task"""
        client.post("/api/tasks", json={"title": "Single Task", "description": "Only one"})

        response = client.delete("/api/tasks")
        assert response.status_code == 204

        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0

    def test_delete_all_with_very_long_titles_and_descriptions(
        self, client: TestClient
    ):
        """Test delete all with tasks having maximum length fields"""
        long_title = "A" * 200  # Maximum title length
        long_description = "B" * 1000  # Maximum description length

        client.post(
            "/api/tasks",
            json={"title": long_title, "description": long_description}
        )

        response = client.delete("/api/tasks")
        assert response.status_code == 204

        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0

    def test_delete_all_preserves_api_functionality(self, client: TestClient):
        """Test that all API operations work correctly after delete all"""
        # Create and delete tasks
        client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})
        client.delete("/api/tasks")

        # Test GET all tasks
        response = client.get("/api/tasks")
        assert response.status_code == 200

        # Test POST create task
        response = client.post(
            "/api/tasks",
            json={"title": "New Task", "description": "After delete"}
        )
        assert response.status_code == 201
        task_id = response.json()["id"]

        # Test GET single task
        response = client.get(f"/api/tasks/{task_id}")
        assert response.status_code == 200

        # Test PUT update task
        response = client.put(
            f"/api/tasks/{task_id}",
            json={"title": "Updated Task"}
        )
        assert response.status_code == 200

        # Test DELETE single task
        response = client.delete(f"/api/tasks/{task_id}")
        assert response.status_code == 204
