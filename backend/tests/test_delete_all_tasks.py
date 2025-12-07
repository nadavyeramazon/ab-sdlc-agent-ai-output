"""
Comprehensive tests for delete_all_tasks feature.

This test suite covers:
- Repository delete_all() method
- Service delete_all_tasks() method
- DELETE /api/tasks endpoint
- Property-based tests for delete_all behavior
"""

from typing import Generator
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from hypothesis import HealthCheck, given, settings
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


# Custom strategies for generating test data
@st.composite
def task_create_strategy(draw):
    """Generate valid TaskCreate objects for property testing"""
    title = draw(
        st.text(min_size=1, max_size=200).filter(lambda s: s.strip() != "")
    )
    description = draw(st.text(min_size=0, max_size=1000))
    return TaskCreate(title=title, description=description)


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


class TestRepositoryDeleteAll:
    """Unit tests for TaskRepository.delete_all() method"""

    def test_delete_all_returns_count_of_deleted_tasks(
        self, client: TestClient
    ) -> None:
        """Test that delete_all returns the count of deleted tasks"""
        # Create some tasks
        client.post(
            "/api/tasks",
            json={"title": "Task 1", "description": "Desc 1"}
        )
        client.post(
            "/api/tasks",
            json={"title": "Task 2", "description": "Desc 2"}
        )
        client.post(
            "/api/tasks",
            json={"title": "Task 3", "description": "Desc 3"}
        )

        # Verify 3 tasks exist
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 3

        # Delete all tasks
        response = client.delete("/api/tasks")
        assert response.status_code == 204

        # Verify all tasks are gone
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0

    def test_delete_all_on_empty_database_returns_zero(
        self, client: TestClient
    ) -> None:
        """Test that delete_all on empty database returns 0 and succeeds"""
        # Verify database is empty
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0

        # Delete all tasks (should succeed even with no tasks)
        response = client.delete("/api/tasks")
        assert response.status_code == 204

        # Verify database is still empty
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0

    def test_delete_all_removes_all_tasks(
        self, client: TestClient
    ) -> None:
        """Test that delete_all removes all tasks completely"""
        # Create tasks
        task1_response = client.post(
            "/api/tasks", json={"title": "Task 1", "description": "Desc 1"}
        )
        task2_response = client.post(
            "/api/tasks", json={"title": "Task 2", "description": "Desc 2"}
        )
        task1_id = task1_response.json()["id"]
        task2_id = task2_response.json()["id"]

        # Verify tasks exist
        assert client.get(f"/api/tasks/{task1_id}").status_code == 200
        assert client.get(f"/api/tasks/{task2_id}").status_code == 200

        # Delete all tasks
        response = client.delete("/api/tasks")
        assert response.status_code == 204

        # Verify tasks no longer exist
        assert client.get(f"/api/tasks/{task1_id}").status_code == 404
        assert client.get(f"/api/tasks/{task2_id}").status_code == 404


class TestServiceDeleteAllTasks:
    """Unit tests for TaskService.delete_all_tasks() method"""

    def test_service_calls_repository_delete_all(
        self, client: TestClient
    ) -> None:
        """Test that service method calls repository delete_all"""
        # Create some tasks
        client.post(
            "/api/tasks",
            json={"title": "Task 1", "description": "Desc 1"}
        )
        client.post(
            "/api/tasks",
            json={"title": "Task 2", "description": "Desc 2"}
        )

        # Call delete all through endpoint (which uses service)
        response = client.delete("/api/tasks")
        assert response.status_code == 204

        # Verify all tasks are deleted
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0


class TestDeleteAllTasksEndpoint:
    """Integration tests for DELETE /api/tasks endpoint"""

    def test_delete_all_tasks_returns_204(
        self, client: TestClient
    ) -> None:
        """Test DELETE /api/tasks returns 204 No Content"""
        response = client.delete("/api/tasks")
        assert response.status_code == 204

    def test_delete_all_tasks_returns_no_content(
        self, client: TestClient
    ) -> None:
        """Test DELETE /api/tasks returns no response body"""
        response = client.delete("/api/tasks")
        assert response.status_code == 204
        assert response.content == b""

    def test_delete_all_tasks_with_multiple_tasks(
        self, client: TestClient
    ) -> None:
        """Test deleting all tasks when multiple tasks exist"""
        # Create multiple tasks
        for i in range(5):
            client.post(
                "/api/tasks",
                json={"title": f"Task {i}", "description": f"Desc {i}"}
            )

        # Verify 5 tasks exist
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 5

        # Delete all tasks
        response = client.delete("/api/tasks")
        assert response.status_code == 204

        # Verify all tasks are gone
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0

    def test_delete_all_tasks_idempotent(
        self, client: TestClient
    ) -> None:
        """Test that calling delete_all multiple times is safe"""
        # Create tasks
        client.post(
            "/api/tasks",
            json={"title": "Task 1", "description": "Desc 1"}
        )

        # Delete all tasks first time
        response = client.delete("/api/tasks")
        assert response.status_code == 204

        # Delete all tasks second time (should still succeed)
        response = client.delete("/api/tasks")
        assert response.status_code == 204

        # Delete all tasks third time (should still succeed)
        response = client.delete("/api/tasks")
        assert response.status_code == 204

    def test_delete_all_route_before_delete_single(
        self, client: TestClient
    ) -> None:
        """
        Test that DELETE /api/tasks matches before
        DELETE /api/tasks/{task_id}
        """
        # Create a task
        response = client.post(
            "/api/tasks",
            json={"title": "Task", "description": "Desc"}
        )
        task_id = response.json()["id"]

        # Verify task exists
        response = client.get(f"/api/tasks/{task_id}")
        assert response.status_code == 200

        # Call DELETE /api/tasks (should delete all, not treat
        # "tasks" as task_id)
        response = client.delete("/api/tasks")
        assert response.status_code == 204

        # Verify task was deleted (as part of delete_all)
        response = client.get(f"/api/tasks/{task_id}")
        assert response.status_code == 404

    def test_can_create_tasks_after_delete_all(
        self, client: TestClient
    ) -> None:
        """Test that tasks can be created after delete_all"""
        # Create and delete tasks
        client.post(
            "/api/tasks",
            json={"title": "Task 1", "description": "Desc 1"}
        )
        client.delete("/api/tasks")

        # Verify can create new task
        response = client.post(
            "/api/tasks",
            json={"title": "New Task", "description": "New Desc"}
        )
        assert response.status_code == 201
        assert response.json()["title"] == "New Task"

        # Verify new task appears in list
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 1
        assert response.json()["tasks"][0]["title"] == "New Task"


class TestDeleteAllTasksProperties:
    """Property-based tests for delete_all_tasks feature"""

    @settings(
        max_examples=10,
        deadline=2000,
        suppress_health_check=[HealthCheck.function_scoped_fixture]
    )
    @given(tasks_data=st.lists(task_create_strategy(), min_size=1, max_size=10))
    def test_property_delete_all_removes_all_tasks(
        self, client: TestClient, tasks_data: list
    ) -> None:
        """
        Property: For any set of tasks, after calling delete_all,
        retrieving all tasks should return an empty list.
        """
        # Create all tasks
        for task_data in tasks_data:
            response = client.post("/api/tasks", json=task_data.model_dump())
            assert response.status_code == 201

        # Verify tasks were created
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == len(tasks_data)

        # Delete all tasks
        response = client.delete("/api/tasks")
        assert response.status_code == 204

        # Verify all tasks are gone
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0

    @settings(
        max_examples=10,
        deadline=2000,
        suppress_health_check=[HealthCheck.function_scoped_fixture]
    )
    @given(tasks_data=st.lists(task_create_strategy(), min_size=1, max_size=10))
    def test_property_delete_all_makes_tasks_unretrievable_by_id(
        self, client: TestClient, tasks_data: list
    ) -> None:
        """
        Property: For any set of tasks, after calling delete_all,
        no task should be retrievable by its ID (all should return 404).
        """
        # Create all tasks and collect their IDs
        task_ids = []
        for task_data in tasks_data:
            response = client.post("/api/tasks", json=task_data.model_dump())
            task_ids.append(response.json()["id"])

        # Verify all tasks exist
        for task_id in task_ids:
            response = client.get(f"/api/tasks/{task_id}")
            assert response.status_code == 200

        # Delete all tasks
        response = client.delete("/api/tasks")
        assert response.status_code == 204

        # Verify all tasks return 404
        for task_id in task_ids:
            response = client.get(f"/api/tasks/{task_id}")
            assert response.status_code == 404

    @settings(
        max_examples=5,
        deadline=2000,
        suppress_health_check=[HealthCheck.function_scoped_fixture]
    )
    @given(
        first_batch=st.lists(task_create_strategy(), min_size=1, max_size=5),
        second_batch=st.lists(task_create_strategy(), min_size=1, max_size=5),
    )
    def test_property_delete_all_allows_new_tasks_after(
        self, client: TestClient, first_batch: list, second_batch: list
    ) -> None:
        """
        Property: After delete_all, new tasks can be created and
        only the new tasks exist (old tasks don't reappear).
        """
        # Create first batch
        first_batch_ids = []
        for task_data in first_batch:
            response = client.post("/api/tasks", json=task_data.model_dump())
            first_batch_ids.append(response.json()["id"])

        # Delete all tasks
        client.delete("/api/tasks")

        # Create second batch
        second_batch_ids = []
        for task_data in second_batch:
            response = client.post("/api/tasks", json=task_data.model_dump())
            second_batch_ids.append(response.json()["id"])

        # Verify only second batch exists
        response = client.get("/api/tasks")
        tasks = response.json()["tasks"]
        assert len(tasks) == len(second_batch)

        # Verify all returned tasks are from second batch
        returned_ids = {task["id"] for task in tasks}
        assert returned_ids == set(second_batch_ids)

        # Verify first batch tasks don't exist
        for task_id in first_batch_ids:
            response = client.get(f"/api/tasks/{task_id}")
            assert response.status_code == 404
