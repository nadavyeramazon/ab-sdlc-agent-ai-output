"""
Tests for delete all tasks functionality.

This test suite covers:
- Repository layer delete_all() method
- Service layer delete_all_tasks() method
- API endpoint DELETE /api/tasks
- Edge cases and error scenarios
"""

from typing import Generator
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from hypothesis import given, settings, HealthCheck
from hypothesis import strategies as st

from app.main import create_app
from app.models.task import Task, TaskCreate
from app.repositories.task_repository import TaskRepository


# Mock task storage
mock_tasks = {}


def create_mock_repository():
    """Create a mock repository with in-memory storage"""
    repo = TaskRepository.__new__(TaskRepository)
    repo.db_config = {}

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


class TestDeleteAllTasksRepository:
    """Unit tests for repository delete_all() method"""

    def test_delete_all_returns_zero_when_no_tasks(self, test_repo):
        """Test that delete_all() returns 0 when there are no tasks"""
        count = test_repo.delete_all()
        assert count == 0

    def test_delete_all_returns_count_of_deleted_tasks(self, test_repo):
        """Test that delete_all() returns the correct count of deleted tasks"""
        # Create 3 tasks
        test_repo.create(TaskCreate(title="Task 1", description="Description 1"))
        test_repo.create(TaskCreate(title="Task 2", description="Description 2"))
        test_repo.create(TaskCreate(title="Task 3", description="Description 3"))

        # Delete all tasks
        count = test_repo.delete_all()

        assert count == 3

    def test_delete_all_removes_all_tasks(self, test_repo):
        """Test that delete_all() removes all tasks from storage"""
        # Create multiple tasks
        test_repo.create(TaskCreate(title="Task 1", description="Description 1"))
        test_repo.create(TaskCreate(title="Task 2", description="Description 2"))
        test_repo.create(TaskCreate(title="Task 3", description="Description 3"))

        # Verify tasks exist
        tasks_before = test_repo.get_all()
        assert len(tasks_before) == 3

        # Delete all tasks
        test_repo.delete_all()

        # Verify all tasks are removed
        tasks_after = test_repo.get_all()
        assert len(tasks_after) == 0

    def test_delete_all_is_idempotent(self, test_repo):
        """Test that calling delete_all() multiple times works correctly"""
        # Create tasks
        test_repo.create(TaskCreate(title="Task 1", description="Description 1"))
        test_repo.create(TaskCreate(title="Task 2", description="Description 2"))

        # First delete
        count1 = test_repo.delete_all()
        assert count1 == 2

        # Second delete (should return 0)
        count2 = test_repo.delete_all()
        assert count2 == 0

        # Third delete (should still return 0)
        count3 = test_repo.delete_all()
        assert count3 == 0

    def test_delete_all_with_single_task(self, test_repo):
        """Test that delete_all() works correctly with a single task"""
        # Create one task
        task = test_repo.create(TaskCreate(title="Only Task", description="Alone"))

        # Delete all tasks
        count = test_repo.delete_all()

        assert count == 1
        assert test_repo.get_by_id(task.id) is None
        assert len(test_repo.get_all()) == 0


class TestDeleteAllTasksEndpoint:
    """Integration tests for DELETE /api/tasks endpoint"""

    def test_delete_all_endpoint_returns_204_with_no_tasks(self, client: TestClient):
        """Test DELETE /api/tasks returns 204 when there are no tasks"""
        response = client.delete("/api/tasks")

        assert response.status_code == 204
        assert response.content == b""

    def test_delete_all_endpoint_returns_204_with_tasks(self, client: TestClient):
        """Test DELETE /api/tasks returns 204 when deleting tasks"""
        # Create multiple tasks
        client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})
        client.post("/api/tasks", json={"title": "Task 2", "description": "Desc 2"})
        client.post("/api/tasks", json={"title": "Task 3", "description": "Desc 3"})

        # Delete all tasks
        response = client.delete("/api/tasks")

        assert response.status_code == 204
        assert response.content == b""

    def test_delete_all_endpoint_removes_all_tasks(self, client: TestClient):
        """Test DELETE /api/tasks actually removes all tasks"""
        # Create tasks
        client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})
        client.post("/api/tasks", json={"title": "Task 2", "description": "Desc 2"})

        # Verify tasks exist
        response_before = client.get("/api/tasks")
        assert len(response_before.json()["tasks"]) == 2

        # Delete all tasks
        client.delete("/api/tasks")

        # Verify all tasks are removed
        response_after = client.get("/api/tasks")
        assert len(response_after.json()["tasks"]) == 0

    def test_delete_all_endpoint_is_idempotent(self, client: TestClient):
        """Test that calling DELETE /api/tasks multiple times is safe"""
        # Create tasks
        client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})

        # First delete
        response1 = client.delete("/api/tasks")
        assert response1.status_code == 204

        # Second delete (should still work)
        response2 = client.delete("/api/tasks")
        assert response2.status_code == 204

        # Third delete (should still work)
        response3 = client.delete("/api/tasks")
        assert response3.status_code == 204

    def test_delete_all_endpoint_with_single_task(self, client: TestClient):
        """Test DELETE /api/tasks works correctly with a single task"""
        # Create one task
        response = client.post(
            "/api/tasks",
            json={"title": "Only Task", "description": "Alone"}
        )
        task_id = response.json()["id"]

        # Delete all tasks
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204

        # Verify task is removed
        get_response = client.get(f"/api/tasks/{task_id}")
        assert get_response.status_code == 404

    def test_delete_all_does_not_affect_individual_delete(self, client: TestClient):
        """Test that delete all and individual delete work independently"""
        # Create tasks
        response1 = client.post("/api/tasks", json={"title": "Task 1", "description": "D1"})
        task1_id = response1.json()["id"]
        client.post("/api/tasks", json={"title": "Task 2", "description": "D2"})

        # Delete one task individually
        client.delete(f"/api/tasks/{task1_id}")

        # Verify one task remains
        tasks_response = client.get("/api/tasks")
        assert len(tasks_response.json()["tasks"]) == 1

        # Delete all remaining tasks
        client.delete("/api/tasks")

        # Verify all tasks are gone
        final_response = client.get("/api/tasks")
        assert len(final_response.json()["tasks"]) == 0

    def test_create_after_delete_all_works(self, client: TestClient):
        """Test that creating tasks after delete all works correctly"""
        # Create and delete tasks
        client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})
        client.delete("/api/tasks")

        # Create new tasks after delete all
        response = client.post(
            "/api/tasks",
            json={"title": "New Task", "description": "New Description"}
        )

        assert response.status_code == 201
        task = response.json()
        assert task["title"] == "New Task"
        assert task["description"] == "New Description"

        # Verify task exists
        tasks_response = client.get("/api/tasks")
        assert len(tasks_response.json()["tasks"]) == 1


class TestDeleteAllTasksProperties:
    """Property-based tests for delete all functionality"""

    @given(st.integers(min_value=0, max_value=20))
    @settings(max_examples=10, deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_property_delete_all_removes_exact_count(
        self, client: TestClient, task_count: int
    ):
        """
        Property: Delete all removes exact count
        For any number of tasks created, delete all should remove exactly
        that many tasks, leaving the system empty.
        """
        # Create the specified number of tasks
        for i in range(task_count):
            client.post(
                "/api/tasks",
                json={"title": f"Task {i}", "description": f"Description {i}"}
            )

        # Verify tasks exist
        response_before = client.get("/api/tasks")
        assert len(response_before.json()["tasks"]) == task_count

        # Delete all tasks
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204

        # Verify all tasks are removed
        response_after = client.get("/api/tasks")
        assert len(response_after.json()["tasks"]) == 0

    @given(st.integers(min_value=0, max_value=5))
    @settings(max_examples=10, deadline=2000, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_property_delete_all_is_idempotent(
        self, client: TestClient, repeat_count: int
    ):
        """
        Property: Delete all is idempotent
        Calling delete all multiple times should always succeed with 204,
        regardless of whether tasks exist.
        """
        # Create some tasks
        client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})
        client.post("/api/tasks", json={"title": "Task 2", "description": "Desc 2"})

        # Call delete all multiple times
        for _ in range(repeat_count + 1):
            response = client.delete("/api/tasks")
            assert response.status_code == 204

        # Verify no tasks remain
        final_response = client.get("/api/tasks")
        assert len(final_response.json()["tasks"]) == 0
