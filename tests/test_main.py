"""Comprehensive tests for the Hello World API.

This module contains tests for all endpoints in the FastAPI application.
"""

import pytest
from fastapi.testclient import TestClient
from main import app

# Create test client
client = TestClient(app)


class TestRootEndpoint:
    """Tests for the root endpoint."""
    
    def test_root_endpoint_success(self):
        """Test that root endpoint returns correct message."""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello World"}
    
    def test_root_endpoint_response_type(self):
        """Test that root endpoint returns JSON."""
        response = client.get("/")
        assert response.headers["content-type"] == "application/json"
    
    def test_root_endpoint_has_message_key(self):
        """Test that response contains 'message' key."""
        response = client.get("/")
        data = response.json()
        assert "message" in data
        assert isinstance(data["message"], str)


class TestHealthCheckEndpoint:
    """Tests for the health check endpoint."""
    
    def test_health_check_success(self):
        """Test that health check returns healthy status."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}
    
    def test_health_check_response_structure(self):
        """Test that health check response has correct structure."""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"


class TestHelloNameEndpoint:
    """Tests for the personalized hello endpoint."""
    
    def test_hello_with_name(self):
        """Test personalized greeting with a name."""
        response = client.get("/hello/Alice")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello Alice!"}
    
    def test_hello_with_different_names(self):
        """Test personalized greeting with multiple names."""
        test_names = ["Bob", "Charlie", "David", "Eve"]
        for name in test_names:
            response = client.get(f"/hello/{name}")
            assert response.status_code == 200
            assert response.json() == {"message": f"Hello {name}!"}
    
    def test_hello_with_special_characters(self):
        """Test personalized greeting with special characters in name."""
        response = client.get("/hello/John-Doe")
        assert response.status_code == 200
        assert "John-Doe" in response.json()["message"]
    
    def test_hello_with_unicode_name(self):
        """Test personalized greeting with unicode characters."""
        response = client.get("/hello/José")
        assert response.status_code == 200
        assert "José" in response.json()["message"]
    
    def test_hello_response_format(self):
        """Test that hello endpoint returns correct format."""
        response = client.get("/hello/TestUser")
        data = response.json()
        assert "message" in data
        assert isinstance(data["message"], str)
        assert data["message"].startswith("Hello ")
        assert data["message"].endswith("!")


class TestAPIMetadata:
    """Tests for API metadata and documentation."""
    
    def test_openapi_schema_exists(self):
        """Test that OpenAPI schema is accessible."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
    
    def test_api_title_and_version(self):
        """Test API metadata in OpenAPI schema."""
        response = client.get("/openapi.json")
        schema = response.json()
        assert schema["info"]["title"] == "Hello World API"
        assert schema["info"]["version"] == "1.0.0"
    
    def test_docs_endpoint_accessible(self):
        """Test that Swagger UI docs are accessible."""
        response = client.get("/docs")
        assert response.status_code == 200


class TestErrorHandling:
    """Tests for error handling and edge cases."""
    
    def test_nonexistent_endpoint(self):
        """Test that nonexistent endpoints return 404."""
        response = client.get("/nonexistent")
        assert response.status_code == 404
    
    def test_invalid_method_on_root(self):
        """Test that invalid HTTP methods are rejected."""
        response = client.post("/")
        assert response.status_code == 405  # Method Not Allowed
    
    def test_invalid_method_on_health(self):
        """Test that health endpoint only accepts GET."""
        response = client.put("/health")
        assert response.status_code == 405


class TestConcurrency:
    """Tests for concurrent requests."""
    
    def test_multiple_concurrent_requests(self):
        """Test that API handles multiple requests correctly."""
        responses = []
        for i in range(10):
            response = client.get("/")
            responses.append(response)
        
        # All requests should succeed
        for response in responses:
            assert response.status_code == 200
            assert response.json() == {"message": "Hello World"}


# Parametrized tests for better coverage
@pytest.mark.parametrize("endpoint,expected_status", [
    ("/", 200),
    ("/health", 200),
    ("/hello/Test", 200),
])
def test_endpoints_status_codes(endpoint, expected_status):
    """Parametrized test for endpoint status codes."""
    response = client.get(endpoint)
    assert response.status_code == expected_status


@pytest.mark.parametrize("name,expected_message", [
    ("Alice", "Hello Alice!"),
    ("Bob", "Hello Bob!"),
    ("123", "Hello 123!"),
    ("test_user", "Hello test_user!"),
])
def test_hello_endpoint_parametrized(name, expected_message):
    """Parametrized test for hello endpoint with different names."""
    response = client.get(f"/hello/{name}")
    assert response.status_code == 200
    assert response.json() == {"message": expected_message}
