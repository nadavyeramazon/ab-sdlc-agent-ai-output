"""
Unit and integration tests for DELETE /api/tasks bulk delete endpoint.

This test suite covers the new bulk delete functionality across all layers:
- Repository layer (delete_all method)
- Service layer (delete_all_tasks method)
- API endpoint (DELETE /api/tasks)
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
        """Delete all tasks from mock storage"""
        mock_tasks.clear()

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


@pytest.fixture
def test_repo():
    """Create a TaskRepository for testing with mocked storage."""
    global mock_tasks
    mock_tasks = {}

    with patch('app.repositories.task_repository.TaskRepository._initialize_database'):
        repo = create_mock_repository()
        yield repo

    mock_tasks = {}


class TestRepositoryDeleteAll:
    """Unit tests for TaskRepository.delete_all() method"""

    def test_delete_all_removes_all_tasks(self, test_repo) -> None:
        """Test that delete_all removes all tasks from repository"""
        # Create multiple tasks
        test_repo.create(TaskCreate(title="Task 1", description="Description 1"))
        test_repo.create(TaskCreate(title="Task 2", description="Description 2"))
        test_repo.create(TaskCreate(title="Task 3", description="Description 3"))

        # Verify tasks exist
        all_tasks = test_repo.get_all()
        assert len(all_tasks) == 3

        # Delete all tasks
        test_repo.delete_all()

        # Verify all tasks are removed
        all_tasks = test_repo.get_all()
        assert len(all_tasks) == 0

    def test_delete_all_on_empty_repository(self, test_repo) -> None:
        """Test that delete_all works when repository is already empty"""
        # Verify repository is empty
        all_tasks = test_repo.get_all()
        assert len(all_tasks) == 0

        # Delete all tasks (should not raise error)
        test_repo.delete_all()

        # Verify repository is still empty
        all_tasks = test_repo.get_all()
        assert len(all_tasks) == 0

    def test_delete_all_allows_new_tasks_after(self, test_repo) -> None:
        """Test that new tasks can be created after delete_all"""
        # Create and delete tasks
        test_repo.create(TaskCreate(title="Task 1", description="Description 1"))
        test_repo.delete_all()

        # Create new task after deletion
        new_task = test_repo.create(TaskCreate(title="New Task", description="New Description"))

        # Verify new task exists
        all_tasks = test_repo.get_all()
        assert len(all_tasks) == 1
        assert all_tasks[0].id == new_task.id
        assert all_tasks[0].title == "New Task"


class TestServiceDeleteAllTasks:
    """Unit tests for TaskService.delete_all_tasks() method"""

    def test_service_calls_repository_delete_all(self, test_repo) -> None:
        """Test that service method delegates to repository"""
        from app.services.task_service import TaskService

        service = TaskService(repository=test_repo)

        # Create tasks
        service.create_task(TaskCreate(title="Task 1", description="Description 1"))
        service.create_task(TaskCreate(title="Task 2", description="Description 2"))

        # Verify tasks exist
        assert len(service.get_all_tasks()) == 2

        # Delete all tasks
        service.delete_all_tasks()

        # Verify all tasks are removed
        assert len(service.get_all_tasks()) == 0


class TestDeleteAllTasksEndpoint:
    """Integration tests for DELETE /api/tasks endpoint"""

    def test_delete_all_tasks_returns_204(self, client: TestClient) -> None:
        """Test that DELETE /api/tasks returns 204 No Content"""
        # Create some tasks
        client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})
        client.post("/api/tasks", json={"title": "Task 2", "description": "Desc 2"})

        # Delete all tasks
        response = client.delete("/api/tasks")

        # Verify 204 No Content response
        assert response.status_code == 204
        assert response.text == ""

    def test_delete_all_tasks_removes_all_tasks(self, client: TestClient) -> None:
        """Test that DELETE /api/tasks removes all tasks"""
        # Create multiple tasks
        client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})
        client.post("/api/tasks", json={"title": "Task 2", "description": "Desc 2"})
        client.post("/api/tasks", json={"title": "Task 3", "description": "Desc 3"})

        # Verify tasks exist
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 3

        # Delete all tasks
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204

        # Verify all tasks are removed
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0

    def test_delete_all_tasks_on_empty_list(self, client: TestClient) -> None:
        """Test that DELETE /api/tasks works when no tasks exist"""
        # Verify no tasks exist
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0

        # Delete all tasks (should not raise error)
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204

        # Verify still no tasks
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0

    def test_can_create_tasks_after_delete_all(self, client: TestClient) -> None:
        """Test that new tasks can be created after delete_all"""
        # Create and delete tasks
        client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})
        client.delete("/api/tasks")

        # Create new task after deletion
        response = client.post(
            "/api/tasks",
            json={"title": "New Task", "description": "New Description"}
        )

        assert response.status_code == 201
        new_task = response.json()
        assert new_task["title"] == "New Task"

        # Verify only new task exists
        response = client.get("/api/tasks")
        tasks = response.json()["tasks"]
        assert len(tasks) == 1
        assert tasks[0]["title"] == "New Task"

    def test_delete_all_does_not_conflict_with_delete_by_id(
        self, client: TestClient
    ) -> None:
        """Test that DELETE /api/tasks doesn't conflict with DELETE /api/tasks/{id}"""
        # Create tasks
        response1 = client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})
        task1_id = response1.json()["id"]
        client.post("/api/tasks", json={"title": "Task 2", "description": "Desc 2"})
        client.post("/api/tasks", json={"title": "Task 3", "description": "Desc 3"})

        # Delete single task by ID
        delete_response = client.delete(f"/api/tasks/{task1_id}")
        assert delete_response.status_code == 204

        # Verify only 2 tasks remain
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 2

        # Delete all remaining tasks
        delete_all_response = client.delete("/api/tasks")
        assert delete_all_response.status_code == 204

        # Verify all tasks are removed
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0

    def test_delete_all_with_varying_task_counts(self, client: TestClient) -> None:
        """Test DELETE /api/tasks with different numbers of tasks"""
        # Test with 1 task
        client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})
        response = client.delete("/api/tasks")
        assert response.status_code == 204
        assert len(client.get("/api/tasks").json()["tasks"]) == 0

        # Test with 5 tasks
        for i in range(5):
            client.post("/api/tasks", json={"title": f"Task {i}", "description": f"Desc {i}"})
        response = client.delete("/api/tasks")
        assert response.status_code == 204
        assert len(client.get("/api/tasks").json()["tasks"]) == 0

        # Test with 10 tasks
        for i in range(10):
            client.post("/api/tasks", json={"title": f"Task {i}", "description": f"Desc {i}"})
        response = client.delete("/api/tasks")
        assert response.status_code == 204
        assert len(client.get("/api/tasks").json()["tasks"]) == 0

    def test_delete_all_only_accepts_delete_method(self, client: TestClient) -> None:
        """Test that /api/tasks only accepts DELETE method for bulk operations"""
        # GET is allowed (get all tasks)
        assert client.get("/api/tasks").status_code == 200

        # POST is allowed (create task)
        response = client.post("/api/tasks", json={"title": "Task", "description": "Desc"})
        assert response.status_code == 201

        # DELETE is allowed (delete all)
        assert client.delete("/api/tasks").status_code == 204

        # PUT is not allowed on /api/tasks (no path parameter)
        assert client.put("/api/tasks", json={"title": "Updated"}).status_code == 405

    def test_delete_all_tasks_persists_across_requests(self, client: TestClient) -> None:
        """Test that delete_all effect persists across multiple requests"""
        # Create tasks
        client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})
        client.post("/api/tasks", json={"title": "Task 2", "description": "Desc 2"})

        # Delete all
        client.delete("/api/tasks")

        # Make multiple GET requests to verify persistence
        for _ in range(3):
            response = client.get("/api/tasks")
            assert len(response.json()["tasks"]) == 0


class TestDeleteAllEdgeCases:
    """Edge case tests for bulk delete functionality"""

    def test_delete_all_with_completed_and_incomplete_tasks(
        self, client: TestClient
    ) -> None:
        """Test that delete_all removes both completed and incomplete tasks"""
        # Create incomplete task
        client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})

        # Create and complete another task
        response2 = client.post("/api/tasks", json={"title": "Task 2", "description": "Desc 2"})
        task2_id = response2.json()["id"]
        client.put(f"/api/tasks/{task2_id}", json={"completed": True})

        # Verify we have one completed and one incomplete task
        tasks = client.get("/api/tasks").json()["tasks"]
        assert len(tasks) == 2
        completed_count = sum(1 for t in tasks if t["completed"])
        assert completed_count == 1

        # Delete all tasks
        client.delete("/api/tasks")

        # Verify all tasks are removed regardless of completion status
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0

    def test_delete_all_with_long_descriptions(self, client: TestClient) -> None:
        """Test that delete_all handles tasks with long descriptions"""
        # Create tasks with varying description lengths
        long_desc = "a" * 1000  # Max length description
        client.post("/api/tasks", json={"title": "Task 1", "description": long_desc})
        client.post("/api/tasks", json={"title": "Task 2", "description": ""})
        client.post("/api/tasks", json={"title": "Task 3", "description": "Normal desc"})

        # Delete all
        response = client.delete("/api/tasks")
        assert response.status_code == 204

        # Verify all removed
        assert len(client.get("/api/tasks").json()["tasks"]) == 0
