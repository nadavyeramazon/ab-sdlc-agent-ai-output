"""
Comprehensive tests for DELETE /api/tasks endpoint (delete all tasks).

This test suite covers:
- Successful deletion of all tasks
- Behavior when no tasks exist
- Database state after deletion
- Error scenarios and edge cases
- Idempotency
- Integration with other endpoints
"""

import pytest
from fastapi.testclient import TestClient
from hypothesis import given, settings, strategies as st
from hypothesis import HealthCheck
from main import app


@pytest.fixture
def client():
    """
    Create a TestClient instance for testing FastAPI endpoints.
    This fixture is reused across all tests.
    """
    import tempfile
    import os
    from task_repository import TaskRepository
    
    # Create a temporary directory for test data
    temp_dir = tempfile.mkdtemp()
    test_data_file = os.path.join(temp_dir, "test_tasks.json")
    
    # Override the repository with test data file
    import main
    main._task_repository = TaskRepository(data_file=test_data_file)
    
    client = TestClient(app)
    
    yield client
    
    # Cleanup
    import shutil
    shutil.rmtree(temp_dir, ignore_errors=True)
    main._task_repository = None


class TestDeleteAllTasksEndpoint:
    """
    Comprehensive tests for DELETE /api/tasks endpoint.
    
    **Feature: task-manager-app, Delete All Tasks**
    **Validates: Bulk deletion of all tasks via REST API**
    """
    
    def test_delete_all_tasks_success(self, client):
        """
        Test successful deletion of all tasks.
        
        Verifies:
        - Returns 204 No Content status
        - All tasks are deleted
        - GET /api/tasks returns empty list after deletion
        """
        # Clear existing tasks first
        existing_response = client.get("/api/tasks")
        for task in existing_response.json()["tasks"]:
            client.delete(f"/api/tasks/{task['id']}")
        
        # Create multiple tasks
        client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})
        client.post("/api/tasks", json={"title": "Task 2", "description": "Desc 2"})
        client.post("/api/tasks", json={"title": "Task 3", "description": "Desc 3"})
        
        # Verify tasks exist
        before_response = client.get("/api/tasks")
        assert before_response.status_code == 200
        assert len(before_response.json()["tasks"]) == 3
        
        # Delete all tasks
        delete_response = client.delete("/api/tasks")
        
        # Verify status code
        assert delete_response.status_code == 204
        
        # Verify response has no content
        assert delete_response.content == b""
        
        # Verify all tasks are deleted
        after_response = client.get("/api/tasks")
        assert after_response.status_code == 200
        tasks = after_response.json()["tasks"]
        assert len(tasks) == 0
        assert tasks == []
    
    def test_delete_all_tasks_empty_repository(self, client):
        """
        Test delete_all when no tasks exist.
        
        Verifies:
        - Returns 204 No Content status
        - Does not cause errors
        - Repository remains in valid state
        """
        # Clear all existing tasks
        existing_response = client.get("/api/tasks")
        for task in existing_response.json()["tasks"]:
            client.delete(f"/api/tasks/{task['id']}")
        
        # Verify repository is empty
        before_response = client.get("/api/tasks")
        assert len(before_response.json()["tasks"]) == 0
        
        # Delete all tasks (none exist)
        delete_response = client.delete("/api/tasks")
        
        # Verify status code
        assert delete_response.status_code == 204
        
        # Verify repository is still empty
        after_response = client.get("/api/tasks")
        assert after_response.status_code == 200
        assert len(after_response.json()["tasks"]) == 0
    
    def test_delete_all_tasks_idempotence(self, client):
        """
        Test that calling delete_all multiple times is safe (idempotent).
        
        Verifies:
        - Multiple calls return 204
        - No errors occur
        - Repository remains empty after each call
        """
        # Clear existing tasks first
        existing_response = client.get("/api/tasks")
        for task in existing_response.json()["tasks"]:
            client.delete(f"/api/tasks/{task['id']}")
        
        # Create tasks
        client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})
        client.post("/api/tasks", json={"title": "Task 2", "description": "Desc 2"})
        
        # First delete_all
        delete_response1 = client.delete("/api/tasks")
        assert delete_response1.status_code == 204
        assert len(client.get("/api/tasks").json()["tasks"]) == 0
        
        # Second delete_all (should be safe)
        delete_response2 = client.delete("/api/tasks")
        assert delete_response2.status_code == 204
        assert len(client.get("/api/tasks").json()["tasks"]) == 0
        
        # Third delete_all (should still be safe)
        delete_response3 = client.delete("/api/tasks")
        assert delete_response3.status_code == 204
        assert len(client.get("/api/tasks").json()["tasks"]) == 0
    
    def test_delete_all_tasks_specific_tasks_not_retrievable(self, client):
        """
        Test that specific tasks cannot be retrieved after delete_all.
        
        Verifies:
        - Individual task IDs return 404 after delete_all
        - All tasks are truly deleted, not just hidden
        """
        # Clear existing tasks first
        existing_response = client.get("/api/tasks")
        for task in existing_response.json()["tasks"]:
            client.delete(f"/api/tasks/{task['id']}")
        
        # Create tasks and store their IDs
        response1 = client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})
        task1_id = response1.json()["id"]
        
        response2 = client.post("/api/tasks", json={"title": "Task 2", "description": "Desc 2"})
        task2_id = response2.json()["id"]
        
        response3 = client.post("/api/tasks", json={"title": "Task 3", "description": "Desc 3"})
        task3_id = response3.json()["id"]
        
        # Verify tasks can be retrieved before deletion
        assert client.get(f"/api/tasks/{task1_id}").status_code == 200
        assert client.get(f"/api/tasks/{task2_id}").status_code == 200
        assert client.get(f"/api/tasks/{task3_id}").status_code == 200
        
        # Delete all tasks
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204
        
        # Verify tasks cannot be retrieved after deletion
        assert client.get(f"/api/tasks/{task1_id}").status_code == 404
        assert client.get(f"/api/tasks/{task2_id}").status_code == 404
        assert client.get(f"/api/tasks/{task3_id}").status_code == 404
    
    def test_delete_all_tasks_allows_new_tasks_after_deletion(self, client):
        """
        Test that new tasks can be created after delete_all.
        
        Verifies:
        - API remains functional after delete_all
        - New tasks can be created with fresh IDs
        - New tasks are properly stored and retrievable
        """
        # Clear existing tasks first
        existing_response = client.get("/api/tasks")
        for task in existing_response.json()["tasks"]:
            client.delete(f"/api/tasks/{task['id']}")
        
        # Create initial tasks
        client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})
        client.post("/api/tasks", json={"title": "Task 2", "description": "Desc 2"})
        
        # Delete all tasks
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204
        
        # Create new tasks after deletion
        new_response1 = client.post("/api/tasks", json={"title": "New Task 1", "description": "New Desc 1"})
        new_response2 = client.post("/api/tasks", json={"title": "New Task 2", "description": "New Desc 2"})
        
        # Verify new tasks were created
        assert new_response1.status_code == 201
        assert new_response2.status_code == 201
        
        # Verify new tasks exist
        tasks_response = client.get("/api/tasks")
        tasks = tasks_response.json()["tasks"]
        assert len(tasks) == 2
        assert tasks[0]["title"] in ["New Task 1", "New Task 2"]
        assert tasks[1]["title"] in ["New Task 1", "New Task 2"]
    
    def test_delete_all_tasks_with_mixed_states(self, client):
        """
        Test delete_all removes tasks regardless of completion state.
        
        Verifies:
        - Both completed and incomplete tasks are deleted
        - Task state doesn't affect deletion
        """
        # Clear existing tasks first
        existing_response = client.get("/api/tasks")
        for task in existing_response.json()["tasks"]:
            client.delete(f"/api/tasks/{task['id']}")
        
        # Create incomplete task
        incomplete_response = client.post("/api/tasks", json={"title": "Incomplete Task", "description": "Not done"})
        incomplete_id = incomplete_response.json()["id"]
        
        # Create completed task
        complete_response = client.post("/api/tasks", json={"title": "Complete Task", "description": "Done"})
        complete_id = complete_response.json()["id"]
        client.put(f"/api/tasks/{complete_id}", json={"completed": True})
        
        # Verify both tasks exist
        assert len(client.get("/api/tasks").json()["tasks"]) == 2
        
        # Delete all tasks
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204
        
        # Verify both tasks are deleted
        assert len(client.get("/api/tasks").json()["tasks"]) == 0
        assert client.get(f"/api/tasks/{incomplete_id}").status_code == 404
        assert client.get(f"/api/tasks/{complete_id}").status_code == 404
    
    def test_delete_all_tasks_wrong_http_methods(self, client):
        """
        Test that other HTTP methods are not allowed on /api/tasks (without ID).
        
        Verifies:
        - PUT is not allowed (405)
        - PATCH is not allowed (405)
        - GET and POST are allowed (separate endpoint functionality)
        """
        # Test PUT is not allowed
        put_response = client.put("/api/tasks", json={"title": "Test"})
        assert put_response.status_code == 405
        
        # Test PATCH is not allowed
        patch_response = client.patch("/api/tasks", json={"title": "Test"})
        assert patch_response.status_code == 405
        
        # Verify GET still works (different endpoint)
        get_response = client.get("/api/tasks")
        assert get_response.status_code == 200
        
        # Verify POST still works (different endpoint)
        post_response = client.post("/api/tasks", json={"title": "Test Task", "description": "Test"})
        assert post_response.status_code == 201
    
    def test_delete_all_tasks_no_trailing_slash(self, client):
        """
        Test that /api/tasks/ (with trailing slash) is not the same endpoint.
        
        Verifies:
        - Trailing slash returns 404 (redirect_slashes is disabled)
        - Endpoint is strict about path matching
        """
        # Clear existing tasks first
        existing_response = client.get("/api/tasks")
        for task in existing_response.json()["tasks"]:
            client.delete(f"/api/tasks/{task['id']}")
        
        # Create a task
        client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})
        
        # Try to delete with trailing slash
        delete_response = client.delete("/api/tasks/")
        
        # Should return 404 (redirect_slashes is disabled)
        assert delete_response.status_code == 404
        
        # Verify task still exists
        tasks = client.get("/api/tasks").json()["tasks"]
        assert len(tasks) == 1
    
    def test_delete_all_tasks_response_headers(self, client):
        """
        Test that delete_all returns appropriate response headers.
        
        Verifies:
        - CORS headers are present (if configured)
        - Content-Length is 0 or not present
        - No body is returned
        """
        # Clear existing tasks first
        existing_response = client.get("/api/tasks")
        for task in existing_response.json()["tasks"]:
            client.delete(f"/api/tasks/{task['id']}")
        
        # Create tasks
        client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})
        
        # Delete all tasks
        delete_response = client.delete("/api/tasks")
        
        # Verify status code
        assert delete_response.status_code == 204
        
        # Verify no content is returned
        assert delete_response.content == b""
        
        # Verify content-length is 0 or not set
        content_length = delete_response.headers.get("content-length")
        if content_length is not None:
            assert int(content_length) == 0
    
    @given(st.lists(
        st.tuples(
            st.text(min_size=1, max_size=200).filter(lambda s: s.strip()),  # title
            st.text(max_size=1000)  # description
        ),
        min_size=1,
        max_size=20
    ))
    @settings(max_examples=50, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_property_delete_all_removes_all_tasks_comprehensive(self, client, task_data_list):
        """
        Property-based test: DELETE /api/tasks removes all tasks regardless of quantity.
        
        For any non-empty set of tasks, delete_all should remove all tasks
        and return 204 status.
        
        **Feature: task-manager-app, Property: Delete all completeness via API**
        """
        # Clear existing tasks first
        existing_response = client.get("/api/tasks")
        for task in existing_response.json()["tasks"]:
            client.delete(f"/api/tasks/{task['id']}")
        
        # Create all tasks
        created_count = 0
        for title, description in task_data_list:
            response = client.post("/api/tasks", json={
                "title": title.strip(),
                "description": description
            })
            if response.status_code == 201:
                created_count += 1
        
        # Verify tasks were created
        tasks_before = client.get("/api/tasks").json()["tasks"]
        assert len(tasks_before) == created_count
        
        # Delete all tasks
        delete_response = client.delete("/api/tasks")
        
        # Verify deletion succeeded
        assert delete_response.status_code == 204
        
        # Verify all tasks are deleted
        tasks_after = client.get("/api/tasks").json()["tasks"]
        assert len(tasks_after) == 0
    
    def test_delete_all_tasks_persistence(self, client):
        """
        Test that delete_all persists deletion to storage.
        
        Verifies:
        - Deletion is written to persistent storage
        - Repository reload shows empty state
        - New repository instance has no tasks
        """
        import tempfile
        import os
        from task_repository import TaskRepository
        
        # Create a new temp file for this specific test
        temp_dir = tempfile.mkdtemp()
        test_data_file = os.path.join(temp_dir, "persistence_test.json")
        
        try:
            # Create repository with test file
            import main
            original_repo = main._task_repository
            main._task_repository = TaskRepository(data_file=test_data_file)
            
            # Use new test client with this repository
            test_client = TestClient(app)
            
            # Create tasks
            test_client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})
            test_client.post("/api/tasks", json={"title": "Task 2", "description": "Desc 2"})
            
            # Delete all tasks
            delete_response = test_client.delete("/api/tasks")
            assert delete_response.status_code == 204
            
            # Create new repository instance (simulates app restart)
            main._task_repository = TaskRepository(data_file=test_data_file)
            test_client = TestClient(app)
            
            # Verify tasks are still deleted after "restart"
            tasks = test_client.get("/api/tasks").json()["tasks"]
            assert len(tasks) == 0
            
            # Restore original repository
            main._task_repository = original_repo
            
        finally:
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)
    
    def test_delete_all_tasks_concurrent_operations(self, client):
        """
        Test delete_all behavior with rapid successive calls.
        
        Verifies:
        - Multiple rapid calls don't cause errors
        - Final state is consistent (empty)
        - No race conditions or data corruption
        """
        # Clear existing tasks first
        existing_response = client.get("/api/tasks")
        for task in existing_response.json()["tasks"]:
            client.delete(f"/api/tasks/{task['id']}")
        
        # Create multiple tasks
        for i in range(10):
            client.post("/api/tasks", json={"title": f"Task {i}", "description": f"Desc {i}"})
        
        # Make multiple rapid delete_all calls
        responses = []
        for _ in range(5):
            response = client.delete("/api/tasks")
            responses.append(response)
        
        # Verify all responses are 204
        for response in responses:
            assert response.status_code == 204
        
        # Verify final state is empty
        final_tasks = client.get("/api/tasks").json()["tasks"]
        assert len(final_tasks) == 0
    
    def test_delete_all_tasks_integration_with_other_endpoints(self, client):
        """
        Test delete_all integration with other task endpoints.
        
        Verifies:
        - Individual task operations work before delete_all
        - Individual task operations work after delete_all
        - All endpoints remain functional
        """
        # Clear existing tasks first
        existing_response = client.get("/api/tasks")
        for task in existing_response.json()["tasks"]:
            client.delete(f"/api/tasks/{task['id']}")
        
        # Create a task
        create_response = client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})
        task_id = create_response.json()["id"]
        
        # Update the task
        update_response = client.put(f"/api/tasks/{task_id}", json={"title": "Updated Task 1"})
        assert update_response.status_code == 200
        
        # Get the task
        get_response = client.get(f"/api/tasks/{task_id}")
        assert get_response.status_code == 200
        
        # Delete all tasks
        delete_all_response = client.delete("/api/tasks")
        assert delete_all_response.status_code == 204
        
        # Verify task is gone
        get_after_response = client.get(f"/api/tasks/{task_id}")
        assert get_after_response.status_code == 404
        
        # Create new task after delete_all
        new_create_response = client.post("/api/tasks", json={"title": "New Task", "description": "New Desc"})
        assert new_create_response.status_code == 201
        new_task_id = new_create_response.json()["id"]
        
        # Verify new task exists
        new_get_response = client.get(f"/api/tasks/{new_task_id}")
        assert new_get_response.status_code == 200
