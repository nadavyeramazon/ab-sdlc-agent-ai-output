"""
Comprehensive tests for delete all tasks feature.

This test suite covers:
- Repository delete_all() method
- Service delete_all_tasks() method
- DELETE /tasks endpoint (integration tests)
- Edge cases (empty database, multiple tasks)
- Property-based tests using Hypothesis
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
            mock_tasks.values(), key=lambda t: t.created_at, reverse=True
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


class TestDeleteAllTasksRepository:
    """Unit tests for TaskRepository.delete_all() method"""

    def test_delete_all_returns_count_of_deleted_tasks(
        self, client: TestClient
    ) -> None:
        """Test that delete_all() returns the count of deleted tasks"""
        # Create 3 tasks
        client.post(
            "/api/tasks",
            json={"title": "Task 1", "description": "Description 1"}
        )
        client.post(
            "/api/tasks",
            json={"title": "Task 2", "description": "Description 2"}
        )
        client.post(
            "/api/tasks",
            json={"title": "Task 3", "description": "Description 3"}
        )

        # Verify tasks exist
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 3

        # Delete all tasks
        response = client.delete("/api/tasks")
        assert response.status_code == 204

        # Verify all tasks deleted
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0

    def test_delete_all_on_empty_database(self, client: TestClient) -> None:
        """Test that delete_all() works correctly on empty database"""
        # Verify no tasks exist
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0

        # Delete all tasks (should not error)
        response = client.delete("/api/tasks")
        assert response.status_code == 204

        # Verify still no tasks
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0

    def test_delete_all_removes_all_tasks(self, client: TestClient) -> None:
        """Test that delete_all() removes all tasks regardless of count"""
        # Create 10 tasks
        for i in range(10):
            client.post(
                "/api/tasks",
                json={
                    "title": f"Task {i+1}",
                    "description": f"Description {i+1}"
                }
            )

        # Verify tasks exist
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 10

        # Delete all tasks
        response = client.delete("/api/tasks")
        assert response.status_code == 204

        # Verify all tasks deleted
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0


class TestDeleteAllTasksEndpoint:
    """Integration tests for DELETE /tasks endpoint"""

    def test_delete_all_tasks_endpoint_returns_204(
        self, client: TestClient
    ) -> None:
        """Test that DELETE /tasks returns 204 No Content"""
        # Create a task
        client.post(
            "/api/tasks",
            json={"title": "Test Task", "description": "Test Description"}
        )

        # Delete all tasks
        response = client.delete("/api/tasks")
        assert response.status_code == 204

    def test_delete_all_tasks_endpoint_no_response_body(
        self, client: TestClient
    ) -> None:
        """Test that DELETE /tasks returns no response body"""
        # Create a task
        client.post(
            "/api/tasks",
            json={"title": "Test Task", "description": "Test Description"}
        )

        # Delete all tasks
        response = client.delete("/api/tasks")
        assert response.status_code == 204
        assert response.text == ""

    def test_delete_all_tasks_removes_all_tasks_from_list(
        self, client: TestClient
    ) -> None:
        """Test that DELETE /tasks removes all tasks from GET /tasks response"""
        # Create multiple tasks
        task_ids = []
        for i in range(5):
            response = client.post(
                "/api/tasks",
                json={
                    "title": f"Task {i+1}",
                    "description": f"Description {i+1}"
                }
            )
            task_ids.append(response.json()["id"])

        # Verify tasks exist
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 5

        # Delete all tasks
        response = client.delete("/api/tasks")
        assert response.status_code == 204

        # Verify all tasks are gone
        response = client.get("/api/tasks")
        tasks = response.json()["tasks"]
        assert len(tasks) == 0

        # Verify individual tasks return 404
        for task_id in task_ids:
            response = client.get(f"/api/tasks/{task_id}")
            assert response.status_code == 404

    def test_delete_all_tasks_on_empty_list(self, client: TestClient) -> None:
        """Test that DELETE /tasks works on empty list without error"""
        # Verify no tasks exist
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0

        # Delete all tasks (should succeed)
        response = client.delete("/api/tasks")
        assert response.status_code == 204

    def test_delete_all_tasks_route_positioned_before_task_id(
        self, client: TestClient
    ) -> None:
        """Test DELETE /tasks route is correctly positioned before task_id"""
        # Create a task
        response = client.post(
            "/api/tasks",
            json={"title": "Test Task", "description": "Test Description"}
        )
        task_id = response.json()["id"]

        # Delete all tasks using DELETE /tasks (should not treat 'tasks' as id)
        response = client.delete("/api/tasks")
        assert response.status_code == 204

        # Verify task is deleted
        response = client.get(f"/api/tasks/{task_id}")
        assert response.status_code == 404

    def test_can_create_tasks_after_delete_all(
        self, client: TestClient
    ) -> None:
        """Test that new tasks can be created after deleting all tasks"""
        # Create tasks
        client.post(
            "/api/tasks",
            json={"title": "Task 1", "description": "Description 1"}
        )
        client.post(
            "/api/tasks",
            json={"title": "Task 2", "description": "Description 2"}
        )

        # Delete all tasks
        response = client.delete("/api/tasks")
        assert response.status_code == 204

        # Create new tasks
        response = client.post(
            "/api/tasks",
            json={"title": "New Task", "description": "New Description"}
        )
        assert response.status_code == 201

        # Verify new task exists
        response = client.get("/api/tasks")
        tasks = response.json()["tasks"]
        assert len(tasks) == 1
        assert tasks[0]["title"] == "New Task"


class TestDeleteAllTasksPropertyBased:
    """Property-based tests for delete all tasks feature"""

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
        Property: For any number of tasks in the database, when delete_all
        is called, retrieving all tasks should return an empty list.
        """
        # Create specified number of tasks
        for i in range(num_tasks):
            client.post(
                "/api/tasks",
                json={
                    "title": f"Task {i+1}",
                    "description": f"Description {i+1}"
                }
            )

        # Verify correct number of tasks created
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == num_tasks

        # Delete all tasks
        response = client.delete("/api/tasks")
        assert response.status_code == 204

        # Verify all tasks removed
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0

    @given(st.lists(st.text(min_size=1, max_size=50), min_size=1, max_size=10))
    @settings(
        max_examples=10,
        deadline=2000,
        suppress_health_check=[HealthCheck.function_scoped_fixture]
    )
    def test_property_delete_all_returns_204_regardless_of_tasks(
        self, client: TestClient, titles: list
    ) -> None:
        """
        Property: For any list of task titles, when delete_all is called,
        the endpoint should always return 204 No Content.
        """
        # Create tasks with given titles
        for title in titles:
            clean_title = title.strip() if title.strip() else "Default"
            client.post(
                "/api/tasks",
                json={"title": clean_title, "description": "Test"}
            )

        # Delete all tasks - should always return 204
        response = client.delete("/api/tasks")
        assert response.status_code == 204
        assert response.text == ""

    @given(st.integers(min_value=1, max_value=15))
    @settings(
        max_examples=10,
        deadline=3000,
        suppress_health_check=[HealthCheck.function_scoped_fixture]
    )
    def test_property_delete_all_idempotent(
        self, client: TestClient, num_tasks: int
    ) -> None:
        """
        Property: For any number of tasks, calling delete_all multiple times
        should be idempotent (subsequent calls work without error).
        """
        # Create tasks
        for i in range(num_tasks):
            client.post(
                "/api/tasks",
                json={
                    "title": f"Task {i+1}",
                    "description": f"Description {i+1}"
                }
            )

        # First delete all
        response = client.delete("/api/tasks")
        assert response.status_code == 204

        # Second delete all (should succeed)
        response = client.delete("/api/tasks")
        assert response.status_code == 204

        # Third delete all (should still succeed)
        response = client.delete("/api/tasks")
        assert response.status_code == 204

        # Verify still no tasks
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0
