"""Comprehensive tests for the Hello World FastAPI application.

Tests cover all endpoints including root, hello, personalized greetings,
and health check functionality.
"""

import pytest
from fastapi.testclient import TestClient
from main import app

# Create test client
client = TestClient(app)


class TestRootEndpoint:
    """Test cases for the root endpoint."""
    
    def test_root_endpoint_returns_200(self):
        """Test that root endpoint returns 200 status code."""
        response = client.get("/")
        assert response.status_code == 200
    
    def test_root_endpoint_returns_json(self):
        """Test that root endpoint returns JSON response."""
        response = client.get("/")
        assert response.headers["content-type"] == "application/json"
    
    def test_root_endpoint_message(self):
        """Test that root endpoint returns correct message."""
        response = client.get("/")
        data = response.json()
        assert "message" in data
        assert data["message"] == "Welcome to the Hello World API"


class TestHelloEndpoint:
    """Test cases for the hello endpoint."""
    
    def test_hello_endpoint_returns_200(self):
        """Test that hello endpoint returns 200 status code."""
        response = client.get("/hello")
        assert response.status_code == 200
    
    def test_hello_endpoint_returns_json(self):
        """Test that hello endpoint returns JSON response."""
        response = client.get("/hello")
        assert response.headers["content-type"] == "application/json"
    
    def test_hello_endpoint_message(self):
        """Test that hello endpoint returns correct message."""
        response = client.get("/hello")
        data = response.json()
        assert "message" in data
        assert data["message"] == "Hello, World!"


class TestHelloNameEndpoint:
    """Test cases for the personalized hello endpoint."""
    
    def test_hello_name_returns_200(self):
        """Test that hello with name returns 200 status code."""
        response = client.get("/hello/John")
        assert response.status_code == 200
    
    def test_hello_name_returns_json(self):
        """Test that hello with name returns JSON response."""
        response = client.get("/hello/Alice")
        assert response.headers["content-type"] == "application/json"
    
    def test_hello_name_message(self):
        """Test that hello endpoint returns personalized message."""
        response = client.get("/hello/John")
        data = response.json()
        assert "message" in data
        assert data["message"] == "Hello, John!"
    
    def test_hello_name_different_names(self):
        """Test hello endpoint with different names."""
        names = ["Alice", "Bob", "Charlie", "Diana"]
        for name in names:
            response = client.get(f"/hello/{name}")
            data = response.json()
            assert data["message"] == f"Hello, {name}!"
    
    def test_hello_name_special_characters(self):
        """Test hello endpoint with special characters in name."""
        response = client.get("/hello/Mary-Jane")
        assert response.status_code == 200
        data = response.json()
        assert "Mary-Jane" in data["message"]
    
    def test_hello_name_unicode(self):
        """Test hello endpoint with unicode characters."""
        response = client.get("/hello/José")
        assert response.status_code == 200
        data = response.json()
        assert "José" in data["message"]


class TestHealthCheckEndpoint:
    """Test cases for the health check endpoint."""
    
    def test_health_check_returns_200(self):
        """Test that health check returns 200 status code."""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_check_returns_json(self):
        """Test that health check returns JSON response."""
        response = client.get("/health")
        assert response.headers["content-type"] == "application/json"
    
    def test_health_check_status(self):
        """Test that health check returns healthy status."""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
    
    def test_health_check_service_info(self):
        """Test that health check returns service information."""
        response = client.get("/health")
        data = response.json()
        assert "service" in data
        assert "version" in data
        assert data["service"] == "Hello World API"
        assert data["version"] == "1.0.0"


class TestAPIDocumentation:
    """Test cases for API documentation endpoints."""
    
    def test_openapi_schema_accessible(self):
        """Test that OpenAPI schema is accessible."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
    
    def test_docs_accessible(self):
        """Test that interactive docs are accessible."""
        response = client.get("/docs")
        assert response.status_code == 200
    
    def test_redoc_accessible(self):
        """Test that ReDoc documentation is accessible."""
        response = client.get("/redoc")
        assert response.status_code == 200


class TestErrorHandling:
    """Test cases for error handling."""
    
    def test_nonexistent_endpoint_returns_404(self):
        """Test that non-existent endpoint returns 404."""
        response = client.get("/nonexistent")
        assert response.status_code == 404
    
    def test_invalid_method_returns_405(self):
        """Test that invalid HTTP method returns 405."""
        response = client.post("/hello")
        assert response.status_code == 405


class TestResponseStructure:
    """Test cases for response structure and data types."""
    
    def test_all_responses_are_json(self):
        """Test that all successful responses return JSON."""
        endpoints = ["/", "/hello", "/hello/Test", "/health"]
        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.status_code == 200
            # Verify it's valid JSON by parsing it
            data = response.json()
            assert isinstance(data, dict)
    
    def test_message_responses_have_message_key(self):
        """Test that message endpoints have 'message' key."""
        endpoints = ["/", "/hello", "/hello/Test"]
        for endpoint in endpoints:
            response = client.get(endpoint)
            data = response.json()
            assert "message" in data
            assert isinstance(data["message"], str)
            assert len(data["message"]) > 0


# Integration tests
class TestIntegration:
    """Integration tests for the complete API."""
    
    def test_multiple_requests_consistency(self):
        """Test that multiple requests return consistent results."""
        for _ in range(5):
            response = client.get("/hello")
            assert response.status_code == 200
            data = response.json()
            assert data["message"] == "Hello, World!"
    
    def test_all_endpoints_accessible(self):
        """Test that all main endpoints are accessible."""
        endpoints = [
            ("/", 200),
            ("/hello", 200),
            ("/hello/TestUser", 200),
            ("/health", 200),
            ("/docs", 200),
            ("/openapi.json", 200)
        ]
        
        for endpoint, expected_status in endpoints:
            response = client.get(endpoint)
            assert response.status_code == expected_status, \
                f"Endpoint {endpoint} returned {response.status_code}, expected {expected_status}"
