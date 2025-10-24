"""Unit tests for the FastAPI Hello World application.

This module contains comprehensive tests for all endpoints and error cases.
"""

import pytest
from fastapi.testclient import TestClient
from main import app, __version__


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


class TestHealthEndpoint:
    """Tests for the /health endpoint."""

    def test_health_endpoint_success(self, client):
        """Test that the health endpoint returns 200 OK."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    def test_health_endpoint_response_structure(self, client):
        """Test that the health endpoint returns correct JSON structure."""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert isinstance(data["status"], str)
        assert data["status"] == "healthy"


class TestHelloEndpoint:
    """Tests for the /hello endpoint."""

    def test_hello_endpoint_success(self, client):
        """Test that the hello endpoint returns 200 OK."""
        response = client.get("/hello")
        assert response.status_code == 200

    def test_hello_endpoint_response_structure(self, client):
        """Test that the hello endpoint returns correct JSON structure."""
        response = client.get("/hello")
        data = response.json()
        assert "message" in data
        assert isinstance(data["message"], str)
        assert data["message"] == "Hello, World!"

    def test_hello_endpoint_content_type(self, client):
        """Test that the hello endpoint returns JSON content type."""
        response = client.get("/hello")
        assert response.headers["content-type"] == "application/json"


class TestRootEndpoint:
    """Tests for the root / endpoint."""

    def test_root_endpoint_success(self, client):
        """Test that the root endpoint returns 200 OK."""
        response = client.get("/")
        assert response.status_code == 200

    def test_root_endpoint_response_structure(self, client):
        """Test that the root endpoint returns correct JSON structure."""
        response = client.get("/")
        data = response.json()
        assert "service" in data
        assert "version" in data
        assert "status" in data
        assert isinstance(data["service"], str)
        assert isinstance(data["version"], str)
        assert isinstance(data["status"], str)

    def test_root_endpoint_version(self, client):
        """Test that the root endpoint returns correct version."""
        response = client.get("/")
        data = response.json()
        assert data["version"] == __version__

    def test_root_endpoint_service_name(self, client):
        """Test that the root endpoint returns correct service name."""
        response = client.get("/")
        data = response.json()
        assert data["service"] == "ab-sdlc-agent-ai-backend"

    def test_root_endpoint_status(self, client):
        """Test that the root endpoint returns running status."""
        response = client.get("/")
        data = response.json()
        assert data["status"] == "running"


class TestErrorHandling:
    """Tests for error handling and edge cases."""

    def test_nonexistent_endpoint_returns_404(self, client):
        """Test that non-existent endpoints return 404."""
        response = client.get("/nonexistent")
        assert response.status_code == 404

    def test_nonexistent_endpoint_json_response(self, client):
        """Test that 404 errors return JSON response."""
        response = client.get("/nonexistent")
        data = response.json()
        assert "detail" in data

    def test_method_not_allowed_post_on_get_endpoint(self, client):
        """Test that POST on GET-only endpoints returns 405."""
        response = client.post("/hello")
        assert response.status_code == 405

    def test_method_not_allowed_put_on_get_endpoint(self, client):
        """Test that PUT on GET-only endpoints returns 405."""
        response = client.put("/health")
        assert response.status_code == 405

    def test_method_not_allowed_delete_on_get_endpoint(self, client):
        """Test that DELETE on GET-only endpoints returns 405."""
        response = client.delete("/")
        assert response.status_code == 405


class TestAPIDocumentation:
    """Tests for API documentation endpoints."""

    def test_openapi_schema_available(self, client):
        """Test that OpenAPI schema is available."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert "paths" in data

    def test_swagger_ui_available(self, client):
        """Test that Swagger UI is available."""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_redoc_available(self, client):
        """Test that ReDoc is available."""
        response = client.get("/redoc")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]


class TestCORS:
    """Tests for CORS configuration."""

    def test_cors_headers_present(self, client):
        """Test that CORS headers are present in responses."""
        response = client.get("/hello")
        assert "access-control-allow-origin" in response.headers

    def test_cors_allows_all_origins(self, client):
        """Test that CORS allows all origins."""
        response = client.get(
            "/hello",
            headers={"Origin": "http://example.com"}
        )
        assert response.headers.get("access-control-allow-origin") == "*"

    def test_cors_preflight_request(self, client):
        """Test CORS preflight OPTIONS request."""
        response = client.options(
            "/hello",
            headers={
                "Origin": "http://example.com",
                "Access-Control-Request-Method": "GET"
            }
        )
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers


@pytest.mark.asyncio
class TestAsyncBehavior:
    """Tests for async endpoint behavior."""

    @pytest.mark.asyncio
    async def test_concurrent_requests(self, client):
        """Test that multiple concurrent requests are handled correctly."""
        import asyncio
        
        def make_request():
            return client.get("/hello")
        
        # Make 10 concurrent requests
        responses = [make_request() for _ in range(10)]
        
        # All should succeed
        for response in responses:
            assert response.status_code == 200
            assert response.json() == {"message": "Hello, World!"}


class TestResponseHeaders:
    """Tests for response headers."""

    def test_content_type_json(self, client):
        """Test that all JSON endpoints return correct content-type."""
        endpoints = ["/", "/health", "/hello"]
        for endpoint in endpoints:
            response = client.get(endpoint)
            assert "application/json" in response.headers["content-type"]

    def test_response_has_content_length(self, client):
        """Test that responses include content-length header."""
        response = client.get("/hello")
        assert "content-length" in response.headers
        assert int(response.headers["content-length"]) > 0
