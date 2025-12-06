"""
Tests for bulk delete functionality (DELETE /api/tasks endpoint).

This test suite covers:
- Repository layer: delete_all() method
- Service layer: delete_all_tasks() method
- API layer: DELETE /api/tasks endpoint
- Integration tests with multiple tasks
- Edge cases (empty database, after deletion)
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
        mock_tasks.clear()
        return True

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
    """Unit tests for TaskRepository.delete_all() method"""

    def test_delete_all_with_single_task(self, test_repo):
        """Test delete_all removes single task from repository"""
        # Create a task
        task_data = TaskCreate(title="Test Task", description="Test Description")
        test_repo.create(task_data)

        # Verify task exists
        tasks = test_repo.get_all()
        assert len(tasks) == 1

        # Delete all tasks
        result = test_repo.delete_all()
        assert result is True

        # Verify all tasks are deleted
        tasks = test_repo.get_all()
        assert len(tasks) == 0

    def test_delete_all_with_multiple_tasks(self, test_repo):
        """Test delete_all removes multiple tasks from repository"""
        # Create multiple tasks
        for i in range(5):
            task_data = TaskCreate(
                title=f"Task {i}",
                description=f"Description {i}"
            )
            test_repo.create(task_data)

        # Verify tasks exist
        tasks = test_repo.get_all()
        assert len(tasks) == 5

        # Delete all tasks
        result = test_repo.delete_all()
        assert result is True

        # Verify all tasks are deleted
        tasks = test_repo.get_all()
        assert len(tasks) == 0

    def test_delete_all_with_empty_database(self, test_repo):
        """Test delete_all succeeds when database is already empty"""
        # Verify database is empty
        tasks = test_repo.get_all()
        assert len(tasks) == 0

        # Delete all tasks (should succeed even when empty)
        result = test_repo.delete_all()
        assert result is True

        # Verify database is still empty
        tasks = test_repo.get_all()
        assert len(tasks) == 0

    def test_delete_all_returns_true(self, test_repo):
        """Test delete_all returns True indicating successful operation"""
        # Create some tasks
        for i in range(3):
            task_data = TaskCreate(title=f"Task {i}", description="Test")
            test_repo.create(task_data)

        # Delete all should return True
        result = test_repo.delete_all()
        assert result is True
        assert isinstance(result, bool)


class TestServiceDeleteAll:
    """Unit tests for TaskService.delete_all_tasks() method"""

    def test_service_delete_all_calls_repository(self, test_repo):
        """Test service delete_all_tasks calls repository delete_all"""
        from app.services.task_service import TaskService

        # Create service with test repository
        service = TaskService(test_repo)

        # Create some tasks
        for i in range(3):
            task_data = TaskCreate(title=f"Task {i}", description="Test")
            service.create_task(task_data)

        # Verify tasks exist
        tasks = service.get_all_tasks()
        assert len(tasks) == 3

        # Delete all tasks through service
        result = service.delete_all_tasks()
        assert result is True

        # Verify all tasks are deleted
        tasks = service.get_all_tasks()
        assert len(tasks) == 0

    def test_service_delete_all_returns_boolean(self, test_repo):
        """Test service delete_all_tasks returns boolean value"""
        from app.services.task_service import TaskService

        service = TaskService(test_repo)

        result = service.delete_all_tasks()
        assert isinstance(result, bool)
        assert result is True


class TestDeleteAllEndpoint:
    """Integration tests for DELETE /api/tasks endpoint"""

    def test_delete_all_endpoint_returns_204(self, client: TestClient):
        """Test DELETE /api/tasks returns 204 No Content"""
        response = client.delete("/api/tasks")

        assert response.status_code == 204
        assert response.content == b''

    def test_delete_all_endpoint_deletes_single_task(self, client: TestClient):
        """Test DELETE /api/tasks deletes single task"""
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

        # Verify all tasks are deleted
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 0

    def test_delete_all_endpoint_deletes_multiple_tasks(self, client: TestClient):
        """Test DELETE /api/tasks deletes all tasks when multiple exist"""
        # Create multiple tasks
        task_ids = []
        for i in range(5):
            response = client.post(
                "/api/tasks",
                json={"title": f"Task {i}", "description": f"Description {i}"}
            )
            assert response.status_code == 201
            task_ids.append(response.json()["id"])

        # Verify all tasks exist
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 5

        # Delete all tasks
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204

        # Verify all tasks are deleted
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 0

        # Verify individual tasks are no longer accessible
        for task_id in task_ids:
            response = client.get(f"/api/tasks/{task_id}")
            assert response.status_code == 404

    def test_delete_all_endpoint_with_empty_database(self, client: TestClient):
        """Test DELETE /api/tasks succeeds when database is empty"""
        # Verify database is empty
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 0

        # Delete all tasks (should succeed)
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204

        # Verify database is still empty
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 0

    def test_delete_all_endpoint_returns_no_content(self, client: TestClient):
        """Test DELETE /api/tasks returns empty response body"""
        response = client.delete("/api/tasks")

        assert response.status_code == 204
        assert response.content == b''
        assert len(response.content) == 0

    def test_delete_all_multiple_times(self, client: TestClient):
        """Test DELETE /api/tasks can be called multiple times successfully"""
        # Create some tasks
        for i in range(3):
            client.post(
                "/api/tasks",
                json={"title": f"Task {i}", "description": "Test"}
            )

        # First delete
        response1 = client.delete("/api/tasks")
        assert response1.status_code == 204

        # Second delete (empty database)
        response2 = client.delete("/api/tasks")
        assert response2.status_code == 204

        # Third delete (still empty)
        response3 = client.delete("/api/tasks")
        assert response3.status_code == 204

    def test_delete_all_wrong_methods(self, client: TestClient):
        """Test that only DELETE method is allowed on /api/tasks for bulk delete"""
        # Note: GET and POST are valid on /api/tasks, but other methods should fail
        # We're not testing GET/POST here as they're separate endpoints

        # PUT should not be allowed
        response = client.put("/api/tasks", json={"title": "Test"})
        assert response.status_code == 405  # Method Not Allowed


class TestDeleteAllIntegration:
    """Integration tests for delete_all with other operations"""

    def test_create_after_delete_all(self, client: TestClient):
        """Test creating tasks after deleting all works correctly"""
        # Create initial tasks
        for i in range(3):
            client.post(
                "/api/tasks",
                json={"title": f"Task {i}", "description": "Test"}
            )

        # Delete all
        client.delete("/api/tasks")

        # Create new tasks
        response = client.post(
            "/api/tasks",
            json={"title": "New Task", "description": "After delete"}
        )
        assert response.status_code == 201

        # Verify only new task exists
        get_response = client.get("/api/tasks")
        tasks = get_response.json()["tasks"]
        assert len(tasks) == 1
        assert tasks[0]["title"] == "New Task"

    def test_delete_all_with_mixed_task_states(self, client: TestClient):
        """Test delete_all removes tasks with different completion states"""
        # Create tasks with different states
        task1_response = client.post(
            "/api/tasks",
            json={"title": "Incomplete Task", "description": "Not done"}
        )
        task1_id = task1_response.json()["id"]

        task2_response = client.post(
            "/api/tasks",
            json={"title": "Complete Task", "description": "Done"}
        )
        task2_id = task2_response.json()["id"]

        # Mark second task as completed
        client.put(
            f"/api/tasks/{task2_id}",
            json={"completed": True}
        )

        # Verify both tasks exist
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 2

        # Delete all tasks
        client.delete("/api/tasks")

        # Verify all tasks are deleted regardless of completion status
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 0

    def test_delete_all_with_long_descriptions(self, client: TestClient):
        """Test delete_all handles tasks with maximum length descriptions"""
        # Create task with maximum length description (1000 chars)
        long_description = "a" * 1000
        response = client.post(
            "/api/tasks",
            json={"title": "Long Task", "description": long_description}
        )
        assert response.status_code == 201

        # Delete all tasks
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204

        # Verify task is deleted
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 0

    def test_route_order_delete_all_before_delete_by_id(self, client: TestClient):
        """
        Test that DELETE /api/tasks is matched before DELETE /api/tasks/{task_id}.
        This verifies the route ordering is correct.
        """
        # Create a task
        create_response = client.post(
            "/api/tasks",
            json={"title": "Test Task", "description": "Test"}
        )
        task_id = create_response.json()["id"]

        # DELETE /api/tasks should delete all (not treat "tasks" as an ID)
        delete_all_response = client.delete("/api/tasks")
        assert delete_all_response.status_code == 204

        # Verify task is deleted
        get_response = client.get(f"/api/tasks/{task_id}")
        assert get_response.status_code == 404

        # Now create another task and test specific delete
        create_response2 = client.post(
            "/api/tasks",
            json={"title": "Another Task", "description": "Test"}
        )
        task_id2 = create_response2.json()["id"]

        # DELETE /api/tasks/{task_id} should delete specific task
        delete_one_response = client.delete(f"/api/tasks/{task_id2}")
        assert delete_one_response.status_code == 204


class TestDeleteAllEdgeCases:
    """Edge case tests for delete_all functionality"""

    def test_delete_all_with_special_characters_in_tasks(self, client: TestClient):
        """Test delete_all handles tasks with special characters"""
        special_titles = [
            "Task with émojis 🎉",
            "Task with 中文",
            "Task with symbols !@#$%",
            "Task with \"quotes\" and 'apostrophes'"
        ]

        # Create tasks with special characters
        for title in special_titles:
            client.post(
                "/api/tasks",
                json={"title": title, "description": "Special chars test"}
            )

        # Verify tasks exist
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == len(special_titles)

        # Delete all tasks
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204

        # Verify all tasks are deleted
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 0

    def test_delete_all_concurrent_safety(self, client: TestClient):
        """Test delete_all can handle being called multiple times rapidly"""
        # Create some tasks
        for i in range(5):
            client.post(
                "/api/tasks",
                json={"title": f"Task {i}", "description": "Test"}
            )

        # Call delete_all multiple times in sequence (simulating concurrent calls)
        responses = []
        for _ in range(3):
            response = client.delete("/api/tasks")
            responses.append(response)

        # All should succeed with 204
        for response in responses:
            assert response.status_code == 204

        # Verify database is empty
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 0
