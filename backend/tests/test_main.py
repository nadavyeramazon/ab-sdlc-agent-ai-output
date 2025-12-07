"""
Comprehensive backend tests for FastAPI application.

This test suite covers:
- /health endpoint (GET)
- Task API endpoints (CRUD operations)
- Response validation
- Status codes
- JSON structure
- Edge cases and error scenarios
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

    repo.get_all = get_all
    repo.get_by_id = get_by_id
    repo.create = create
    repo.update = update
    repo.delete = delete

    return repo


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


class TestApplicationInitialization:
    """Integration tests for application initialization and configuration"""

    def test_app_starts_successfully(self) -> None:
        """Test that app starts successfully using create_app factory"""
        app_instance = create_app()

        assert app_instance is not None
        assert app_instance.title == "Task Manager API"
        assert app_instance.description == "A RESTful API for managing tasks"
        assert app_instance.version == "1.0.0"

    def test_all_routes_are_registered(self, client: TestClient) -> None:
        """Test that all routes are registered correctly"""
        # Test health route is registered
        response = client.get("/health")
        assert response.status_code == 200

        # Test task routes are registered with /api prefix
        response = client.get("/api/tasks")
        assert response.status_code == 200

        # Test individual task route
        response = client.post(
            "/api/tasks",
            json={"title": "Test", "description": "Test"}
        )
        assert response.status_code == 201
        task_id = response.json()["id"]

        response = client.get(f"/api/tasks/{task_id}")
        assert response.status_code == 200

        response = client.put(
            f"/api/tasks/{task_id}",
            json={"title": "Updated"}
        )
        assert response.status_code == 200

        response = client.delete(f"/api/tasks/{task_id}")
        assert response.status_code == 204

    def test_cors_is_configured(self, client: TestClient) -> None:
        """Test that CORS middleware is configured correctly"""
        # Make request with Origin header
        response = client.get(
            "/api/tasks",
            headers={"Origin": "http://localhost:3000"}
        )

        # Check CORS headers are present
        assert "access-control-allow-origin" in response.headers
        cors_header = response.headers["access-control-allow-origin"]
        assert cors_header == "http://localhost:3000"

    def test_openapi_docs_accessible(self, client: TestClient) -> None:
        """Test that OpenAPI documentation is accessible"""
        # Test OpenAPI JSON endpoint
        response = client.get("/openapi.json")
        assert response.status_code == 200

        openapi_spec = response.json()
        assert openapi_spec["info"]["title"] == "Task Manager API"
        spec_desc = "A RESTful API for managing tasks"
        assert openapi_spec["info"]["description"] == spec_desc
        assert openapi_spec["info"]["version"] == "1.0.0"

        # Verify routes are documented
        assert "/health" in openapi_spec["paths"]
        assert "/api/tasks" in openapi_spec["paths"]
        assert "/api/tasks/{task_id}" in openapi_spec["paths"]

        # Test Swagger UI endpoint
        response = client.get("/docs")
        assert response.status_code == 200

        # Test ReDoc endpoint
        response = client.get("/redoc")
        assert response.status_code == 200


class TestHealthEndpoint:
    """Test suite for /health endpoint"""

    def test_health_endpoint_success(self, client: TestClient) -> None:
        """Test successful response from /health endpoint"""
        response = client.get("/health")

        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"

    def test_health_endpoint_json_structure(self, client: TestClient) -> None:
        """Test that /health returns correct JSON structure"""
        response = client.get("/health")
        data = response.json()

        # Verify required key is present
        assert "status" in data

        # Verify it only contains the status key
        assert len(data) == 1

    def test_health_endpoint_status_value(self, client: TestClient) -> None:
        """Test that /health returns 'healthy' status"""
        response = client.get("/health")
        data = response.json()

        assert data["status"] == "healthy"
        assert isinstance(data["status"], str)

    def test_health_endpoint_multiple_calls(self, client: TestClient) -> None:
        """Test that multiple calls to /health are consistent"""
        for _ in range(5):
            response = client.get("/health")
            data = response.json()

            assert response.status_code == 200
            assert data["status"] == "healthy"

    def test_health_endpoint_with_trailing_slash(
        self, client: TestClient
    ) -> None:
        """Test /health endpoint with trailing slash (should fail)"""
        response = client.get("/health/")

        # FastAPI by default doesn't redirect, so this should return 404
        assert response.status_code == 404

    def test_health_endpoint_wrong_methods(self, client: TestClient) -> None:
        """Test that only GET method is allowed on /health"""
        assert client.post("/health").status_code == 405
        assert client.put("/health").status_code == 405
        assert client.delete("/health").status_code == 405


class TestCORSConfiguration:
    """Test suite for CORS middleware configuration"""

    def test_cors_headers_present(self, client: TestClient) -> None:
        """Test that CORS headers are present in responses"""
        response = client.get(
            "/api/tasks",
            headers={"Origin": "http://localhost:3000"}
        )

        # CORS headers should be present
        assert "access-control-allow-origin" in response.headers

    def test_cors_allows_frontend_origin(self, client: TestClient) -> None:
        """Test that CORS allows requests from frontend origin"""
        response = client.get(
            "/api/tasks",
            headers={"Origin": "http://localhost:3000"}
        )

        assert response.status_code == 200
        cors_header = response.headers.get("access-control-allow-origin")
        assert cors_header == "http://localhost:3000"


class TestApplicationRoutes:
    """Test suite for general application routing"""

    def test_nonexistent_route_returns_404(self, client: TestClient) -> None:
        """Test that accessing non-existent route returns 404"""
        response = client.get("/nonexistent")

        assert response.status_code == 404

    def test_root_path_returns_404(self, client: TestClient) -> None:
        """Test that root path returns 404 (no root endpoint defined)"""
        response = client.get("/")

        assert response.status_code == 404


class TestTaskAPIEndpoints:
    """Unit tests for task API endpoints"""

    def test_get_all_tasks_returns_list(self, client: TestClient) -> None:
        """Test GET /api/tasks returns a list of tasks"""
        response = client.get("/api/tasks")
        assert response.status_code == 200
        data = response.json()
        assert "tasks" in data
        assert isinstance(data["tasks"], list)

    def test_post_task_valid_data(self, client: TestClient) -> None:
        """Test POST /api/tasks with valid data"""
        response = client.post(
            "/api/tasks",
            json={"title": "New Task", "description": "Task description"}
        )

        assert response.status_code == 201
        task = response.json()
        assert task["title"] == "New Task"
        assert task["description"] == "Task description"
        assert task["completed"] is False
        assert "id" in task
        assert "created_at" in task
        assert "updated_at" in task

    def test_post_task_invalid_empty_title(self, client: TestClient) -> None:
        """Test POST /api/tasks with empty title"""
        response = client.post(
            "/api/tasks",
            json={"title": "", "description": "Description"}
        )

        assert response.status_code == 422

    def test_post_task_invalid_whitespace_title(
        self, client: TestClient
    ) -> None:
        """Test POST /api/tasks with whitespace-only title"""
        response = client.post(
            "/api/tasks",
            json={"title": "   ", "description": "Description"}
        )

        assert response.status_code == 422

    def test_post_task_title_too_long(self, client: TestClient) -> None:
        """Test POST /api/tasks with title exceeding 200 characters"""
        long_title = "a" * 201
        response = client.post(
            "/api/tasks",
            json={"title": long_title, "description": "Description"}
        )

        assert response.status_code == 422

    def test_post_task_description_too_long(self, client: TestClient) -> None:
        """Test POST /api/tasks with description exceeding 1000 chars"""
        long_description = "a" * 1001
        response = client.post(
            "/api/tasks",
            json={"title": "Valid Title", "description": long_description}
        )

        assert response.status_code == 422

    def test_get_task_by_id_non_existent(self, client: TestClient) -> None:
        """Test GET /api/tasks/{id} with non-existent ID"""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = client.get(f"/api/tasks/{fake_id}")

        assert response.status_code == 404

    def test_put_task_non_existent(self, client: TestClient) -> None:
        """Test PUT /api/tasks/{id} with non-existent ID"""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = client.put(
            f"/api/tasks/{fake_id}",
            json={"title": "Updated Title"}
        )

        assert response.status_code == 404

    def test_delete_task_non_existent(self, client: TestClient) -> None:
        """Test DELETE /api/tasks/{id} with non-existent ID"""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = client.delete(f"/api/tasks/{fake_id}")

        assert response.status_code == 404


# Property-Based Tests
class TestTaskCreationProperties:
    """Property-based tests for task creation and management"""

    @given(st.text().filter(lambda s: not s or not s.strip()))
    @settings(
        max_examples=10,
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        deadline=1000
    )
    def test_property_empty_title_rejection(
        self, client: TestClient, empty_title: str
    ) -> None:
        """
        Property: Empty title rejection
        For any string composed entirely of whitespace or empty string,
        attempting to create a task with that title should result in a
        validation error (422 status).
        """
        response = client.post(
            "/api/tasks",
            json={"title": empty_title, "description": "Test description"}
        )

        # Should return validation error
        assert response.status_code == 422

    @given(
        st.text(min_size=1, max_size=200).filter(lambda s: s.strip()),
        st.text(max_size=1000),
    )
    @settings(
        max_examples=10,
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        deadline=2000
    )
    def test_property_restful_status_codes(
        self, client: TestClient, title: str, description: str
    ) -> None:
        """
        Property: RESTful status codes
        Successful creates return 201, successful updates/gets return 200,
        successful deletes return 204, validation errors return 422,
        and not-found errors return 404.
        """
        # Test POST returns 201 for successful create
        create_response = client.post(
            "/api/tasks",
            json={"title": title.strip(), "description": description}
        )
        assert create_response.status_code == 201
        task_id = create_response.json()["id"]

        # Test GET returns 200 for successful retrieval
        get_response = client.get(f"/api/tasks/{task_id}")
        assert get_response.status_code == 200

        # Test PUT returns 200 for successful update
        update_response = client.put(
            f"/api/tasks/{task_id}",
            json={
                "title": "Updated " + title.strip()[:50],
                "completed": True
            },
        )
        assert update_response.status_code == 200

        # Test DELETE returns 204 for successful delete
        delete_response = client.delete(f"/api/tasks/{task_id}")
        assert delete_response.status_code == 204

        # Test GET returns 404 for non-existent task
        not_found_response = client.get(f"/api/tasks/{task_id}")
        assert not_found_response.status_code == 404

        # Test POST returns 422 for validation error (empty title)
        validation_error = client.post(
            "/api/tasks",
            json={"title": "", "description": "Test"}
        )
        assert validation_error.status_code == 422
