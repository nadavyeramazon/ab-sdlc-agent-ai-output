"""
Tests for bulk delete functionality (DELETE /api/tasks).

This test suite covers:
- DELETE /api/tasks endpoint (bulk delete)
- Repository delete_all() method
- Service delete_all_tasks() method
- Response validation
- Status codes
- Edge cases (empty database)
"""

from typing import Generator
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from hypothesis import given, settings, HealthCheck
from hypothesis import strategies as st

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
        return sorted(
            mock_tasks.values(),
            key=lambda t: t.created_at,
            reverse=True
        )

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


class TestBulkDeleteEndpoint:
    """Unit tests for DELETE /api/tasks endpoint (bulk delete)"""

    def test_delete_all_tasks_empty_database(
        self, client: TestClient
    ) -> None:
        """Test DELETE /api/tasks with empty database returns 204"""
        response = client.delete("/api/tasks")

        assert response.status_code == 204
        assert response.content == b""

    def test_delete_all_tasks_single_task(self, client: TestClient) -> None:
        """Test DELETE /api/tasks removes single task successfully"""
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
        assert delete_response.content == b""

        # Verify no tasks remain
        verify_response = client.get("/api/tasks")
        assert verify_response.status_code == 200
        assert len(verify_response.json()["tasks"]) == 0

    def test_delete_all_tasks_multiple_tasks(
        self, client: TestClient
    ) -> None:
        """Test DELETE /api/tasks removes multiple tasks successfully"""
        # Create multiple tasks
        for i in range(5):
            response = client.post(
                "/api/tasks",
                json={
                    "title": f"Task {i}",
                    "description": f"Description {i}"
                }
            )
            assert response.status_code == 201

        # Verify tasks exist
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 5

        # Delete all tasks
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204
        assert delete_response.content == b""

        # Verify no tasks remain
        verify_response = client.get("/api/tasks")
        assert verify_response.status_code == 200
        assert len(verify_response.json()["tasks"]) == 0

    def test_delete_all_tasks_idempotent(self, client: TestClient) -> None:
        """Test DELETE /api/tasks is idempotent (multiple calls)"""
        # Create tasks
        client.post(
            "/api/tasks",
            json={"title": "Task 1", "description": "Desc 1"}
        )
        client.post(
            "/api/tasks",
            json={"title": "Task 2", "description": "Desc 2"}
        )

        # First delete
        response1 = client.delete("/api/tasks")
        assert response1.status_code == 204

        # Second delete (on empty database)
        response2 = client.delete("/api/tasks")
        assert response2.status_code == 204

        # Verify still empty
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 0

    def test_delete_all_then_create_new_task(
        self, client: TestClient
    ) -> None:
        """Test creating new task after bulk delete works correctly"""
        # Create and delete tasks
        client.post(
            "/api/tasks",
            json={"title": "Task 1", "description": "Desc 1"}
        )
        client.delete("/api/tasks")

        # Create new task after delete
        response = client.post(
            "/api/tasks",
            json={"title": "New Task", "description": "New Description"}
        )
        assert response.status_code == 201

        # Verify only new task exists
        get_response = client.get("/api/tasks")
        tasks = get_response.json()["tasks"]
        assert len(tasks) == 1
        assert tasks[0]["title"] == "New Task"

    def test_delete_all_tasks_no_body_required(
        self, client: TestClient
    ) -> None:
        """Test DELETE /api/tasks does not require request body"""
        response = client.delete("/api/tasks")

        assert response.status_code == 204
        assert response.content == b""

    def test_delete_all_tasks_with_completed_and_incomplete(
        self, client: TestClient
    ) -> None:
        """Test DELETE /api/tasks removes completed and incomplete tasks"""
        # Create tasks with different completion status
        task1_response = client.post(
            "/api/tasks",
            json={"title": "Incomplete Task", "description": "Not done"}
        )
        task1_id = task1_response.json()["id"]

        task2_response = client.post(
            "/api/tasks",
            json={"title": "Completed Task", "description": "Done"}
        )
        task2_id = task2_response.json()["id"]

        # Mark one as completed
        client.put(
            f"/api/tasks/{task2_id}",
            json={"completed": True}
        )

        # Delete all
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204

        # Verify both are deleted
        assert client.get(f"/api/tasks/{task1_id}").status_code == 404
        assert client.get(f"/api/tasks/{task2_id}").status_code == 404


class TestBulkDeleteRepository:
    """Unit tests for repository delete_all() method"""

    def test_repository_delete_all_returns_count(self) -> None:
        """Test that repository delete_all() returns deleted count"""
        global mock_tasks
        mock_tasks = {}

        repo = create_mock_repository()

        # Create tasks
        repo.create(TaskCreate(title="Task 1", description="Desc 1"))
        repo.create(TaskCreate(title="Task 2", description="Desc 2"))
        repo.create(TaskCreate(title="Task 3", description="Desc 3"))

        # Delete all
        count = repo.delete_all()

        assert count == 3
        assert len(repo.get_all()) == 0

        mock_tasks = {}

    def test_repository_delete_all_empty_returns_zero(self) -> None:
        """Test repository delete_all() returns 0 for empty database"""
        global mock_tasks
        mock_tasks = {}

        repo = create_mock_repository()

        count = repo.delete_all()

        assert count == 0
        assert len(repo.get_all()) == 0

        mock_tasks = {}


class TestBulkDeleteProperties:
    """Property-based tests for bulk delete functionality"""

    @given(st.integers(min_value=0, max_value=20))
    @settings(
        max_examples=10,
        deadline=2000,
        suppress_health_check=[HealthCheck.function_scoped_fixture]
    )
    def test_property_delete_all_removes_all_tasks(
        self, client: TestClient, num_tasks: int
    ) -> None:
        """
        Property: For any number of tasks, DELETE /api/tasks should remove
        all tasks from the database, leaving it empty.
        """
        global mock_tasks
        mock_tasks = {}

        # Create N tasks
        for i in range(num_tasks):
            response = client.post(
                "/api/tasks",
                json={
                    "title": f"Task {i}",
                    "description": f"Description {i}"
                }
            )
            assert response.status_code == 201

        # Verify tasks were created
        get_before = client.get("/api/tasks")
        assert len(get_before.json()["tasks"]) == num_tasks

        # Delete all tasks
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204

        # Verify no tasks remain
        get_after = client.get("/api/tasks")
        assert get_after.status_code == 200
        assert len(get_after.json()["tasks"]) == 0

        mock_tasks = {}

    @given(st.integers(min_value=1, max_value=10))
    @settings(
        max_examples=5,
        deadline=2000,
        suppress_health_check=[HealthCheck.function_scoped_fixture]
    )
    def test_property_delete_all_then_recreate_works(
        self, client: TestClient, num_cycles: int
    ) -> None:
        """
        Property: Bulk delete operation is idempotent and can be repeated
        multiple times with create operations in between.
        """
        global mock_tasks
        mock_tasks = {}

        for cycle in range(num_cycles):
            # Create some tasks
            client.post(
                "/api/tasks",
                json={"title": f"Task {cycle}", "description": "Test"}
            )

            # Verify created
            get_response = client.get("/api/tasks")
            assert len(get_response.json()["tasks"]) >= 1

            # Delete all
            delete_response = client.delete("/api/tasks")
            assert delete_response.status_code == 204

            # Verify empty
            verify_response = client.get("/api/tasks")
            assert len(verify_response.json()["tasks"]) == 0

        mock_tasks = {}
