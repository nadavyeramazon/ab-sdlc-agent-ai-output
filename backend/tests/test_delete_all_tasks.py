"""
Tests for delete all tasks functionality.

This test suite covers:
- DELETE /api/tasks endpoint (delete all tasks)
- Repository delete_all method
- Service delete_all_tasks method
- Edge cases and error scenarios
- Property-based tests
"""

from typing import Generator
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from app.main import create_app
from app.models.task import Task, TaskCreate
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService


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


@pytest.fixture
def test_repo():
    """
    Create a TaskRepository for testing with mocked storage.
    Cleans up all tasks before and after each test.
    """
    global mock_tasks
    mock_tasks = {}

    with patch('app.repositories.task_repository.TaskRepository._initialize_database'):
        repo = create_mock_repository()
        yield repo

    mock_tasks = {}


class TestDeleteAllTasksEndpoint:
    """Unit tests for DELETE /api/tasks endpoint"""

    def test_delete_all_tasks_empty_list(self, client: TestClient) -> None:
        """Test DELETE /api/tasks with no tasks returns 204"""
        response = client.delete("/api/tasks")

        assert response.status_code == 204
        assert response.content == b''

        # Verify tasks list is still empty
        get_response = client.get("/api/tasks")
        assert get_response.status_code == 200
        assert len(get_response.json()["tasks"]) == 0

    def test_delete_all_tasks_single_task(self, client: TestClient) -> None:
        """Test DELETE /api/tasks with one task"""
        # Create a task
        client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})

        # Verify task exists
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 1

        # Delete all tasks
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204

        # Verify tasks list is empty
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 0

    def test_delete_all_tasks_multiple_tasks(self, client: TestClient) -> None:
        """Test DELETE /api/tasks with multiple tasks"""
        # Create multiple tasks
        for i in range(5):
            client.post("/api/tasks", json={"title": f"Task {i}", "description": f"Desc {i}"})

        # Verify tasks exist
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 5

        # Delete all tasks
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204
        assert delete_response.content == b''

        # Verify tasks list is empty
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 0

    def test_delete_all_tasks_idempotent(self, client: TestClient) -> None:
        """Test DELETE /api/tasks is idempotent (can be called multiple times)"""
        # Create tasks
        client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})
        client.post("/api/tasks", json={"title": "Task 2", "description": "Desc 2"})

        # First delete
        response1 = client.delete("/api/tasks")
        assert response1.status_code == 204

        # Second delete (should still succeed)
        response2 = client.delete("/api/tasks")
        assert response2.status_code == 204

        # Third delete (should still succeed)
        response3 = client.delete("/api/tasks")
        assert response3.status_code == 204

        # Verify list is empty
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 0

    def test_delete_all_tasks_no_content_response(self, client: TestClient) -> None:
        """Test DELETE /api/tasks returns no content in body"""
        # Create a task
        client.post("/api/tasks", json={"title": "Task", "description": "Desc"})

        # Delete all
        response = client.delete("/api/tasks")

        assert response.status_code == 204
        assert response.content == b''
        assert len(response.text) == 0

    def test_delete_all_then_create_new_task(self, client: TestClient) -> None:
        """Test that new tasks can be created after delete all"""
        # Create initial tasks
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

        # Verify only the new task exists
        get_response = client.get("/api/tasks")
        tasks = get_response.json()["tasks"]
        assert len(tasks) == 1
        assert tasks[0]["title"] == "New Task"

    def test_delete_all_does_not_conflict_with_delete_by_id(
        self, client: TestClient
    ) -> None:
        """Test DELETE /api/tasks (all) does not conflict with DELETE /api/tasks/{id}"""
        # Create tasks
        response1 = client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})
        task1_id = response1.json()["id"]

        response2 = client.post("/api/tasks", json={"title": "Task 2", "description": "Desc 2"})
        task2_id = response2.json()["id"]

        # Delete specific task by ID
        delete_by_id = client.delete(f"/api/tasks/{task1_id}")
        assert delete_by_id.status_code == 204

        # Verify one task remains
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 1

        # Delete all tasks
        delete_all = client.delete("/api/tasks")
        assert delete_all.status_code == 204

        # Verify no tasks remain
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 0


class TestDeleteAllRepository:
    """Unit tests for TaskRepository.delete_all() method"""

    def test_repository_delete_all_returns_count(self, test_repo) -> None:
        """Test that delete_all returns the number of deleted tasks"""
        # Create tasks
        test_repo.create(TaskCreate(title="Task 1", description="Desc 1"))
        test_repo.create(TaskCreate(title="Task 2", description="Desc 2"))
        test_repo.create(TaskCreate(title="Task 3", description="Desc 3"))

        # Delete all and verify count
        count = test_repo.delete_all()
        assert count == 3

        # Verify tasks are deleted
        assert len(test_repo.get_all()) == 0

    def test_repository_delete_all_empty_returns_zero(self, test_repo) -> None:
        """Test that delete_all returns 0 when no tasks exist"""
        count = test_repo.delete_all()
        assert count == 0

    def test_repository_delete_all_removes_all_tasks(self, test_repo) -> None:
        """Test that delete_all removes all tasks"""
        # Create multiple tasks
        for i in range(10):
            test_repo.create(TaskCreate(title=f"Task {i}", description=f"Desc {i}"))

        # Verify tasks exist
        assert len(test_repo.get_all()) == 10

        # Delete all
        test_repo.delete_all()

        # Verify no tasks remain
        assert len(test_repo.get_all()) == 0


class TestDeleteAllService:
    """Unit tests for TaskService.delete_all_tasks() method"""

    def test_service_delete_all_calls_repository(self, test_repo) -> None:
        """Test that service.delete_all_tasks calls repository.delete_all"""
        service = TaskService(test_repo)

        # Create tasks
        service.create_task(TaskCreate(title="Task 1", description="Desc 1"))
        service.create_task(TaskCreate(title="Task 2", description="Desc 2"))

        # Delete all
        count = service.delete_all_tasks()

        # Verify count returned
        assert count == 2

        # Verify tasks are deleted
        assert len(service.get_all_tasks()) == 0

    def test_service_delete_all_returns_count(self, test_repo) -> None:
        """Test that service.delete_all_tasks returns the count"""
        service = TaskService(test_repo)

        # Test with 0 tasks
        assert service.delete_all_tasks() == 0

        # Create tasks and test again
        service.create_task(TaskCreate(title="Task", description="Desc"))
        assert service.delete_all_tasks() == 1


class TestDeleteAllPropertyBased:
    """Property-based tests for delete all functionality"""

    @given(st.integers(min_value=0, max_value=20))
    @settings(
        max_examples=10,
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        deadline=2000
    )
    def test_property_delete_all_removes_n_tasks(
        self, client: TestClient, num_tasks: int
    ) -> None:
        """
        Property: Delete all removes exactly N tasks
        For any number of tasks N, after creating N tasks and calling
        delete_all, the task list should be empty and the count should be N.
        """
        # Create N tasks
        for i in range(num_tasks):
            response = client.post(
                "/api/tasks",
                json={"title": f"Task {i}", "description": f"Description {i}"}
            )
            assert response.status_code == 201

        # Verify N tasks exist
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == num_tasks

        # Delete all tasks
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204

        # Verify list is empty
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 0

    @given(st.lists(
        st.text(min_size=1, max_size=100).filter(lambda s: s.strip()),
        min_size=1,
        max_size=10
    ))
    @settings(
        max_examples=10,
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        deadline=3000
    )
    def test_property_delete_all_idempotent(
        self, client: TestClient, task_titles: list
    ) -> None:
        """
        Property: Delete all is idempotent
        For any list of tasks, calling delete_all multiple times
        should always result in an empty list and return 204.
        """
        # Create tasks
        for title in task_titles:
            client.post(
                "/api/tasks",
                json={"title": title.strip(), "description": "Test"}
            )

        # First delete
        response1 = client.delete("/api/tasks")
        assert response1.status_code == 204

        # Second delete should also succeed
        response2 = client.delete("/api/tasks")
        assert response2.status_code == 204

        # Verify still empty
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 0

    @given(st.integers(min_value=1, max_value=10))
    @settings(
        max_examples=10,
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        deadline=3000
    )
    def test_property_delete_all_then_create(
        self, client: TestClient, initial_count: int
    ) -> None:
        """
        Property: Delete all then create
        For any number of initial tasks, after deleting all and creating
        one new task, exactly one task should exist.
        """
        # Create initial tasks
        for i in range(initial_count):
            client.post(
                "/api/tasks",
                json={"title": f"Initial {i}", "description": "Initial"}
            )

        # Delete all
        client.delete("/api/tasks")

        # Create new task
        response = client.post(
            "/api/tasks",
            json={"title": "New Task", "description": "New"}
        )
        assert response.status_code == 201

        # Verify exactly one task exists
        get_response = client.get("/api/tasks")
        tasks = get_response.json()["tasks"]
        assert len(tasks) == 1
        assert tasks[0]["title"] == "New Task"
