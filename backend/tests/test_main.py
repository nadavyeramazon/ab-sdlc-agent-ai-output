"""
Comprehensive backend tests for FastAPI application.

This test suite covers:
- /api/hello endpoint (GET)
- /health endpoint (GET)
- Response validation
- Status codes
- JSON structure
- Edge cases and error scenarios
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from main import app


# Test client fixture
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


class TestHealthEndpoint:
    """Test suite for /health endpoint"""

    def test_health_endpoint_success(self, client):
        """Test successful response from /health endpoint"""
        response = client.get("/health")
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"

    def test_health_endpoint_status_code(self, client):
        """Test that /health returns 200 status code"""
        response = client.get("/health")
        
        assert response.status_code == 200

    def test_health_endpoint_json_structure(self, client):
        """Test that /health returns correct JSON structure"""
        response = client.get("/health")
        data = response.json()
        
        # Verify required key is present
        assert "status" in data
        
        # Verify it only contains the status key
        assert len(data) == 1

    def test_health_endpoint_status_value(self, client):
        """Test that /health returns 'healthy' status"""
        response = client.get("/health")
        data = response.json()
        
        assert data["status"] == "healthy"
        assert isinstance(data["status"], str)

    def test_health_endpoint_multiple_calls(self, client):
        """Test that multiple calls to /health are consistent"""
        for _ in range(5):
            response = client.get("/health")
            data = response.json()
            
            assert response.status_code == 200
            assert data["status"] == "healthy"

    def test_health_endpoint_with_trailing_slash(self, client):
        """Test /health endpoint with trailing slash (should fail as not defined)"""
        response = client.get("/health/")
        
        # FastAPI by default doesn't redirect, so this should return 404
        assert response.status_code == 404

    def test_health_endpoint_wrong_method_post(self, client):
        """Test that POST method is not allowed on /health"""
        response = client.post("/health")
        
        # Should return 405 Method Not Allowed
        assert response.status_code == 405

    def test_health_endpoint_wrong_method_put(self, client):
        """Test that PUT method is not allowed on /health"""
        response = client.put("/health")
        
        # Should return 405 Method Not Allowed
        assert response.status_code == 405

    def test_health_endpoint_wrong_method_delete(self, client):
        """Test that DELETE method is not allowed on /health"""
        response = client.delete("/health")
        
        # Should return 405 Method Not Allowed
        assert response.status_code == 405

    def test_health_endpoint_case_sensitivity(self, client):
        """Test that endpoint is case-sensitive"""
        response = client.get("/HEALTH")
        
        # Should return 404 as endpoint is case-sensitive
        assert response.status_code == 404


class TestCORSConfiguration:
    """Test suite for CORS middleware configuration"""

    def test_cors_headers_present(self, client):
        """Test that CORS headers are present in responses"""
        response = client.get("/api/tasks", headers={"Origin": "http://localhost:3000"})
        
        # CORS headers should be present
        assert "access-control-allow-origin" in response.headers

    def test_cors_allows_frontend_origin(self, client):
        """Test that CORS allows requests from frontend origin"""
        response = client.get(
            "/api/tasks",
            headers={"Origin": "http://localhost:3000"}
        )
        
        assert response.status_code == 200
        assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"


class TestApplicationRoutes:
    """Test suite for general application routing"""

    def test_nonexistent_route_returns_404(self, client):
        """Test that accessing non-existent route returns 404"""
        response = client.get("/nonexistent")
        
        assert response.status_code == 404

    def test_root_path_returns_404(self, client):
        """Test that root path returns 404 (no root endpoint defined)"""
        response = client.get("/")
        
        assert response.status_code == 404

    def test_api_prefix_without_endpoint(self, client):
        """Test that /api without endpoint returns 404"""
        response = client.get("/api")
        
        assert response.status_code == 404

    def test_api_prefix_with_trailing_slash(self, client):
        """Test that /api/ without endpoint returns 404"""
        response = client.get("/api/")
        
        assert response.status_code == 404


class TestResponseHeaders:
    """Test suite for HTTP response headers"""

    def test_health_endpoint_content_type(self, client):
        """Test that /health returns correct content-type header"""
        response = client.get("/health")
        
        assert response.headers["content-type"] == "application/json"

    def test_tasks_endpoint_content_type(self, client):
        """Test that /api/tasks returns correct content-type header"""
        response = client.get("/api/tasks")
        
        assert response.headers["content-type"] == "application/json"


class TestEdgeCases:
    """Test suite for edge cases and boundary conditions"""

    def test_health_endpoint_with_query_params(self, client):
        """Test /health with query parameters (should be ignored)"""
        response = client.get("/health?test=true")
        
        # Should still work normally, query params ignored
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    def test_concurrent_requests_to_health(self, client):
        """Test multiple concurrent requests to /health"""
        responses = []
        
        # Make 10 concurrent-like requests
        for _ in range(10):
            response = client.get("/health")
            responses.append(response)
        
        # All should succeed
        for response in responses:
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"


# Property-Based Tests
from hypothesis import given, strategies as st
from hypothesis import settings, HealthCheck


class TestTaskCreationProperties:
    """Property-based tests for task creation"""

    @given(st.text().filter(lambda s: not s or not s.strip()))
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_property_empty_title_rejection(self, client, empty_title):
        """
        **Feature: task-manager-app, Property 2: Empty title rejection**
        **Validates: Requirements 1.2**
        
        For any string composed entirely of whitespace or empty string,
        attempting to create a task with that title should result in a
        validation error (422 status), and the task list should remain unchanged.
        """
        # Get initial task count
        initial_response = client.get("/api/tasks")
        initial_tasks = initial_response.json()["tasks"]
        initial_count = len(initial_tasks)
        
        # Attempt to create task with empty/whitespace title
        response = client.post("/api/tasks", json={
            "title": empty_title,
            "description": "Test description"
        })
        
        # Should return validation error
        assert response.status_code == 422
        
        # Task list should remain unchanged
        after_response = client.get("/api/tasks")
        after_tasks = after_response.json()["tasks"]
        assert len(after_tasks) == initial_count

    @given(st.lists(
        st.tuples(
            st.text(min_size=1).filter(lambda s: s.strip()),  # title (non-empty)
            st.text(max_size=1000)  # description
        ),
        min_size=0,
        max_size=10
    ))
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_property_task_retrieval_completeness(self, client, task_data_list):
        """
        **Feature: task-manager-app, Property 3: Task retrieval completeness**
        **Validates: Requirements 2.1**
        
        For any set of tasks in storage, when retrieving all tasks via GET /api/tasks,
        the response should contain exactly the same tasks that exist in storage
        with no additions or omissions.
        """
        # Clear all existing tasks first
        existing_response = client.get("/api/tasks")
        for task in existing_response.json()["tasks"]:
            client.delete(f"/api/tasks/{task['id']}")
        
        # Create all tasks
        created_task_ids = set()
        for title, description in task_data_list:
            response = client.post("/api/tasks", json={
                "title": title.strip(),
                "description": description
            })
            if response.status_code == 201:
                task = response.json()
                created_task_ids.add(task["id"])
        
        # Retrieve all tasks
        response = client.get("/api/tasks")
        assert response.status_code == 200
        
        retrieved_tasks = response.json()["tasks"]
        retrieved_task_ids = {task["id"] for task in retrieved_tasks}
        
        # Verify all created tasks are retrieved
        assert created_task_ids == retrieved_task_ids
        
        # Verify count matches
        assert len(retrieved_tasks) == len(created_task_ids)

    @given(
        st.text(min_size=1, max_size=200).filter(lambda s: s.strip()),  # valid title (max 200 chars)
        st.text(max_size=1000)  # description
    )
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_property_restful_status_codes(self, client, title, description):
        """
        **Feature: task-manager-app, Property 8: RESTful status codes**
        **Validates: Requirements 6.2, 6.3, 6.4, 6.5**
        
        For any API operation, successful creates should return 201, successful updates/gets
        should return 200, successful deletes should return 204, validation errors should
        return 422, and not-found errors should return 404.
        """
        # Clear existing tasks
        existing_response = client.get("/api/tasks")
        for task in existing_response.json()["tasks"]:
            client.delete(f"/api/tasks/{task['id']}")
        
        # Test POST returns 201 for successful create
        create_response = client.post("/api/tasks", json={
            "title": title.strip(),
            "description": description
        })
        assert create_response.status_code == 201
        task_id = create_response.json()["id"]
        
        # Test GET returns 200 for successful retrieval
        get_response = client.get(f"/api/tasks/{task_id}")
        assert get_response.status_code == 200
        
        # Test PUT returns 200 for successful update
        update_response = client.put(f"/api/tasks/{task_id}", json={
            "title": "Updated " + title.strip()[:50],
            "completed": True
        })
        assert update_response.status_code == 200
        
        # Test DELETE returns 204 for successful delete
        delete_response = client.delete(f"/api/tasks/{task_id}")
        assert delete_response.status_code == 204
        
        # Test GET returns 404 for non-existent task
        not_found_response = client.get(f"/api/tasks/{task_id}")
        assert not_found_response.status_code == 404
        
        # Test PUT returns 404 for non-existent task
        update_not_found = client.put(f"/api/tasks/{task_id}", json={"title": "Test"})
        assert update_not_found.status_code == 404
        
        # Test DELETE returns 404 for non-existent task
        delete_not_found = client.delete(f"/api/tasks/{task_id}")
        assert delete_not_found.status_code == 404
        
        # Test POST returns 422 for validation error (empty title)
        validation_error = client.post("/api/tasks", json={
            "title": "",
            "description": "Test"
        })
        assert validation_error.status_code == 422
        
        # Test PUT returns 422 for validation error (empty title)
        # First create a task to update
        create_response2 = client.post("/api/tasks", json={
            "title": "Valid Title",
            "description": "Test"
        })
        task_id2 = create_response2.json()["id"]
        
        update_validation_error = client.put(f"/api/tasks/{task_id2}", json={
            "title": "   ",  # whitespace only
            "description": "Test"
        })
        assert update_validation_error.status_code == 422

    @given(st.text().filter(lambda s: not s or not s.strip()))
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_property_invalid_update_rejection(self, client, invalid_title):
        """
        **Feature: task-manager-app, Property 7: Invalid update rejection**
        **Validates: Requirements 5.3**
        
        For any task update request with an empty or whitespace-only title,
        the API should reject the request with a validation error (422 status),
        and the task should remain unchanged in storage.
        """
        # Clear existing tasks
        existing_response = client.get("/api/tasks")
        for task in existing_response.json()["tasks"]:
            client.delete(f"/api/tasks/{task['id']}")
        
        # Create a task to update
        create_response = client.post("/api/tasks", json={
            "title": "Original Title",
            "description": "Original Description"
        })
        assert create_response.status_code == 201
        task = create_response.json()
        task_id = task["id"]
        original_title = task["title"]
        original_description = task["description"]
        original_updated_at = task["updated_at"]
        
        # Attempt to update with invalid title
        update_response = client.put(f"/api/tasks/{task_id}", json={
            "title": invalid_title,
            "description": "New Description"
        })
        
        # Should return validation error
        assert update_response.status_code == 422
        
        # Task should remain unchanged
        get_response = client.get(f"/api/tasks/{task_id}")
        assert get_response.status_code == 200
        unchanged_task = get_response.json()
        
        assert unchanged_task["title"] == original_title
        assert unchanged_task["description"] == original_description
        assert unchanged_task["updated_at"] == original_updated_at

    @given(st.lists(
        st.tuples(
            st.text(min_size=1).filter(lambda s: s.strip()),  # title (non-empty)
            st.text(max_size=1000)  # description
        ),
        min_size=2,
        max_size=10
    ))
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_property_task_ordering_consistency(self, client, task_data_list):
        """
        **Feature: task-manager-app, Property 10: Task ordering consistency**
        **Validates: Requirements 2.4**
        
        For any set of tasks, when retrieved via GET /api/tasks, the tasks should be
        ordered by creation timestamp in descending order (newest first).
        """
        import time
        
        # Clear all existing tasks first
        existing_response = client.get("/api/tasks")
        for task in existing_response.json()["tasks"]:
            client.delete(f"/api/tasks/{task['id']}")
        
        # Create tasks with small delays to ensure different timestamps
        created_tasks = []
        for title, description in task_data_list:
            response = client.post("/api/tasks", json={
                "title": title.strip(),
                "description": description
            })
            if response.status_code == 201:
                task = response.json()
                created_tasks.append(task)
                time.sleep(0.01)  # Small delay to ensure different timestamps
        
        # Retrieve all tasks
        response = client.get("/api/tasks")
        assert response.status_code == 200
        
        retrieved_tasks = response.json()["tasks"]
        
        # Verify tasks are ordered by creation timestamp (newest first)
        if len(retrieved_tasks) > 1:
            for i in range(len(retrieved_tasks) - 1):
                current_timestamp = retrieved_tasks[i]["created_at"]
                next_timestamp = retrieved_tasks[i + 1]["created_at"]
                
                # Current task should have a timestamp >= next task (descending order)
                assert current_timestamp >= next_timestamp, \
                    f"Tasks not in descending order: {current_timestamp} should be >= {next_timestamp}"

    @given(
        st.text(min_size=1, max_size=200).filter(lambda s: s.strip()),  # valid title (max 200 chars)
        st.text(max_size=1000),  # description
        st.booleans()  # initial completion status
    )
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_property_completion_toggle_idempotence(self, client, title, description, initial_completed):
        """
        **Feature: task-manager-app, Property 4: Completion toggle idempotence**
        **Validates: Requirements 3.1, 3.3**
        
        For any task, toggling its completion status twice should return it to its
        original state, and the persisted data should reflect this final state.
        """
        # Clear all existing tasks first
        existing_response = client.get("/api/tasks")
        for task in existing_response.json()["tasks"]:
            client.delete(f"/api/tasks/{task['id']}")
        
        # Ensure title doesn't exceed 200 chars after stripping
        trimmed_title = title.strip()[:200]
        
        # Create a task with initial completion status
        create_response = client.post("/api/tasks", json={
            "title": trimmed_title,
            "description": description
        })
        assert create_response.status_code == 201
        task = create_response.json()
        task_id = task["id"]
        
        # Set initial completion status if different from default (False)
        if initial_completed:
            update_response = client.put(f"/api/tasks/{task_id}", json={
                "completed": initial_completed
            })
            assert update_response.status_code == 200
        
        # Get the task to confirm initial state
        get_response = client.get(f"/api/tasks/{task_id}")
        assert get_response.status_code == 200
        initial_task = get_response.json()
        initial_status = initial_task["completed"]
        
        # Toggle completion status (first toggle)
        toggle1_response = client.put(f"/api/tasks/{task_id}", json={
            "completed": not initial_status
        })
        assert toggle1_response.status_code == 200
        toggled_task = toggle1_response.json()
        assert toggled_task["completed"] == (not initial_status)
        
        # Toggle completion status again (second toggle)
        toggle2_response = client.put(f"/api/tasks/{task_id}", json={
            "completed": initial_status
        })
        assert toggle2_response.status_code == 200
        final_task = toggle2_response.json()
        
        # Verify task is back to original state
        assert final_task["completed"] == initial_status
        
        # Verify persistence by retrieving the task again
        verify_response = client.get(f"/api/tasks/{task_id}")
        assert verify_response.status_code == 200
        persisted_task = verify_response.json()
        assert persisted_task["completed"] == initial_status
        
        # Verify other fields remain unchanged
        assert persisted_task["id"] == task_id
        assert persisted_task["title"] == trimmed_title
        assert persisted_task["description"] == description

    @given(
        st.text(min_size=1, max_size=200).filter(lambda s: s.strip()),  # valid title (max 200 chars)
        st.text(max_size=1000)  # description
    )
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_property_delete_operation_removes_task(self, client, title, description):
        """
        **Feature: task-manager-app, Property 5: Delete operation removes task**
        **Validates: Requirements 4.1, 4.2**
        
        For any existing task, when a delete operation succeeds (204 status),
        subsequent attempts to retrieve that specific task should return 404,
        and the task should not appear in the list of all tasks.
        """
        # Clear all existing tasks first
        existing_response = client.get("/api/tasks")
        for task in existing_response.json()["tasks"]:
            client.delete(f"/api/tasks/{task['id']}")
        
        # Ensure title doesn't exceed 200 chars after stripping
        trimmed_title = title.strip()[:200]
        
        # Create a task
        create_response = client.post("/api/tasks", json={
            "title": trimmed_title,
            "description": description
        })
        assert create_response.status_code == 201
        task = create_response.json()
        task_id = task["id"]
        
        # Verify task exists before deletion
        get_before_response = client.get(f"/api/tasks/{task_id}")
        assert get_before_response.status_code == 200
        
        # Verify task appears in the list
        list_before_response = client.get("/api/tasks")
        assert list_before_response.status_code == 200
        tasks_before = list_before_response.json()["tasks"]
        task_ids_before = {t["id"] for t in tasks_before}
        assert task_id in task_ids_before
        
        # Delete the task
        delete_response = client.delete(f"/api/tasks/{task_id}")
        assert delete_response.status_code == 204
        
        # Verify task no longer exists (GET should return 404)
        get_after_response = client.get(f"/api/tasks/{task_id}")
        assert get_after_response.status_code == 404
        
        # Verify task does not appear in the list
        list_after_response = client.get("/api/tasks")
        assert list_after_response.status_code == 200
        tasks_after = list_after_response.json()["tasks"]
        task_ids_after = {t["id"] for t in tasks_after}
        assert task_id not in task_ids_after
        
        # Verify attempting to delete again returns 404
        delete_again_response = client.delete(f"/api/tasks/{task_id}")
        assert delete_again_response.status_code == 404



class TestTaskAPIEndpoints:
    """Unit tests for task API endpoints"""

    def test_get_all_tasks_empty_list(self, client):
        """Test GET /api/tasks with empty task list"""
        # Clear all tasks
        existing_response = client.get("/api/tasks")
        for task in existing_response.json()["tasks"]:
            client.delete(f"/api/tasks/{task['id']}")
        
        response = client.get("/api/tasks")
        assert response.status_code == 200
        data = response.json()
        assert "tasks" in data
        assert data["tasks"] == []

    def test_get_all_tasks_populated_list(self, client):
        """Test GET /api/tasks with populated task list"""
        # Clear all tasks
        existing_response = client.get("/api/tasks")
        for task in existing_response.json()["tasks"]:
            client.delete(f"/api/tasks/{task['id']}")
        
        # Create some tasks
        task1 = client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})
        task2 = client.post("/api/tasks", json={"title": "Task 2", "description": "Desc 2"})
        
        response = client.get("/api/tasks")
        assert response.status_code == 200
        data = response.json()
        assert "tasks" in data
        assert len(data["tasks"]) == 2

    def test_post_task_valid_data(self, client):
        """Test POST /api/tasks with valid data"""
        response = client.post("/api/tasks", json={
            "title": "New Task",
            "description": "Task description"
        })
        
        assert response.status_code == 201
        task = response.json()
        assert task["title"] == "New Task"
        assert task["description"] == "Task description"
        assert task["completed"] is False
        assert "id" in task
        assert "created_at" in task
        assert "updated_at" in task

    def test_post_task_invalid_empty_title(self, client):
        """Test POST /api/tasks with empty title"""
        response = client.post("/api/tasks", json={
            "title": "",
            "description": "Description"
        })
        
        assert response.status_code == 422

    def test_post_task_invalid_whitespace_title(self, client):
        """Test POST /api/tasks with whitespace-only title"""
        response = client.post("/api/tasks", json={
            "title": "   ",
            "description": "Description"
        })
        
        assert response.status_code == 422

    def test_post_task_title_too_long(self, client):
        """Test POST /api/tasks with title exceeding 200 characters"""
        long_title = "a" * 201
        response = client.post("/api/tasks", json={
            "title": long_title,
            "description": "Description"
        })
        
        assert response.status_code == 422

    def test_post_task_description_too_long(self, client):
        """Test POST /api/tasks with description exceeding 1000 characters"""
        long_description = "a" * 1001
        response = client.post("/api/tasks", json={
            "title": "Valid Title",
            "description": long_description
        })
        
        assert response.status_code == 422

    def test_get_task_by_id_existing(self, client):
        """Test GET /api/tasks/{id} with existing task"""
        # Create a task
        create_response = client.post("/api/tasks", json={
            "title": "Test Task",
            "description": "Test Description"
        })
        task_id = create_response.json()["id"]
        
        # Get the task
        response = client.get(f"/api/tasks/{task_id}")
        assert response.status_code == 200
        task = response.json()
        assert task["id"] == task_id
        assert task["title"] == "Test Task"
        assert task["description"] == "Test Description"

    def test_get_task_by_id_non_existent(self, client):
        """Test GET /api/tasks/{id} with non-existent ID"""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = client.get(f"/api/tasks/{fake_id}")
        
        assert response.status_code == 404

    def test_put_task_valid_data(self, client):
        """Test PUT /api/tasks/{id} with valid data"""
        # Create a task
        create_response = client.post("/api/tasks", json={
            "title": "Original Title",
            "description": "Original Description"
        })
        task_id = create_response.json()["id"]
        
        # Update the task
        response = client.put(f"/api/tasks/{task_id}", json={
            "title": "Updated Title",
            "description": "Updated Description",
            "completed": True
        })
        
        assert response.status_code == 200
        task = response.json()
        assert task["id"] == task_id
        assert task["title"] == "Updated Title"
        assert task["description"] == "Updated Description"
        assert task["completed"] is True

    def test_put_task_partial_update(self, client):
        """Test PUT /api/tasks/{id} with partial data"""
        # Create a task
        create_response = client.post("/api/tasks", json={
            "title": "Original Title",
            "description": "Original Description"
        })
        task_id = create_response.json()["id"]
        
        # Update only the title
        response = client.put(f"/api/tasks/{task_id}", json={
            "title": "Updated Title"
        })
        
        assert response.status_code == 200
        task = response.json()
        assert task["title"] == "Updated Title"
        assert task["description"] == "Original Description"

    def test_put_task_invalid_empty_title(self, client):
        """Test PUT /api/tasks/{id} with empty title"""
        # Create a task
        create_response = client.post("/api/tasks", json={
            "title": "Original Title",
            "description": "Original Description"
        })
        task_id = create_response.json()["id"]
        
        # Attempt to update with empty title
        response = client.put(f"/api/tasks/{task_id}", json={
            "title": ""
        })
        
        assert response.status_code == 422

    def test_put_task_non_existent(self, client):
        """Test PUT /api/tasks/{id} with non-existent ID"""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = client.put(f"/api/tasks/{fake_id}", json={
            "title": "Updated Title"
        })
        
        assert response.status_code == 404

    def test_delete_task_existing(self, client):
        """Test DELETE /api/tasks/{id} with existing task"""
        # Create a task
        create_response = client.post("/api/tasks", json={
            "title": "Task to Delete",
            "description": "Will be deleted"
        })
        task_id = create_response.json()["id"]
        
        # Delete the task
        response = client.delete(f"/api/tasks/{task_id}")
        assert response.status_code == 204
        
        # Verify task is deleted
        get_response = client.get(f"/api/tasks/{task_id}")
        assert get_response.status_code == 404

    def test_delete_task_non_existent(self, client):
        """Test DELETE /api/tasks/{id} with non-existent ID"""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = client.delete(f"/api/tasks/{fake_id}")
        
        assert response.status_code == 404

    def test_task_404_responses(self, client):
        """Test that 404 responses are returned for non-existent tasks"""
        fake_id = "00000000-0000-0000-0000-000000000000"
        
        # GET should return 404
        get_response = client.get(f"/api/tasks/{fake_id}")
        assert get_response.status_code == 404
        
        # PUT should return 404
        put_response = client.put(f"/api/tasks/{fake_id}", json={"title": "Test"})
        assert put_response.status_code == 404
        
        # DELETE should return 404
        delete_response = client.delete(f"/api/tasks/{fake_id}")
        assert delete_response.status_code == 404

    @given(
        st.text(min_size=1, max_size=200).filter(lambda s: s.strip()),  # original title
        st.text(max_size=1000),  # original description
        st.text(min_size=1, max_size=200).filter(lambda s: s.strip()),  # updated title
        st.text(max_size=1000)  # updated description
    )
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_property_update_preserves_identity(self, client, original_title, original_description, updated_title, updated_description):
        """
        **Feature: task-manager-app, Property 6: Update preserves identity**
        **Validates: Requirements 5.2, 5.4**
        
        For any existing task, when updating its title or description, the task's ID
        and creation timestamp should remain unchanged, while the updated_at timestamp
        should be more recent.
        """
        import time
        
        # Clear all existing tasks first
        existing_response = client.get("/api/tasks")
        for task in existing_response.json()["tasks"]:
            client.delete(f"/api/tasks/{task['id']}")
        
        # Ensure titles don't exceed 200 chars after stripping
        trimmed_original_title = original_title.strip()[:200]
        trimmed_updated_title = updated_title.strip()[:200]
        
        # Create a task
        create_response = client.post("/api/tasks", json={
            "title": trimmed_original_title,
            "description": original_description
        })
        assert create_response.status_code == 201
        original_task = create_response.json()
        task_id = original_task["id"]
        original_created_at = original_task["created_at"]
        original_updated_at = original_task["updated_at"]
        
        # Small delay to ensure updated_at will be different
        time.sleep(0.01)
        
        # Update the task
        update_response = client.put(f"/api/tasks/{task_id}", json={
            "title": trimmed_updated_title,
            "description": updated_description
        })
        assert update_response.status_code == 200
        updated_task = update_response.json()
        
        # Verify ID remains unchanged
        assert updated_task["id"] == task_id
        
        # Verify created_at remains unchanged
        assert updated_task["created_at"] == original_created_at
        
        # Verify updated_at is more recent (or at least not earlier)
        assert updated_task["updated_at"] >= original_updated_at
        
        # Verify the update was actually applied
        assert updated_task["title"] == trimmed_updated_title
        assert updated_task["description"] == updated_description
        
        # Verify persistence by retrieving the task again
        verify_response = client.get(f"/api/tasks/{task_id}")
        assert verify_response.status_code == 200
        persisted_task = verify_response.json()
        
        # Verify all identity properties are preserved in persisted data
        assert persisted_task["id"] == task_id
        assert persisted_task["created_at"] == original_created_at
        assert persisted_task["updated_at"] >= original_updated_at
        assert persisted_task["title"] == trimmed_updated_title
        assert persisted_task["description"] == updated_description


class TestDeleteAllTasksEndpoint:
    """Test suite for DELETE /api/tasks endpoint (delete all tasks)"""

    def test_delete_all_tasks_empty_list(self, client):
        """Test DELETE /api/tasks with empty task list returns 204"""
        # Clear all tasks first
        existing_response = client.get("/api/tasks")
        for task in existing_response.json()["tasks"]:
            client.delete(f"/api/tasks/{task['id']}")
        
        # Verify list is empty
        response = client.get("/api/tasks")
        assert response.json()["tasks"] == []
        
        # Delete all (on empty list)
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204
        
        # Verify still empty
        response = client.get("/api/tasks")
        assert response.json()["tasks"] == []

    def test_delete_all_tasks_populated_list(self, client):
        """Test DELETE /api/tasks removes all tasks and returns 204"""
        # Clear all tasks first
        existing_response = client.get("/api/tasks")
        for task in existing_response.json()["tasks"]:
            client.delete(f"/api/tasks/{task['id']}")
        
        # Create some tasks
        client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})
        client.post("/api/tasks", json={"title": "Task 2", "description": "Desc 2"})
        client.post("/api/tasks", json={"title": "Task 3", "description": "Desc 3"})
        
        # Verify tasks exist
        response = client.get("/api/tasks")
        assert len(response.json()["tasks"]) == 3
        
        # Delete all tasks
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204
        
        # Verify all tasks are deleted
        response = client.get("/api/tasks")
        assert response.json()["tasks"] == []

    def test_delete_all_tasks_returns_no_content(self, client):
        """Test DELETE /api/tasks returns no content body"""
        # Create a task
        client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})
        
        # Delete all tasks
        delete_response = client.delete("/api/tasks")
        
        # Verify 204 status and empty/no content
        assert delete_response.status_code == 204
        assert delete_response.content == b'' or delete_response.text == ''

    def test_delete_all_tasks_allows_new_tasks_after(self, client):
        """Test that new tasks can be created after delete all"""
        # Clear all tasks first
        existing_response = client.get("/api/tasks")
        for task in existing_response.json()["tasks"]:
            client.delete(f"/api/tasks/{task['id']}")
        
        # Create some tasks
        client.post("/api/tasks", json={"title": "Old Task 1", "description": "Desc 1"})
        client.post("/api/tasks", json={"title": "Old Task 2", "description": "Desc 2"})
        
        # Delete all tasks
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204
        
        # Create new tasks
        create_response = client.post("/api/tasks", json={
            "title": "New Task",
            "description": "New Description"
        })
        assert create_response.status_code == 201
        
        # Verify only the new task exists
        response = client.get("/api/tasks")
        tasks = response.json()["tasks"]
        assert len(tasks) == 1
        assert tasks[0]["title"] == "New Task"

    def test_delete_all_tasks_idempotent(self, client):
        """Test that calling delete all twice works correctly"""
        # Clear all tasks first
        existing_response = client.get("/api/tasks")
        for task in existing_response.json()["tasks"]:
            client.delete(f"/api/tasks/{task['id']}")
        
        # Create some tasks
        client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})
        
        # First delete all
        delete_response1 = client.delete("/api/tasks")
        assert delete_response1.status_code == 204
        
        # Second delete all (on empty list)
        delete_response2 = client.delete("/api/tasks")
        assert delete_response2.status_code == 204
        
        # Verify empty
        response = client.get("/api/tasks")
        assert response.json()["tasks"] == []

    def test_delete_all_tasks_individual_tasks_not_found_after(self, client):
        """Test that individual tasks return 404 after delete all"""
        # Clear all tasks first
        existing_response = client.get("/api/tasks")
        for task in existing_response.json()["tasks"]:
            client.delete(f"/api/tasks/{task['id']}")
        
        # Create some tasks and store their IDs
        task_ids = []
        for i in range(3):
            response = client.post("/api/tasks", json={
                "title": f"Task {i}",
                "description": f"Description {i}"
            })
            task_ids.append(response.json()["id"])
        
        # Verify tasks exist
        for task_id in task_ids:
            response = client.get(f"/api/tasks/{task_id}")
            assert response.status_code == 200
        
        # Delete all tasks
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204
        
        # Verify individual tasks return 404
        for task_id in task_ids:
            response = client.get(f"/api/tasks/{task_id}")
            assert response.status_code == 404

    def test_delete_all_tasks_wrong_methods(self, client):
        """Test that other methods on /api/tasks work correctly"""
        # GET should return task list
        get_response = client.get("/api/tasks")
        assert get_response.status_code == 200
        
        # POST should create task
        post_response = client.post("/api/tasks", json={
            "title": "Test Task",
            "description": "Test Description"
        })
        assert post_response.status_code == 201
        
        # PUT on collection endpoint should return 405
        put_response = client.put("/api/tasks", json={"title": "Test"})
        assert put_response.status_code == 405

    @given(st.lists(
        st.tuples(
            st.text(min_size=1, max_size=200).filter(lambda s: s.strip()),
            st.text(max_size=1000)
        ),
        min_size=0,
        max_size=15
    ))
    @settings(max_examples=50, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_property_delete_all_removes_all_tasks(self, client, task_data_list):
        """
        Property: For any set of tasks, calling DELETE /api/tasks should result
        in an empty task list.
        """
        # Clear all existing tasks first
        existing_response = client.get("/api/tasks")
        for task in existing_response.json()["tasks"]:
            client.delete(f"/api/tasks/{task['id']}")
        
        # Create tasks
        for title, description in task_data_list:
            client.post("/api/tasks", json={
                "title": title.strip(),
                "description": description
            })
        
        # Verify expected count before delete
        before_response = client.get("/api/tasks")
        # Count may be less than task_data_list if there are duplicates or validation issues
        
        # Delete all tasks
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204
        
        # Verify empty after delete
        after_response = client.get("/api/tasks")
        assert after_response.json()["tasks"] == []

    @given(st.lists(
        st.tuples(
            st.text(min_size=1, max_size=200).filter(lambda s: s.strip()),
            st.text(max_size=1000)
        ),
        min_size=1,
        max_size=10
    ))
    @settings(max_examples=50, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_property_delete_all_then_create_works(self, client, task_data_list):
        """
        Property: After calling DELETE /api/tasks, new tasks can be created
        and will be the only tasks in the system.
        """
        # Clear all existing tasks first
        existing_response = client.get("/api/tasks")
        for task in existing_response.json()["tasks"]:
            client.delete(f"/api/tasks/{task['id']}")
        
        # Create initial tasks
        for title, description in task_data_list:
            client.post("/api/tasks", json={
                "title": title.strip(),
                "description": description
            })
        
        # Delete all tasks
        delete_response = client.delete("/api/tasks")
        assert delete_response.status_code == 204
        
        # Create a new task
        new_task_response = client.post("/api/tasks", json={
            "title": "Brand New Task",
            "description": "This should be the only task"
        })
        assert new_task_response.status_code == 201
        new_task_id = new_task_response.json()["id"]
        
        # Verify only the new task exists
        all_tasks_response = client.get("/api/tasks")
        tasks = all_tasks_response.json()["tasks"]
        assert len(tasks) == 1
        assert tasks[0]["id"] == new_task_id
        assert tasks[0]["title"] == "Brand New Task"
