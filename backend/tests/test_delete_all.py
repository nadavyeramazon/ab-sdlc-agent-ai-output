"""
Comprehensive tests for delete all tasks functionality.

This test suite covers:
- Repository layer delete_all method
- Service layer delete_all_tasks method
- API endpoint DELETE /api/tasks
- Edge cases and error scenarios
"""

from typing import Generator
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

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


class TestRepositoryDeleteAll:
    """Unit tests for TaskRepository.delete_all method"""

    def test_delete_all_returns_count_of_deleted_tasks(self, test_repo):
        """Test that delete_all returns the number of tasks deleted"""
        # Create some tasks
        test_repo.create(TaskCreate(title="Task 1", description="Description 1"))
        test_repo.create(TaskCreate(title="Task 2", description="Description 2"))
        test_repo.create(TaskCreate(title="Task 3", description="Description 3"))

        # Delete all tasks
        count = test_repo.delete_all()

        # Verify count
        assert count == 3

    def test_delete_all_removes_all_tasks(self, test_repo):
        """Test that delete_all removes all tasks from storage"""
        # Create some tasks
        test_repo.create(TaskCreate(title="Task 1", description="Description 1"))
        test_repo.create(TaskCreate(title="Task 2", description="Description 2"))

        # Delete all tasks
        test_repo.delete_all()

        # Verify no tasks remain
        all_tasks = test_repo.get_all()
        assert len(all_tasks) == 0

    def test_delete_all_on_empty_storage_returns_zero(self, test_repo):
        """Test that delete_all returns 0 when no tasks exist"""
        # Delete all tasks when storage is empty
        count = test_repo.delete_all()

        # Verify count is zero
        assert count == 0

    def test_delete_all_can_be_called_multiple_times(self, test_repo):
        """Test that delete_all can be called multiple times safely"""
        # Create tasks
        test_repo.create(TaskCreate(title="Task 1", description="Description 1"))

        # First delete
        count1 = test_repo.delete_all()
        assert count1 == 1

        # Second delete (on empty storage)
        count2 = test_repo.delete_all()
        assert count2 == 0

        # Verify still empty
        all_tasks = test_repo.get_all()
        assert len(all_tasks) == 0


class TestServiceDeleteAllTasks:
    """Unit tests for TaskService.delete_all_tasks method"""

    def test_delete_all_tasks_calls_repository_delete_all(self, test_repo):
        """Test that service correctly delegates to repository"""
        from app.services.task_service import TaskService

        service = TaskService(test_repo)

        # Create tasks
        test_repo.create(TaskCreate(title="Task 1", description="Description 1"))
        test_repo.create(TaskCreate(title="Task 2", description="Description 2"))

        # Delete all through service
        count = service.delete_all_tasks()

        # Verify count and that tasks are gone
        assert count == 2
        assert len(test_repo.get_all()) == 0


class TestDeleteAllTasksEndpoint:
    """Integration tests for DELETE /api/tasks endpoint"""

    def test_delete_all_tasks_endpoint_returns_204(self, client: TestClient):
        """Test that DELETE /api/tasks returns 204 No Content"""
        # Create some tasks
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

        # Verify tasks exist
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 3

        # Delete all tasks
        client.delete("/api/tasks")

        # Verify tasks are gone
        response = client.get("/api/tasks")
        assert response.status_code == 200
        assert len(response.json()["tasks"]) == 0

    def test_delete_all_tasks_on_empty_list(self, client: TestClient):
        """Test that DELETE /api/tasks works when no tasks exist"""
        # Verify no tasks exist
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0

        # Delete all tasks
        response = client.delete("/api/tasks")

        # Verify status code is still 204
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

    def test_delete_all_tasks_endpoint_idempotent(self, client: TestClient):
        """Test that calling DELETE /api/tasks multiple times is safe"""
        # Create tasks
        client.post("/api/tasks", json={"title": "Task 1", "description": "Description 1"})

        # First delete
        response1 = client.delete("/api/tasks")
        assert response1.status_code == 204

        # Second delete (no tasks remain)
        response2 = client.delete("/api/tasks")
        assert response2.status_code == 204

        # Verify still no tasks
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0


class TestDeleteAllTasksEdgeCases:
    """Edge case tests for delete all functionality"""

    def test_delete_all_after_individual_deletes(self, client: TestClient):
        """Test delete_all after some tasks already deleted individually"""
        # Create tasks
        response1 = client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})
        task1_id = response1.json()["id"]

        response2 = client.post("/api/tasks", json={"title": "Task 2", "description": "Desc 2"})
        task2_id = response2.json()["id"]

        client.post("/api/tasks", json={"title": "Task 3", "description": "Desc 3"})

        # Delete one task individually
        client.delete(f"/api/tasks/{task1_id}")

        # Verify 2 tasks remain
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 2

        # Delete all remaining tasks
        response = client.delete("/api/tasks")
        assert response.status_code == 204

        # Verify all gone
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0

        # Verify specific tasks are gone
        response = client.get(f"/api/tasks/{task1_id}")
        assert response.status_code == 404

        response = client.get(f"/api/tasks/{task2_id}")
        assert response.status_code == 404

    def test_create_after_delete_all(self, client: TestClient):
        """Test that tasks can be created after delete_all"""
        # Create and delete tasks
        client.post("/api/tasks", json={"title": "Task 1", "description": "Description 1"})
        client.delete("/api/tasks")

        # Create new task
        response = client.post("/api/tasks", json={"title": "New Task", "description": "New Desc"})
        assert response.status_code == 201

        # Verify task exists
        response = client.get("/api/tasks")
        tasks = response.json()["tasks"]
        assert len(tasks) == 1
        assert tasks[0]["title"] == "New Task"

    def test_delete_all_with_various_task_states(self, client: TestClient):
        """Test delete_all with tasks in different completion states"""
        # Create tasks with different states
        client.post("/api/tasks", json={"title": "Task 1", "description": "Incomplete"})

        response = client.post("/api/tasks", json={"title": "Task 2", "description": "Complete"})
        task2_id = response.json()["id"]
        client.put(f"/api/tasks/{task2_id}", json={"completed": True})

        client.post("/api/tasks", json={"title": "Task 3", "description": "Also incomplete"})

        # Verify mixed states
        response = client.get("/api/tasks")
        tasks = response.json()["tasks"]
        assert len(tasks) == 3
        assert any(t["completed"] for t in tasks)
        assert any(not t["completed"] for t in tasks)

        # Delete all
        response = client.delete("/api/tasks")
        assert response.status_code == 204

        # Verify all gone regardless of state
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0


class TestDeleteAllTasksErrorHandling:
    """Error handling tests for delete all functionality"""

    def test_delete_all_error_handling(self, client: TestClient):
        """Test that errors in delete_all are handled gracefully"""
        # Create app with mock that raises exception
        from app.dependencies import get_task_repository
        test_app = create_app()

        # Create mock repository that raises exception
        mock_repo = MagicMock()
        mock_repo.delete_all.side_effect = Exception("Database error")

        test_app.dependency_overrides[get_task_repository] = lambda: mock_repo

        test_client = TestClient(test_app)

        # Attempt to delete all tasks
        response = test_client.delete("/api/tasks")

        # Verify error response
        assert response.status_code == 500
        assert response.json()["detail"] == "Failed to delete tasks"

        # Cleanup
        test_app.dependency_overrides.clear()


class TestDeleteAllTasksIntegration:
    """Integration tests for complete delete all workflow"""

    def test_complete_workflow_with_delete_all(self, client: TestClient):
        """Test complete workflow: create, read, update, delete_all"""
        # Create multiple tasks
        task1 = client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})
        task2 = client.post("/api/tasks", json={"title": "Task 2", "description": "Desc 2"})
        task3 = client.post("/api/tasks", json={"title": "Task 3", "description": "Desc 3"})

        assert task1.status_code == 201
        assert task2.status_code == 201
        assert task3.status_code == 201

        # Read all tasks
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 3

        # Update one task
        task1_id = task1.json()["id"]
        update_response = client.put(
            f"/api/tasks/{task1_id}",
            json={"title": "Updated Task 1", "completed": True}
        )
        assert update_response.status_code == 200

        # Delete all tasks
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204

        # Verify all tasks are gone
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 0

        # Verify individual tasks return 404
        for task in [task1, task2, task3]:
            task_id = task.json()["id"]
            response = client.get(f"/api/tasks/{task_id}")
            assert response.status_code == 404
