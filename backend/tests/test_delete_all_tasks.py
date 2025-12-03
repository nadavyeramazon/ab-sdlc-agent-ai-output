"""
Tests for DELETE /api/tasks endpoint (bulk deletion).

This test suite covers:
- Unit tests for deleting all tasks
- Edge cases (empty list, multiple tasks)
- Integration with other endpoints
- Property-based tests for delete all functionality
"""

import pytest
from fastapi.testclient import TestClient
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from main import app


@pytest.fixture
def client():
    """
    Create a TestClient instance for testing FastAPI endpoints.
    This fixture is reused across all tests.
    """
    import os
    import shutil
    import tempfile

    import main
    from task_repository import TaskRepository

    # Create a temporary directory for test data
    temp_dir = tempfile.mkdtemp()
    test_data_file = os.path.join(temp_dir, "test_tasks.json")

    # Override the repository with test data file
    main._task_repository = TaskRepository(data_file=test_data_file)

    client = TestClient(app)

    yield client

    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)
    main._task_repository = None


class TestDeleteAllTasksEndpoint:
    """Unit tests for DELETE /api/tasks endpoint"""

    def test_delete_all_tasks_empty_list(self, client):
        """Test DELETE /api/tasks when task list is already empty"""
        # Clear all tasks first
        client.delete("/api/tasks")

        # Verify list is empty
        response = client.get("/api/tasks")
        assert response.status_code == 200
        assert response.json()["tasks"] == []

        # Delete all tasks (should work even on empty list)
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204

        # Verify list is still empty
        response = client.get("/api/tasks")
        assert response.status_code == 200
        assert response.json()["tasks"] == []

    def test_delete_all_tasks_single_task(self, client):
        """Test DELETE /api/tasks with a single task"""
        # Clear existing tasks
        client.delete("/api/tasks")

        # Create one task
        client.post("/api/tasks", json={"title": "Task 1", "description": "Description 1"})

        # Verify task was created
        response = client.get("/api/tasks")
        assert response.status_code == 200
        assert len(response.json()["tasks"]) == 1

        # Delete all tasks
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204

        # Verify list is empty
        response = client.get("/api/tasks")
        assert response.status_code == 200
        assert response.json()["tasks"] == []

    def test_delete_all_tasks_multiple_tasks(self, client):
        """Test DELETE /api/tasks with multiple tasks"""
        # Clear existing tasks
        client.delete("/api/tasks")

        # Create multiple tasks
        for i in range(5):
            client.post("/api/tasks", json={"title": f"Task {i}", "description": f"Description {i}"})

        # Verify tasks were created
        response = client.get("/api/tasks")
        assert response.status_code == 200
        assert len(response.json()["tasks"]) == 5

        # Delete all tasks
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204

        # Verify list is empty
        response = client.get("/api/tasks")
        assert response.status_code == 200
        assert response.json()["tasks"] == []

    def test_delete_all_tasks_response_has_no_body(self, client):
        """Test that DELETE /api/tasks returns no response body"""
        # Create some tasks
        client.post("/api/tasks", json={"title": "Task 1", "description": "Description 1"})

        # Delete all tasks
        response = client.delete("/api/tasks")
        assert response.status_code == 204
        # 204 No Content should have no body
        assert response.content == b""

    def test_delete_all_tasks_idempotent(self, client):
        """Test that DELETE /api/tasks is idempotent (can be called multiple times)"""
        # Create some tasks
        client.post("/api/tasks", json={"title": "Task 1", "description": "Description 1"})
        client.post("/api/tasks", json={"title": "Task 2", "description": "Description 2"})

        # Delete all tasks first time
        response1 = client.delete("/api/tasks")
        assert response1.status_code == 204

        # Verify list is empty
        response = client.get("/api/tasks")
        assert response.status_code == 200
        assert response.json()["tasks"] == []

        # Delete all tasks again (should succeed even though list is empty)
        response2 = client.delete("/api/tasks")
        assert response2.status_code == 204

        # Verify list is still empty
        response = client.get("/api/tasks")
        assert response.status_code == 200
        assert response.json()["tasks"] == []

    def test_delete_all_tasks_then_create_new(self, client):
        """Test that new tasks can be created after deleting all"""
        # Create some tasks
        client.post("/api/tasks", json={"title": "Task 1", "description": "Description 1"})
        client.post("/api/tasks", json={"title": "Task 2", "description": "Description 2"})

        # Delete all tasks
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204

        # Create new tasks
        create_response = client.post("/api/tasks", json={"title": "New Task", "description": "New Description"})
        assert create_response.status_code == 201

        # Verify new task exists
        response = client.get("/api/tasks")
        assert response.status_code == 200
        tasks = response.json()["tasks"]
        assert len(tasks) == 1
        assert tasks[0]["title"] == "New Task"

    def test_delete_all_tasks_different_from_delete_by_id(self, client):
        """Test that DELETE /api/tasks doesn't interfere with DELETE /api/tasks/{id}"""
        # Clear existing tasks
        client.delete("/api/tasks")

        # Create a task
        create_response = client.post("/api/tasks", json={"title": "Task 1", "description": "Description 1"})
        task_id = create_response.json()["id"]

        # Create another task
        client.post("/api/tasks", json={"title": "Task 2", "description": "Description 2"})

        # Verify we have 2 tasks
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 2

        # Delete by specific ID (not all)
        delete_by_id_response = client.delete(f"/api/tasks/{task_id}")
        assert delete_by_id_response.status_code == 204

        # Verify we have 1 task left
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 1

        # Now delete all
        delete_all_response = client.delete("/api/tasks")
        assert delete_all_response.status_code == 204

        # Verify list is empty
        response = client.get("/api/tasks")
        assert response.json()["tasks"] == []

    def test_delete_all_tasks_with_completed_and_incomplete(self, client):
        """Test DELETE /api/tasks removes both completed and incomplete tasks"""
        # Clear existing tasks
        client.delete("/api/tasks")

        # Create completed task
        create_response1 = client.post("/api/tasks", json={"title": "Completed Task", "description": "Done"})
        task_id1 = create_response1.json()["id"]
        client.put(f"/api/tasks/{task_id1}", json={"completed": True})

        # Create incomplete task
        client.post("/api/tasks", json={"title": "Incomplete Task", "description": "Not done"})

        # Verify we have 2 tasks
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 2

        # Delete all tasks
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204

        # Verify all tasks are deleted (both completed and incomplete)
        response = client.get("/api/tasks")
        assert response.json()["tasks"] == []

    def test_delete_all_tasks_method_not_allowed(self, client):
        """Test that other HTTP methods are not allowed on /api/tasks for deletion"""
        # POST is allowed for creating tasks (not tested here)
        # GET is allowed for retrieving tasks (not tested here)

        # PUT should not be allowed on /api/tasks without ID
        put_response = client.put("/api/tasks", json={"title": "Test"})
        # FastAPI will return 405 Method Not Allowed or 404 depending on routing
        assert put_response.status_code in [404, 405]

    def test_delete_all_tasks_no_trailing_slash(self, client):
        """Test DELETE /api/tasks/ (with trailing slash) behavior"""
        # Create a task
        client.post("/api/tasks", json={"title": "Task 1", "description": "Description 1"})

        # Try to delete with trailing slash (should fail since redirect_slashes=False)
        response = client.delete("/api/tasks/")
        # Should return 404 since redirect_slashes is disabled
        assert response.status_code == 404

        # Verify task still exists (delete didn't happen)
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 1


class TestDeleteAllTasksProperties:
    """Property-based tests for DELETE /api/tasks endpoint"""

    @given(
        st.lists(
            st.tuples(
                st.text(min_size=1).filter(lambda s: s.strip()),  # title (non-empty)
                st.text(max_size=1000),  # description
            ),
            min_size=0,
            max_size=20,
        )
    )
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_property_delete_all_removes_all_tasks(self, client, task_data_list):
        """
        **Feature: task-manager-app, Property: Delete all removes all tasks**
        **Validates: Bulk deletion functionality**

        For any set of tasks, when DELETE /api/tasks is called, all tasks
        should be removed from storage, and subsequent GET /api/tasks should
        return an empty list.
        """
        # Clear existing tasks
        client.delete("/api/tasks")

        # Create tasks from generated data
        created_task_ids = []
        for title, description in task_data_list:
            response = client.post("/api/tasks", json={"title": title.strip(), "description": description})
            if response.status_code == 201:
                task_id = response.json()["id"]
                created_task_ids.append(task_id)

        # Verify tasks were created
        if created_task_ids:
            get_response = client.get("/api/tasks")
            assert len(get_response.json()["tasks"]) == len(created_task_ids)

        # Delete all tasks
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204

        # Verify all tasks are deleted
        get_response = client.get("/api/tasks")
        assert get_response.status_code == 200
        assert get_response.json()["tasks"] == []

        # Verify each task ID no longer exists
        for task_id in created_task_ids:
            task_response = client.get(f"/api/tasks/{task_id}")
            assert task_response.status_code == 404

    @given(st.integers(min_value=0, max_value=50))
    @settings(max_examples=50, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_property_delete_all_count_invariant(self, client, num_tasks):
        """
        **Feature: task-manager-app, Property: Delete all count invariant**
        **Validates: Delete all works correctly regardless of task count**

        For any number of tasks N (including 0), after DELETE /api/tasks,
        GET /api/tasks should return exactly 0 tasks.
        """
        # Clear existing tasks
        client.delete("/api/tasks")

        # Create N tasks
        for i in range(num_tasks):
            client.post("/api/tasks", json={"title": f"Task {i}", "description": f"Description {i}"})

        # Verify we have N tasks
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == num_tasks

        # Delete all tasks
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204

        # Verify we have 0 tasks
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 0

    @given(
        st.lists(
            st.text(min_size=1, max_size=200).filter(lambda s: s.strip()),
            min_size=1,
            max_size=10,
        )
    )
    @settings(max_examples=50, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_property_delete_all_then_create_is_fresh_start(self, client, task_titles):
        """
        **Feature: task-manager-app, Property: Delete all gives fresh start**
        **Validates: System state is clean after bulk deletion**

        For any set of tasks, after DELETE /api/tasks, creating new tasks
        should result in a system state as if no previous tasks ever existed.
        """
        # Clear existing tasks
        client.delete("/api/tasks")

        # Create first batch of tasks
        for title in task_titles:
            client.post("/api/tasks", json={"title": title.strip(), "description": "First batch"})

        # Get task count before deletion
        get_response = client.get("/api/tasks")
        count_before_delete = len(get_response.json()["tasks"])

        # Delete all tasks
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204

        # Create second batch with same titles
        new_task_ids = []
        for title in task_titles:
            response = client.post("/api/tasks", json={"title": title.strip(), "description": "Second batch"})
            assert response.status_code == 201
            new_task_ids.append(response.json()["id"])

        # Verify we have exactly the same number of tasks as created in second batch
        get_response = client.get("/api/tasks")
        final_tasks = get_response.json()["tasks"]
        assert len(final_tasks) == len(task_titles)

        # Verify all tasks are from the second batch (have "Second batch" description)
        for task in final_tasks:
            assert task["description"] == "Second batch"
            assert task["id"] in new_task_ids

    @given(st.integers(min_value=1, max_value=10))
    @settings(max_examples=20, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_property_delete_all_idempotence(self, client, num_calls):
        """
        **Feature: task-manager-app, Property: Delete all idempotence**
        **Validates: Multiple calls to delete all are safe**

        For any number of consecutive calls to DELETE /api/tasks, after the
        first call, all subsequent calls should succeed with 204 status and
        the task list should remain empty.
        """
        # Clear existing tasks
        client.delete("/api/tasks")

        # Create some tasks
        client.post("/api/tasks", json={"title": "Task 1", "description": "Description"})
        client.post("/api/tasks", json={"title": "Task 2", "description": "Description"})

        # Call DELETE /api/tasks multiple times
        for i in range(num_calls):
            delete_response = client.delete("/api/tasks")
            assert delete_response.status_code == 204

            # Verify list is empty after each call
            get_response = client.get("/api/tasks")
            assert get_response.status_code == 200
            assert get_response.json()["tasks"] == []


class TestDeleteAllTasksIntegration:
    """Integration tests for DELETE /api/tasks with other endpoints"""

    def test_delete_all_does_not_affect_health_endpoint(self, client):
        """Test that DELETE /api/tasks doesn't affect /health endpoint"""
        # Create and delete tasks
        client.post("/api/tasks", json={"title": "Task 1", "description": "Description"})
        client.delete("/api/tasks")

        # Health endpoint should still work
        health_response = client.get("/health")
        assert health_response.status_code == 200
        assert health_response.json()["status"] == "healthy"

    def test_delete_all_persistence(self, client):
        """Test that DELETE /api/tasks persists across repository operations"""
        # Create tasks
        client.post("/api/tasks", json={"title": "Task 1", "description": "Description"})
        client.post("/api/tasks", json={"title": "Task 2", "description": "Description"})

        # Verify tasks exist
        get_response = client.get("/api/tasks")
        assert len(get_response.json()["tasks"]) == 2

        # Delete all tasks
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204

        # Create a new task
        create_response = client.post("/api/tasks", json={"title": "New Task", "description": "After delete"})
        assert create_response.status_code == 201
        new_task_id = create_response.json()["id"]

        # Verify only the new task exists
        get_response = client.get("/api/tasks")
        tasks = get_response.json()["tasks"]
        assert len(tasks) == 1
        assert tasks[0]["id"] == new_task_id
        assert tasks[0]["title"] == "New Task"
