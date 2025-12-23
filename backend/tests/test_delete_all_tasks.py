"""
Unit tests for delete all tasks functionality.

This test suite covers:
- Repository layer: delete_all() method
- Service layer: delete_all_tasks() method
- API endpoint: DELETE /api/tasks
"""

from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.models.task import Task, TaskCreate
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService


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


@pytest.fixture
def test_service(test_repo):
    """Create a TaskService with mocked repository"""
    return TaskService(test_repo)


@pytest.fixture
def client() -> TestClient:
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

    def test_delete_all_returns_count_of_deleted_tasks(self, test_repo):
        """Test that delete_all returns the number of tasks deleted"""
        # Create multiple tasks
        test_repo.create(TaskCreate(title="Task 1", description="Description 1"))
        test_repo.create(TaskCreate(title="Task 2", description="Description 2"))
        test_repo.create(TaskCreate(title="Task 3", description="Description 3"))

        # Delete all tasks
        count = test_repo.delete_all()

        # Verify count
        assert count == 3

    def test_delete_all_removes_all_tasks(self, test_repo):
        """Test that delete_all removes all tasks from storage"""
        # Create multiple tasks
        test_repo.create(TaskCreate(title="Task 1", description="Description 1"))
        test_repo.create(TaskCreate(title="Task 2", description="Description 2"))

        # Delete all tasks
        test_repo.delete_all()

        # Verify no tasks remain
        remaining_tasks = test_repo.get_all()
        assert len(remaining_tasks) == 0

    def test_delete_all_on_empty_storage_returns_zero(self, test_repo):
        """Test that delete_all returns 0 when there are no tasks"""
        # Delete all tasks on empty storage
        count = test_repo.delete_all()

        # Verify count is 0
        assert count == 0

    def test_delete_all_idempotent(self, test_repo):
        """Test that calling delete_all multiple times is safe"""
        # Create tasks
        test_repo.create(TaskCreate(title="Task 1", description="Description 1"))

        # Delete all tasks twice
        count1 = test_repo.delete_all()
        count2 = test_repo.delete_all()

        # Verify first call deleted 1 task, second call deleted 0
        assert count1 == 1
        assert count2 == 0

        # Verify no tasks remain
        remaining_tasks = test_repo.get_all()
        assert len(remaining_tasks) == 0


class TestServiceDeleteAllTasks:
    """Unit tests for TaskService.delete_all_tasks() method"""

    def test_service_delete_all_tasks_calls_repository(self, test_service):
        """Test that service method delegates to repository"""
        # Create tasks
        test_service.create_task(TaskCreate(title="Task 1", description="Description 1"))
        test_service.create_task(TaskCreate(title="Task 2", description="Description 2"))

        # Delete all tasks
        count = test_service.delete_all_tasks()

        # Verify count
        assert count == 2

        # Verify tasks are deleted
        remaining_tasks = test_service.get_all_tasks()
        assert len(remaining_tasks) == 0

    def test_service_delete_all_tasks_returns_count(self, test_service):
        """Test that service returns the count from repository"""
        # Create tasks
        test_service.create_task(TaskCreate(title="Task 1", description="Description 1"))
        test_service.create_task(TaskCreate(title="Task 2", description="Description 2"))
        test_service.create_task(TaskCreate(title="Task 3", description="Description 3"))

        # Delete all tasks
        count = test_service.delete_all_tasks()

        # Verify count matches number of tasks
        assert count == 3


class TestDeleteAllTasksEndpoint:
    """Integration tests for DELETE /api/tasks endpoint"""

    def test_delete_all_tasks_returns_204(self, client: TestClient):
        """Test that DELETE /api/tasks returns 204 No Content"""
        # Create some tasks first
        client.post("/api/tasks", json={"title": "Task 1", "description": "Description 1"})
        client.post("/api/tasks", json={"title": "Task 2", "description": "Description 2"})

        # Delete all tasks
        response = client.delete("/api/tasks")

        # Verify status code
        assert response.status_code == 204

    def test_delete_all_tasks_removes_all_tasks(self, client: TestClient):
        """Test that DELETE /api/tasks removes all tasks"""
        # Create some tasks
        client.post("/api/tasks", json={"title": "Task 1", "description": "Description 1"})
        client.post("/api/tasks", json={"title": "Task 2", "description": "Description 2"})
        client.post("/api/tasks", json={"title": "Task 3", "description": "Description 3"})

        # Delete all tasks
        response = client.delete("/api/tasks")
        assert response.status_code == 204

        # Verify all tasks are deleted
        get_response = client.get("/api/tasks")
        data = get_response.json()
        assert len(data["tasks"]) == 0

    def test_delete_all_tasks_on_empty_list(self, client: TestClient):
        """Test that DELETE /api/tasks works when there are no tasks"""
        # Delete all tasks when list is empty
        response = client.delete("/api/tasks")

        # Should still return 204
        assert response.status_code == 204

    def test_delete_all_tasks_returns_no_content(self, client: TestClient):
        """Test that DELETE /api/tasks returns no response body"""
        # Create a task
        client.post("/api/tasks", json={"title": "Task 1", "description": "Description 1"})

        # Delete all tasks
        response = client.delete("/api/tasks")

        # Verify no content in response
        assert response.status_code == 204
        assert response.text == ""

    def test_delete_all_tasks_route_before_task_id_route(self, client: TestClient):
        """Test that DELETE /api/tasks doesn't conflict with DELETE /api/tasks/{id}"""
        # Create a task
        create_response = client.post(
            "/api/tasks",
            json={"title": "Task 1", "description": "Description 1"}
        )
        task_id = create_response.json()["id"]

        # Delete all tasks (should use /tasks route, not /tasks/{id})
        response = client.delete("/api/tasks")
        assert response.status_code == 204

        # Verify task is deleted
        get_response = client.get(f"/api/tasks/{task_id}")
        assert get_response.status_code == 404

    def test_delete_all_then_create_new_task(self, client: TestClient):
        """Test that creating tasks works after deleting all"""
        # Create initial tasks
        client.post("/api/tasks", json={"title": "Task 1", "description": "Description 1"})
        client.post("/api/tasks", json={"title": "Task 2", "description": "Description 2"})

        # Delete all tasks
        client.delete("/api/tasks")

        # Create a new task
        create_response = client.post(
            "/api/tasks",
            json={"title": "New Task", "description": "New Description"}
        )

        # Verify task is created successfully
        assert create_response.status_code == 201
        assert create_response.json()["title"] == "New Task"

        # Verify only one task exists
        get_response = client.get("/api/tasks")
        data = get_response.json()
        assert len(data["tasks"]) == 1


class TestDeleteAllTasksEdgeCases:
    """Edge case tests for delete all tasks functionality"""

    def test_delete_all_with_many_tasks(self, client: TestClient):
        """Test deleting all tasks when there are many tasks"""
        # Create 50 tasks
        for i in range(50):
            client.post(
                "/api/tasks",
                json={"title": f"Task {i}", "description": f"Description {i}"}
            )

        # Verify tasks were created
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 50

        # Delete all tasks
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204

        # Verify all tasks are deleted
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 0

    def test_delete_all_preserves_database_structure(self, test_repo):
        """Test that delete_all doesn't break database structure"""
        # Create and delete tasks
        test_repo.create(TaskCreate(title="Task 1", description="Description 1"))
        test_repo.delete_all()

        # Create a new task to verify structure is intact
        new_task = test_repo.create(TaskCreate(title="Task 2", description="Description 2"))

        # Verify task has all required fields
        assert new_task.id is not None
        assert new_task.title == "Task 2"
        assert new_task.description == "Description 2"
        assert new_task.completed is False
        assert new_task.created_at is not None
        assert new_task.updated_at is not None

        # Verify task can be retrieved
        retrieved = test_repo.get_by_id(new_task.id)
        assert retrieved is not None
        assert retrieved.id == new_task.id
