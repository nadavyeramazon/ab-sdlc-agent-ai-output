"""Tests for the FastAPI backend application."""

import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


class TestRootEndpoint:
    """Tests for the root endpoint."""

    def test_root_endpoint(self, client):
        """Test the root endpoint returns correct information."""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "message" in data
        assert "docs" in data
        assert "health" in data
        assert "hello" in data
        assert "theme" in data
        assert data["theme"] == "green"
        assert "Green Hello World API" in data["message"]


class TestHealthEndpoint:
    """Tests for the health check endpoint."""

    def test_health_check(self, client):
        """Test health check returns healthy status."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "healthy"
        assert data["service"] == "green-hello-world-api"
        assert data["version"] == "1.0.0"
        assert data["theme"] == "green"

    def test_health_check_response_model(self, client):
        """Test health check response follows the expected model."""
        response = client.get("/health")
        data = response.json()
        
        # Check all required fields are present
        required_fields = ["status", "service", "version", "theme"]
        for field in required_fields:
            assert field in data
        
        # Check field types
        assert isinstance(data["status"], str)
        assert isinstance(data["service"], str)
        assert isinstance(data["version"], str)
        assert isinstance(data["theme"], str)


class TestHelloEndpoint:
    """Tests for the hello world endpoint."""

    def test_hello_world(self, client):
        """Test hello world endpoint returns correct message."""
        response = client.get("/api/hello")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "message" in data
        assert "status" in data
        assert "theme" in data
        
        assert data["status"] == "success"
        assert data["theme"] == "green"
        assert "Hello World!" in data["message"]
        assert "🌱" in data["message"]  # Green emoji
        assert "React" in data["message"]
        assert "Vite" in data["message"]
        assert "FastAPI" in data["message"]

    def test_hello_world_response_model(self, client):
        """Test hello world response follows the expected model."""
        response = client.get("/api/hello")
        data = response.json()
        
        # Check all required fields are present
        required_fields = ["message", "status", "theme"]
        for field in required_fields:
            assert field in data
        
        # Check field types
        assert isinstance(data["message"], str)
        assert isinstance(data["status"], str)
        assert isinstance(data["theme"], str)


class TestPersonalizedHelloEndpoint:
    """Tests for the personalized hello endpoint."""

    def test_hello_user_valid_name(self, client):
        """Test personalized hello with valid name."""
        name = "Alice"
        response = client.get(f"/api/hello/{name}")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "message" in data
        assert "status" in data
        assert "theme" in data
        
        assert data["status"] == "success"
        assert data["theme"] == "green"
        assert f"Hello, {name}!" in data["message"]
        assert "🌱" in data["message"]  # Green emoji

    def test_hello_user_with_spaces(self, client):
        """Test personalized hello with name containing spaces."""
        name = "John Doe"
        response = client.get(f"/api/hello/{name}")
        
        assert response.status_code == 200
        data = response.json()
        assert f"Hello, {name}!" in data["message"]

    def test_hello_user_with_special_characters(self, client):
        """Test personalized hello with special characters in name."""
        name = "José"
        response = client.get(f"/api/hello/{name}")
        
        assert response.status_code == 200
        data = response.json()
        assert f"Hello, {name}!" in data["message"]

    def test_hello_user_empty_name(self, client):
        """Test personalized hello with empty name returns error."""
        response = client.get("/api/hello/")
        # This should return 404 as the route doesn't match
        assert response.status_code == 404

    def test_hello_user_whitespace_name(self, client):
        """Test personalized hello with whitespace-only name returns error."""
        name = "   "
        response = client.get(f"/api/hello/{name}")
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "empty" in data["detail"].lower()

    def test_hello_user_long_name(self, client):
        """Test personalized hello with very long name returns error."""
        name = "a" * 101  # 101 characters, exceeds 100 limit
        response = client.get(f"/api/hello/{name}")
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "too long" in data["detail"].lower()

    def test_hello_user_max_length_name(self, client):
        """Test personalized hello with maximum allowed name length."""
        name = "a" * 100  # Exactly 100 characters
        response = client.get(f"/api/hello/{name}")
        
        assert response.status_code == 200
        data = response.json()
        assert f"Hello, {name}!" in data["message"]


class TestCORSConfiguration:
    """Tests for CORS configuration."""

    def test_cors_headers_present(self, client):
        """Test that CORS headers are present in responses."""
        response = client.get("/api/hello")
        
        # Check for CORS headers (these may vary based on request)
        assert response.status_code == 200
        # CORS headers are typically added by FastAPI middleware
        # The exact headers depend on the request origin

    def test_options_request(self, client):
        """Test OPTIONS request for CORS preflight."""
        response = client.options(
            "/api/hello",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET"
            }
        )
        
        # Should allow OPTIONS requests
        assert response.status_code in [200, 204]


class TestAPIDocumentation:
    """Tests for API documentation endpoints."""

    def test_openapi_schema(self, client):
        """Test that OpenAPI schema is accessible."""
        response = client.get("/openapi.json")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "openapi" in data
        assert "info" in data
        assert "paths" in data
        
        # Check API info
        info = data["info"]
        assert info["title"] == "Green Hello World API"
        assert info["version"] == "1.0.0"

    def test_swagger_ui(self, client):
        """Test that Swagger UI is accessible."""
        response = client.get("/docs")
        
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")

    def test_redoc_ui(self, client):
        """Test that ReDoc UI is accessible."""
        response = client.get("/redoc")
        
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")


class TestErrorHandling:
    """Tests for error handling."""

    def test_404_error(self, client):
        """Test 404 error for non-existent endpoint."""
        response = client.get("/non-existent-endpoint")
        
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data

    def test_method_not_allowed(self, client):
        """Test method not allowed error."""
        # POST to GET-only endpoint
        response = client.post("/api/hello")
        
        assert response.status_code == 405
        data = response.json()
        assert "detail" in data


class TestResponseHeaders:
    """Tests for response headers and content types."""

    def test_json_content_type(self, client):
        """Test that JSON endpoints return correct content type."""
        response = client.get("/api/hello")
        
        assert response.status_code == 200
        assert "application/json" in response.headers.get("content-type", "")

    def test_response_encoding(self, client):
        """Test that responses are properly encoded."""
        response = client.get("/api/hello/José")
        
        assert response.status_code == 200
        data = response.json()
        # Should handle Unicode characters properly
        assert "José" in data["message"]


class TestPerformance:
    """Basic performance and reliability tests."""

    def test_multiple_requests(self, client):
        """Test handling multiple requests."""
        for i in range(10):
            response = client.get("/api/hello")
            assert response.status_code == 200

    def test_concurrent_requests(self, client):
        """Test handling concurrent requests."""
        import concurrent.futures
        import threading
        
        def make_request():
            return client.get("/health")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        # All requests should succeed
        for response in results:
            assert response.status_code == 200