"""
Tests for delete all tasks functionality.

This test suite covers the delete all tasks endpoint across all layers:
- Repository layer: delete_all() method
- Service layer: delete_all_tasks() method
- API layer: DELETE /api/tasks endpoint
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


class TestDeleteAllTasksRepository:
    """Unit tests for TaskRepository.delete_all() method"""

    def test_delete_all_with_empty_database(self, client: TestClient) -> None:
        """Test that delete_all returns 0 when database is empty"""
        global mock_tasks
        mock_tasks = {}

        mock_repo = create_mock_repository()
        count = mock_repo.delete_all()

        assert count == 0
        assert len(mock_tasks) == 0

    def test_delete_all_with_single_task(self, client: TestClient) -> None:
        """Test that delete_all removes single task and returns 1"""
        global mock_tasks
        mock_tasks = {}

        mock_repo = create_mock_repository()
        mock_repo.create(TaskCreate(title="Task 1", description="Description 1"))

        assert len(mock_tasks) == 1

        count = mock_repo.delete_all()

        assert count == 1
        assert len(mock_tasks) == 0

    def test_delete_all_with_multiple_tasks(self, client: TestClient) -> None:
        """Test that delete_all removes all tasks and returns correct count"""
        global mock_tasks
        mock_tasks = {}

        mock_repo = create_mock_repository()
        mock_repo.create(TaskCreate(title="Task 1", description="Description 1"))
        mock_repo.create(TaskCreate(title="Task 2", description="Description 2"))
        mock_repo.create(TaskCreate(title="Task 3", description="Description 3"))

        assert len(mock_tasks) == 3

        count = mock_repo.delete_all()

        assert count == 3
        assert len(mock_tasks) == 0

    def test_delete_all_clears_all_tasks(self, client: TestClient) -> None:
        """Test that delete_all truly clears all tasks from storage"""
        global mock_tasks
        mock_tasks = {}

        mock_repo = create_mock_repository()
        task1 = mock_repo.create(TaskCreate(title="Task 1", description="Desc 1"))
        task2 = mock_repo.create(TaskCreate(title="Task 2", description="Desc 2"))

        # Verify tasks exist
        assert mock_repo.get_by_id(task1.id) is not None
        assert mock_repo.get_by_id(task2.id) is not None
        assert len(mock_repo.get_all()) == 2

        # Delete all
        mock_repo.delete_all()

        # Verify tasks are gone
        assert mock_repo.get_by_id(task1.id) is None
        assert mock_repo.get_by_id(task2.id) is None
        assert len(mock_repo.get_all()) == 0


class TestDeleteAllTasksService:
    """Unit tests for TaskService.delete_all_tasks() method"""

    def test_delete_all_tasks_calls_repository(self, client: TestClient) -> None:
        """Test that service method calls repository.delete_all()"""
        from app.services.task_service import TaskService

        mock_repo = create_mock_repository()
        service = TaskService(mock_repo)

        # Create some tasks
        mock_repo.create(TaskCreate(title="Task 1", description="Desc 1"))
        mock_repo.create(TaskCreate(title="Task 2", description="Desc 2"))

        count = service.delete_all_tasks()

        assert count == 2
        assert len(mock_repo.get_all()) == 0

    def test_delete_all_tasks_returns_count(self, client: TestClient) -> None:
        """Test that service returns correct count of deleted tasks"""
        from app.services.task_service import TaskService

        mock_repo = create_mock_repository()
        service = TaskService(mock_repo)

        # Test with 0 tasks
        count = service.delete_all_tasks()
        assert count == 0

        # Test with 5 tasks
        for i in range(5):
            mock_repo.create(TaskCreate(title=f"Task {i}", description=f"Desc {i}"))

        count = service.delete_all_tasks()
        assert count == 5


class TestDeleteAllTasksAPI:
    """Integration tests for DELETE /api/tasks endpoint"""

    def test_delete_all_tasks_returns_204(self, client: TestClient) -> None:
        """Test that DELETE /api/tasks returns 204 No Content"""
        response = client.delete("/api/tasks")

        assert response.status_code == 204
        assert response.text == ""

    def test_delete_all_tasks_with_empty_database(self, client: TestClient) -> None:
        """Test DELETE /api/tasks with empty database returns 204"""
        response = client.delete("/api/tasks")

        assert response.status_code == 204

        # Verify database is still empty
        get_response = client.get("/api/tasks")
        assert get_response.json()["tasks"] == []

    def test_delete_all_tasks_removes_all_tasks(self, client: TestClient) -> None:
        """Test that DELETE /api/tasks removes all tasks from database"""
        # Create multiple tasks
        client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})
        client.post("/api/tasks", json={"title": "Task 2", "description": "Desc 2"})
        client.post("/api/tasks", json={"title": "Task 3", "description": "Desc 3"})

        # Verify tasks exist
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 3

        # Delete all tasks
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204

        # Verify all tasks are gone
        get_response = client.get("/api/tasks")
        assert get_response.json()["tasks"] == []

    def test_delete_all_tasks_idempotent(self, client: TestClient) -> None:
        """Test that DELETE /api/tasks can be called multiple times safely"""
        # Create some tasks
        client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})
        client.post("/api/tasks", json={"title": "Task 2", "description": "Desc 2"})

        # Delete all tasks multiple times
        response1 = client.delete("/api/tasks")
        assert response1.status_code == 204

        response2 = client.delete("/api/tasks")
        assert response2.status_code == 204

        response3 = client.delete("/api/tasks")
        assert response3.status_code == 204

        # Verify database is empty
        get_response = client.get("/api/tasks")
        assert get_response.json()["tasks"] == []

    def test_delete_all_tasks_and_create_new(self, client: TestClient) -> None:
        """Test that new tasks can be created after deleting all"""
        # Create and delete tasks
        client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})
        client.delete("/api/tasks")

        # Create new tasks
        response = client.post(
            "/api/tasks",
            json={"title": "New Task", "description": "New Description"}
        )
        assert response.status_code == 201

        # Verify new task exists
        get_response = client.get("/api/tasks")
        tasks = get_response.json()["tasks"]
        assert len(tasks) == 1
        assert tasks[0]["title"] == "New Task"

    def test_delete_all_tasks_no_request_body_required(self, client: TestClient) -> None:
        """Test that DELETE /api/tasks works without request body"""
        response = client.delete("/api/tasks")
        assert response.status_code == 204

    def test_delete_all_tasks_integration_flow(self, client: TestClient) -> None:
        """Test complete workflow: create, read, delete all, verify"""
        # Create tasks
        task_ids = []
        for i in range(5):
            response = client.post(
                "/api/tasks",
                json={"title": f"Task {i}", "description": f"Description {i}"}
            )
            assert response.status_code == 201
            task_ids.append(response.json()["id"])

        # Read all tasks
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 5

        # Delete all tasks
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204

        # Verify all tasks are gone
        get_response = client.get("/api/tasks")
        assert get_response.json()["tasks"] == []

        # Verify individual task lookups return 404
        for task_id in task_ids:
            response = client.get(f"/api/tasks/{task_id}")
            assert response.status_code == 404


class TestDeleteAllTasksEdgeCases:
    """Edge case tests for delete all tasks functionality"""

    def test_delete_all_with_mixed_completion_status(self, client: TestClient) -> None:
        """Test delete_all removes tasks with mixed completion status"""
        # Create tasks with different completion status
        client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})
        task2_response = client.post(
            "/api/tasks",
            json={"title": "Task 2", "description": "Desc 2"}
        )
        task2_id = task2_response.json()["id"]

        # Mark one as completed
        client.put(f"/api/tasks/{task2_id}", json={"completed": True})

        # Verify mixed status
        get_response = client.get("/api/tasks")
        tasks = get_response.json()["tasks"]
        assert any(t["completed"] for t in tasks)
        assert any(not t["completed"] for t in tasks)

        # Delete all
        response = client.delete("/api/tasks")
        assert response.status_code == 204

        # Verify all gone
        get_response = client.get("/api/tasks")
        assert get_response.json()["tasks"] == []

    def test_delete_all_preserves_database_schema(self, client: TestClient) -> None:
        """Test that delete_all doesn't affect database schema"""
        # Delete all tasks
        client.delete("/api/tasks")

        # Create new task to verify schema still works
        response = client.post(
            "/api/tasks",
            json={"title": "Test Task", "description": "Test Description"}
        )
        assert response.status_code == 201

        task = response.json()
        assert "id" in task
        assert "title" in task
        assert "description" in task
        assert "completed" in task
        assert "created_at" in task
        assert "updated_at" in task
