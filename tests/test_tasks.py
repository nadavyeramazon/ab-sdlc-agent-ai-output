"""
Tests for task management endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_tasks():
    """Clear tasks before each test."""
    from app.api.v1.endpoints.tasks import tasks_db
    tasks_db.clear()
    yield
    tasks_db.clear()


def test_create_task():
    """Test creating a new task."""
    response = client.post(
        "/api/v1/tasks",
        json={"title": "Test Task", "description": "Test description", "status": "pending"}
    )
    assert response.status_code == 201
    
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test description"
    assert data["status"] == "pending"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_create_task_minimal():
    """Test creating a task with minimal data."""
    response = client.post(
        "/api/v1/tasks",
        json={"title": "Minimal Task"}
    )
    assert response.status_code == 201
    
    data = response.json()
    assert data["title"] == "Minimal Task"
    assert data["status"] == "pending"


def test_create_task_invalid_status():
    """Test creating a task with invalid status."""
    response = client.post(
        "/api/v1/tasks",
        json={"title": "Test", "status": "invalid_status"}
    )
    assert response.status_code == 422


def test_list_tasks_empty():
    """Test listing tasks when none exist."""
    response = client.get("/api/v1/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks():
    """Test listing tasks."""
    # Create a few tasks
    client.post("/api/v1/tasks", json={"title": "Task 1"})
    client.post("/api/v1/tasks", json={"title": "Task 2"})
    client.post("/api/v1/tasks", json={"title": "Task 3"})
    
    response = client.get("/api/v1/tasks")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 3
    assert all(isinstance(task, dict) for task in data)


def test_list_tasks_with_filter():
    """Test listing tasks with status filter."""
    # Create tasks with different statuses
    client.post("/api/v1/tasks", json={"title": "Task 1", "status": "pending"})
    client.post("/api/v1/tasks", json={"title": "Task 2", "status": "completed"})
    client.post("/api/v1/tasks", json={"title": "Task 3", "status": "pending"})
    
    response = client.get("/api/v1/tasks?status=pending")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 2
    assert all(task["status"] == "pending" for task in data)


def test_get_task():
    """Test getting a specific task."""
    # Create a task
    create_response = client.post(
        "/api/v1/tasks",
        json={"title": "Test Task"}
    )
    task_id = create_response.json()["id"]
    
    # Get the task
    response = client.get(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Test Task"


def test_get_task_not_found():
    """Test getting a non-existent task."""
    response = client.get("/api/v1/tasks/nonexistent-id")
    assert response.status_code == 404


def test_update_task():
    """Test updating a task."""
    # Create a task
    create_response = client.post(
        "/api/v1/tasks",
        json={"title": "Original Title", "status": "pending"}
    )
    task_id = create_response.json()["id"]
    
    # Update the task
    response = client.put(
        f"/api/v1/tasks/{task_id}",
        json={"title": "Updated Title", "status": "completed"}
    )
    assert response.status_code == 200
    
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["status"] == "completed"


def test_update_task_partial():
    """Test partial update of a task."""
    # Create a task
    create_response = client.post(
        "/api/v1/tasks",
        json={"title": "Original Title", "status": "pending"}
    )
    task_id = create_response.json()["id"]
    
    # Update only the status
    response = client.put(
        f"/api/v1/tasks/{task_id}",
        json={"status": "in_progress"}
    )
    assert response.status_code == 200
    
    data = response.json()
    assert data["title"] == "Original Title"
    assert data["status"] == "in_progress"


def test_update_task_not_found():
    """Test updating a non-existent task."""
    response = client.put(
        "/api/v1/tasks/nonexistent-id",
        json={"title": "Updated"}
    )
    assert response.status_code == 404


def test_delete_task():
    """Test deleting a task."""
    # Create a task
    create_response = client.post(
        "/api/v1/tasks",
        json={"title": "To Delete"}
    )
    task_id = create_response.json()["id"]
    
    # Delete the task
    response = client.delete(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 204
    
    # Verify it's gone
    get_response = client.get(f"/api/v1/tasks/{task_id}")
    assert get_response.status_code == 404


def test_delete_task_not_found():
    """Test deleting a non-existent task."""
    response = client.delete("/api/v1/tasks/nonexistent-id")
    assert response.status_code == 404


def test_task_pagination():
    """Test task list pagination."""
    # Create multiple tasks
    for i in range(10):
        client.post("/api/v1/tasks", json={"title": f"Task {i}"})
    
    # Get first page
    response = client.get("/api/v1/tasks?limit=5&offset=0")
    assert response.status_code == 200
    assert len(response.json()) == 5
    
    # Get second page
    response = client.get("/api/v1/tasks?limit=5&offset=5")
    assert response.status_code == 200
    assert len(response.json()) == 5
