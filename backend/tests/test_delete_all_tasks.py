"""
Tests for delete all tasks functionality.

This test module covers:
- DELETE /api/tasks endpoint
- Repository delete_all() method
- Service delete_all_tasks() method
- Edge cases and error scenarios
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
        mock_tasks.clear()

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


class TestDeleteAllTasksEndpoint:
    """Integration tests for DELETE /api/tasks endpoint"""

    def test_delete_all_tasks_empty_list(self, client: TestClient) -> None:
        """Test DELETE /api/tasks with no tasks returns 204"""
        response = client.delete("/api/tasks")

        assert response.status_code == 204
        assert response.text == ""

    def test_delete_all_tasks_single_task(self, client: TestClient) -> None:
        """Test DELETE /api/tasks with one task"""
        # Create a task
        client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})

        # Verify task exists
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 1

        # Delete all tasks
        response = client.delete("/api/tasks")
        assert response.status_code == 204

        # Verify tasks are deleted
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0

    def test_delete_all_tasks_multiple_tasks(self, client: TestClient) -> None:
        """Test DELETE /api/tasks with multiple tasks"""
        # Create multiple tasks
        for i in range(5):
            client.post(
                "/api/tasks",
                json={"title": f"Task {i}", "description": f"Description {i}"}
            )

        # Verify tasks exist
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 5

        # Delete all tasks
        response = client.delete("/api/tasks")
        assert response.status_code == 204

        # Verify all tasks are deleted
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0

    def test_delete_all_tasks_returns_no_content(self, client: TestClient) -> None:
        """Test that DELETE /api/tasks returns no response body"""
        # Create some tasks
        client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})
        client.post("/api/tasks", json={"title": "Task 2", "description": "Desc 2"})

        # Delete all tasks
        response = client.delete("/api/tasks")

        assert response.status_code == 204
        assert response.text == ""
        assert len(response.content) == 0

    def test_delete_all_tasks_idempotent(self, client: TestClient) -> None:
        """Test that deleting all tasks multiple times is idempotent"""
        # Create tasks
        client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})

        # Delete all tasks first time
        response = client.delete("/api/tasks")
        assert response.status_code == 204

        # Delete all tasks second time (no tasks exist)
        response = client.delete("/api/tasks")
        assert response.status_code == 204

        # Verify no tasks exist
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0

    def test_delete_all_tasks_can_create_after(self, client: TestClient) -> None:
        """Test that new tasks can be created after deleting all"""
        # Create and delete tasks
        client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})
        client.delete("/api/tasks")

        # Verify tasks are deleted
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0

        # Create new task
        response = client.post(
            "/api/tasks",
            json={"title": "New Task", "description": "New Description"}
        )
        assert response.status_code == 201

        # Verify new task exists
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 1
        assert response.json()["tasks"][0]["title"] == "New Task"


class TestDeleteAllTasksRepository:
    """Unit tests for TaskRepository.delete_all() method"""

    def test_repository_delete_all_empties_storage(self) -> None:
        """Test that delete_all removes all tasks from repository"""
        global mock_tasks
        mock_tasks = {}

        repo = create_mock_repository()

        # Create multiple tasks
        for i in range(3):
            repo.create(TaskCreate(title=f"Task {i}", description=f"Desc {i}"))

        assert len(mock_tasks) == 3

        # Delete all tasks
        repo.delete_all()

        # Verify storage is empty
        assert len(mock_tasks) == 0
        assert len(repo.get_all()) == 0

        mock_tasks = {}

    def test_repository_delete_all_no_tasks(self) -> None:
        """Test delete_all when no tasks exist"""
        global mock_tasks
        mock_tasks = {}

        repo = create_mock_repository()

        # Delete all with no tasks
        repo.delete_all()

        # Verify no errors and storage is still empty
        assert len(mock_tasks) == 0
        assert len(repo.get_all()) == 0

        mock_tasks = {}


class TestDeleteAllTasksService:
    """Unit tests for TaskService.delete_all_tasks() method"""

    def test_service_delete_all_calls_repository(self) -> None:
        """Test that service.delete_all_tasks calls repository.delete_all"""
        from app.services.task_service import TaskService

        global mock_tasks
        mock_tasks = {}

        repo = create_mock_repository()
        service = TaskService(repo)

        # Create tasks
        service.create_task(TaskCreate(title="Task 1", description="Desc 1"))
        service.create_task(TaskCreate(title="Task 2", description="Desc 2"))

        assert len(service.get_all_tasks()) == 2

        # Delete all tasks via service
        service.delete_all_tasks()

        # Verify all tasks deleted
        assert len(service.get_all_tasks()) == 0

        mock_tasks = {}


class TestDeleteAllTasksEdgeCases:
    """Edge case tests for delete all functionality"""

    def test_delete_all_does_not_affect_individual_delete(
        self, client: TestClient
    ) -> None:
        """Test that individual task delete still works after delete all"""
        # Create task
        response = client.post(
            "/api/tasks",
            json={"title": "Task 1", "description": "Desc 1"}
        )
        task_id = response.json()["id"]

        # Delete all
        client.delete("/api/tasks")

        # Create new task
        response = client.post(
            "/api/tasks",
            json={"title": "Task 2", "description": "Desc 2"}
        )
        new_task_id = response.json()["id"]

        # Try to delete old task (should return 404)
        response = client.delete(f"/api/tasks/{task_id}")
        assert response.status_code == 404

        # Delete new task (should succeed)
        response = client.delete(f"/api/tasks/{new_task_id}")
        assert response.status_code == 204

    def test_delete_all_with_completed_and_incomplete_tasks(
        self, client: TestClient
    ) -> None:
        """Test delete all removes both completed and incomplete tasks"""
        # Create completed task
        response = client.post(
            "/api/tasks",
            json={"title": "Completed Task", "description": "Done"}
        )
        task_id = response.json()["id"]
        client.put(
            f"/api/tasks/{task_id}",
            json={"completed": True}
        )

        # Create incomplete task
        client.post(
            "/api/tasks",
            json={"title": "Incomplete Task", "description": "Not done"}
        )

        # Verify both tasks exist
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 2

        # Delete all
        response = client.delete("/api/tasks")
        assert response.status_code == 204

        # Verify all deleted
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0

    def test_delete_all_preserves_task_schema(
        self, client: TestClient
    ) -> None:
        """Test that tasks created after delete all have proper schema"""
        # Create and delete
        client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})
        client.delete("/api/tasks")

        # Create new task
        response = client.post(
            "/api/tasks",
            json={"title": "New Task", "description": "New Desc"}
        )

        # Verify schema is correct
        task = response.json()
        assert "id" in task
        assert "title" in task
        assert "description" in task
        assert "completed" in task
        assert "created_at" in task
        assert "updated_at" in task
        assert task["title"] == "New Task"
        assert task["description"] == "New Desc"
        assert task["completed"] is False
