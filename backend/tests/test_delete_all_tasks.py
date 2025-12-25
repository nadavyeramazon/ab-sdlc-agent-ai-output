"""
Unit and integration tests for delete all tasks functionality.

This test suite covers the DELETE /api/tasks endpoint for deleting all tasks.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.models.task import Task, TaskCreate


# Mock task storage
mock_tasks = {}


def create_mock_repository():
    """Create a mock repository with in-memory storage"""
    from app.repositories.task_repository import TaskRepository

    repo = TaskRepository.__new__(TaskRepository)
    repo.db_config = {}

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


@pytest.fixture
def client():
    """Create a TestClient instance for testing FastAPI endpoints."""
    global mock_tasks
    mock_tasks = {}

    mock_repo = create_mock_repository()

    from app.dependencies import get_task_repository
    test_app = create_app()
    test_app.dependency_overrides[get_task_repository] = lambda: mock_repo

    test_client = TestClient(test_app)
    yield test_client

    test_app.dependency_overrides.clear()
    mock_tasks = {}


class TestDeleteAllTasksEndpoint:
    """Unit tests for DELETE /api/tasks endpoint"""

    def test_delete_all_tasks_returns_204(self, client: TestClient):
        """Test that DELETE /api/tasks returns 204 No Content"""
        # Create some tasks first
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
        assert response.content == b""

    def test_delete_all_tasks_removes_all_tasks(self, client: TestClient):
        """Test that DELETE /api/tasks removes all tasks from database"""
        # Create multiple tasks
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
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 3

        # Delete all tasks
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204

        # Verify all tasks are deleted
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 0

    def test_delete_all_tasks_when_empty(self, client: TestClient):
        """Test that DELETE /api/tasks works when no tasks exist"""
        # Verify no tasks exist
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 0

        # Delete all tasks (should succeed even when empty)
        response = client.delete("/api/tasks")
        assert response.status_code == 204

    def test_delete_all_tasks_idempotency(self, client: TestClient):
        """Test that DELETE /api/tasks is idempotent"""
        # Create tasks
        client.post(
            "/api/tasks",
            json={"title": "Task 1", "description": "Description 1"}
        )
        client.post(
            "/api/tasks",
            json={"title": "Task 2", "description": "Description 2"}
        )

        # Delete all tasks first time
        response1 = client.delete("/api/tasks")
        assert response1.status_code == 204

        # Delete all tasks second time (should succeed)
        response2 = client.delete("/api/tasks")
        assert response2.status_code == 204

        # Verify no tasks exist
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 0

    def test_delete_all_tasks_can_create_after(self, client: TestClient):
        """Test that tasks can be created after DELETE /api/tasks"""
        # Create and delete tasks
        client.post(
            "/api/tasks",
            json={"title": "Task 1", "description": "Description 1"}
        )
        client.delete("/api/tasks")

        # Create new task after deletion
        create_response = client.post(
            "/api/tasks",
            json={"title": "New Task", "description": "New Description"}
        )
        assert create_response.status_code == 201

        # Verify new task exists
        get_response = client.get("/api/tasks")
        tasks = get_response.json()["tasks"]
        assert len(tasks) == 1
        assert tasks[0]["title"] == "New Task"

    def test_delete_all_tasks_cors_headers(self, client: TestClient):
        """Test that DELETE /api/tasks includes CORS headers"""
        response = client.delete(
            "/api/tasks",
            headers={"Origin": "http://localhost:3000"}
        )

        assert response.status_code == 204
        assert "access-control-allow-origin" in response.headers

    def test_delete_all_tasks_content_type(self, client: TestClient):
        """Test that DELETE /api/tasks returns no content type"""
        client.post(
            "/api/tasks",
            json={"title": "Task 1", "description": "Description 1"}
        )

        response = client.delete("/api/tasks")

        assert response.status_code == 204
        # 204 responses typically have no content-type or empty content
        assert response.content == b""

    def test_delete_all_tasks_with_various_task_states(self, client: TestClient):
        """Test that DELETE /api/tasks deletes tasks in all states"""
        # Create tasks with different states
        client.post(
            "/api/tasks",
            json={"title": "Incomplete Task", "description": "Not done"}
        )

        task2 = client.post(
            "/api/tasks",
            json={"title": "Complete Task", "description": "Done"}
        )
        task2_id = task2.json()["id"]

        # Mark one task as completed
        client.put(f"/api/tasks/{task2_id}", json={"completed": True})

        # Verify both tasks exist with different states
        get_response = client.get("/api/tasks")
        tasks = get_response.json()["tasks"]
        assert len(tasks) == 2

        # Delete all tasks
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204

        # Verify both tasks are deleted
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 0

    def test_delete_all_tasks_large_dataset(self, client: TestClient):
        """Test that DELETE /api/tasks handles large datasets efficiently"""
        # Create many tasks
        for i in range(50):
            client.post(
                "/api/tasks",
                json={"title": f"Task {i}", "description": f"Desc {i}"}
            )

        # Verify all tasks created
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 50

        # Delete all tasks
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204

        # Verify all deleted
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 0

    def test_delete_all_tasks_wrong_method(self, client: TestClient):
        """Test that only DELETE method is allowed on /api/tasks"""
        # GET should work (returns list)
        get_response = client.get("/api/tasks")
        assert get_response.status_code == 200

        # POST should work (creates task)
        post_response = client.post(
            "/api/tasks",
            json={"title": "Task", "description": "Desc"}
        )
        assert post_response.status_code == 201

        # PUT should return 405 (not allowed on collection)
        put_response = client.put("/api/tasks", json={"title": "Updated"})
        assert put_response.status_code == 405


class TestDeleteAllTasksService:
    """Unit tests for service layer delete_all_tasks method"""

    def test_service_delete_all_returns_count(self):
        """Test that service layer returns count of deleted tasks"""
        from app.services.task_service import TaskService

        global mock_tasks
        mock_tasks = {}

        mock_repo = create_mock_repository()
        service = TaskService(mock_repo)

        # Create tasks
        service.create_task(TaskCreate(title="Task 1", description="Desc 1"))
        service.create_task(TaskCreate(title="Task 2", description="Desc 2"))
        service.create_task(TaskCreate(title="Task 3", description="Desc 3"))

        # Delete all and verify count
        count = service.delete_all_tasks()
        assert count == 3

        # Verify all deleted
        assert len(service.get_all_tasks()) == 0

        mock_tasks = {}

    def test_service_delete_all_when_empty(self):
        """Test that service layer handles empty database correctly"""
        from app.services.task_service import TaskService

        global mock_tasks
        mock_tasks = {}

        mock_repo = create_mock_repository()
        service = TaskService(mock_repo)

        # Delete all when empty
        count = service.delete_all_tasks()
        assert count == 0

        mock_tasks = {}


class TestDeleteAllTasksRepository:
    """Unit tests for repository layer delete_all method"""

    def test_repository_delete_all_returns_count(self):
        """Test that repository layer returns count of deleted rows"""
        global mock_tasks
        mock_tasks = {}

        repo = create_mock_repository()

        # Create tasks
        repo.create(TaskCreate(title="Task 1", description="Desc 1"))
        repo.create(TaskCreate(title="Task 2", description="Desc 2"))

        # Delete all
        count = repo.delete_all()
        assert count == 2

        mock_tasks = {}

    def test_repository_delete_all_empties_storage(self):
        """Test that repository layer empties storage completely"""
        global mock_tasks
        mock_tasks = {}

        repo = create_mock_repository()

        # Create tasks
        repo.create(TaskCreate(title="Task 1", description="Desc 1"))
        repo.create(TaskCreate(title="Task 2", description="Desc 2"))
        repo.create(TaskCreate(title="Task 3", description="Desc 3"))

        # Verify tasks exist
        assert len(repo.get_all()) == 3

        # Delete all
        repo.delete_all()

        # Verify empty
        assert len(repo.get_all()) == 0

        mock_tasks = {}


class TestDeleteAllTasksIntegration:
    """Integration tests for delete all functionality across all layers"""

    def test_full_workflow_create_delete_all_create(self, client: TestClient):
        """Test complete workflow: create -> delete all -> create again"""
        # Step 1: Create initial tasks
        task1 = client.post(
            "/api/tasks",
            json={"title": "First Batch Task 1", "description": "Desc 1"}
        )
        task2 = client.post(
            "/api/tasks",
            json={"title": "First Batch Task 2", "description": "Desc 2"}
        )
        assert task1.status_code == 201
        assert task2.status_code == 201

        # Step 2: Verify tasks exist
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 2

        # Step 3: Delete all tasks
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204

        # Step 4: Verify no tasks exist
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 0

        # Step 5: Create new batch of tasks
        task3 = client.post(
            "/api/tasks",
            json={"title": "Second Batch Task 1", "description": "New Desc 1"}
        )
        task4 = client.post(
            "/api/tasks",
            json={"title": "Second Batch Task 2", "description": "New Desc 2"}
        )
        assert task3.status_code == 201
        assert task4.status_code == 201

        # Step 6: Verify new tasks exist and old ones don't
        get_response = client.get("/api/tasks")
        tasks = get_response.json()["tasks"]
        assert len(tasks) == 2
        assert all("Second Batch" in task["title"] for task in tasks)
        assert all("First Batch" not in task["title"] for task in tasks)
