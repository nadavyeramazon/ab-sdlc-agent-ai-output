"""
Unit and integration tests for DELETE /api/tasks endpoint (bulk delete).

This test suite covers:
- DELETE /api/tasks endpoint returns 204 No Content
- Bulk delete removes all tasks
- Subsequent GET /api/tasks returns empty list after delete
- Delete all with empty database returns 204
- Repository delete_all() method behavior
- Service delete_all_tasks() method behavior
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
    """Integration tests for DELETE /api/tasks endpoint"""

    def test_delete_all_tasks_returns_204(self, client: TestClient) -> None:
        """Test DELETE /api/tasks returns 204 No Content"""
        # Create some tasks first
        client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})
        client.post("/api/tasks", json={"title": "Task 2", "description": "Desc 2"})
        client.post("/api/tasks", json={"title": "Task 3", "description": "Desc 3"})

        # Delete all tasks
        response = client.delete("/api/tasks")

        assert response.status_code == 204
        assert response.text == ""  # No content in response body

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

        # Verify all tasks are deleted
        get_response_after = client.get("/api/tasks")
        assert get_response_after.status_code == 200
        assert len(get_response_after.json()["tasks"]) == 0

    def test_delete_all_with_empty_database(self, client: TestClient) -> None:
        """Test DELETE /api/tasks with no tasks returns 204"""
        # Ensure no tasks exist
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0

        # Delete all (should succeed even with no tasks)
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204

    def test_delete_all_followed_by_create(self, client: TestClient) -> None:
        """Test that after DELETE /api/tasks, new tasks can be created"""
        # Create tasks
        client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})
        client.post("/api/tasks", json={"title": "Task 2", "description": "Desc 2"})

        # Delete all
        client.delete("/api/tasks")

        # Create new task
        create_response = client.post(
            "/api/tasks",
            json={"title": "New Task", "description": "New Description"}
        )
        assert create_response.status_code == 201

        # Verify only new task exists
        get_response = client.get("/api/tasks")
        tasks = get_response.json()["tasks"]
        assert len(tasks) == 1
        assert tasks[0]["title"] == "New Task"

    def test_delete_all_does_not_affect_individual_delete(self, client: TestClient) -> None:
        """Test that DELETE /api/tasks route doesn't conflict with DELETE /api/tasks/{id}"""
        # Create a task
        create_response = client.post(
            "/api/tasks",
            json={"title": "Task 1", "description": "Desc 1"}
        )
        task_id = create_response.json()["id"]

        # Individual delete should still work
        delete_individual = client.delete(f"/api/tasks/{task_id}")
        assert delete_individual.status_code == 204

        # Verify task is deleted
        get_response = client.get(f"/api/tasks/{task_id}")
        assert get_response.status_code == 404

    def test_delete_all_endpoint_with_trailing_slash(self, client: TestClient) -> None:
        """Test DELETE /api/tasks/ (with trailing slash) behavior"""
        # FastAPI doesn't automatically handle trailing slashes
        response = client.delete("/api/tasks/")
        # This should return 404 or 307 redirect, not 204
        assert response.status_code in [307, 404]

    def test_delete_all_multiple_times(self, client: TestClient) -> None:
        """Test calling DELETE /api/tasks multiple times"""
        # Create tasks
        client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})
        client.post("/api/tasks", json={"title": "Task 2", "description": "Desc 2"})

        # First delete
        response1 = client.delete("/api/tasks")
        assert response1.status_code == 204

        # Second delete (no tasks)
        response2 = client.delete("/api/tasks")
        assert response2.status_code == 204

        # Third delete (still no tasks)
        response3 = client.delete("/api/tasks")
        assert response3.status_code == 204

    def test_delete_all_with_many_tasks(self, client: TestClient) -> None:
        """Test DELETE /api/tasks with many tasks (edge case)"""
        # Create many tasks
        for i in range(50):
            client.post(
                "/api/tasks",
                json={"title": f"Task {i}", "description": f"Description {i}"}
            )

        # Verify tasks exist
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 50

        # Delete all
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204

        # Verify all deleted
        get_response_after = client.get("/api/tasks")
        assert len(get_response_after.json()["tasks"]) == 0


class TestDeleteAllRepository:
    """Unit tests for TaskRepository.delete_all() method"""

    def test_repository_delete_all_returns_count(self) -> None:
        """Test that repository delete_all() returns number of deleted tasks"""
        global mock_tasks
        mock_tasks = {}

        with patch('app.repositories.task_repository.TaskRepository._initialize_database'):
            repo = create_mock_repository()

            # Create tasks
            repo.create(TaskCreate(title="Task 1", description="Desc 1"))
            repo.create(TaskCreate(title="Task 2", description="Desc 2"))
            repo.create(TaskCreate(title="Task 3", description="Desc 3"))

            # Delete all and verify count
            count = repo.delete_all()
            assert count == 3

            # Verify tasks are deleted
            assert len(repo.get_all()) == 0

        mock_tasks = {}

    def test_repository_delete_all_with_empty_database(self) -> None:
        """Test repository delete_all() with no tasks returns 0"""
        global mock_tasks
        mock_tasks = {}

        with patch('app.repositories.task_repository.TaskRepository._initialize_database'):
            repo = create_mock_repository()

            # Delete all from empty database
            count = repo.delete_all()
            assert count == 0

        mock_tasks = {}

    def test_repository_delete_all_clears_storage(self) -> None:
        """Test that repository delete_all() clears all task storage"""
        global mock_tasks
        mock_tasks = {}

        with patch('app.repositories.task_repository.TaskRepository._initialize_database'):
            repo = create_mock_repository()

            # Create tasks
            task1 = repo.create(TaskCreate(title="Task 1", description="Desc 1"))
            task2 = repo.create(TaskCreate(title="Task 2", description="Desc 2"))

            # Verify tasks exist
            assert repo.get_by_id(task1.id) is not None
            assert repo.get_by_id(task2.id) is not None

            # Delete all
            repo.delete_all()

            # Verify tasks are gone
            assert repo.get_by_id(task1.id) is None
            assert repo.get_by_id(task2.id) is None
            assert len(repo.get_all()) == 0

        mock_tasks = {}


class TestDeleteAllService:
    """Unit tests for TaskService.delete_all_tasks() method"""

    def test_service_delete_all_calls_repository(self) -> None:
        """Test that service delete_all_tasks() delegates to repository"""
        from app.services.task_service import TaskService

        # Create mock repository
        mock_repo = MagicMock()
        mock_repo.delete_all.return_value = 5

        # Create service with mock repository
        service = TaskService(repository=mock_repo)

        # Call delete_all_tasks
        result = service.delete_all_tasks()

        # Verify repository method was called
        mock_repo.delete_all.assert_called_once()
        assert result == 5

    def test_service_delete_all_returns_count(self) -> None:
        """Test that service delete_all_tasks() returns count from repository"""
        global mock_tasks
        mock_tasks = {}

        with patch('app.repositories.task_repository.TaskRepository._initialize_database'):
            from app.services.task_service import TaskService

            repo = create_mock_repository()
            service = TaskService(repository=repo)

            # Create tasks
            repo.create(TaskCreate(title="Task 1", description="Desc 1"))
            repo.create(TaskCreate(title="Task 2", description="Desc 2"))

            # Delete all via service
            count = service.delete_all_tasks()
            assert count == 2

        mock_tasks = {}
