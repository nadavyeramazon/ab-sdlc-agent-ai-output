"""Unit tests for FastAPI backend application.

This module contains comprehensive tests for all API endpoints:
- Root endpoint (/)
- Health check endpoint (/health)
- Hello API endpoint (/api/hello)

Run tests with: pytest
Run with coverage: pytest --cov=main --cov-report=html
"""

import pytest
from fastapi.testclient import TestClient
from main import app

# Create a test client
client = TestClient(app)


class TestRootEndpoint:
    """Test cases for the root endpoint."""

    def test_root_endpoint_success(self):
        """Test that root endpoint returns correct message."""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello World from FastAPI Backend!"}

    def test_root_endpoint_content_type(self):
        """Test that root endpoint returns JSON content type."""
        response = client.get("/")
        assert response.headers["content-type"] == "application/json"


class TestHealthEndpoint:
    """Test cases for the health check endpoint."""

    def test_health_endpoint_success(self):
        """Test that health endpoint returns healthy status."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    def test_health_endpoint_content_type(self):
        """Test that health endpoint returns JSON content type."""
        response = client.get("/health")
        assert response.headers["content-type"] == "application/json"


class TestHelloAPIEndpoint:
    """Test cases for the /api/hello endpoint."""

    def test_hello_api_success(self):
        """Test that hello API returns correct message and structure."""
        response = client.get("/api/hello")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "status" in data
        assert "service" in data
        
        assert data["message"] == "Hello from the backend!"
        assert data["status"] == "success"
        assert data["service"] == "FastAPI Backend"

    def test_hello_api_content_type(self):
        """Test that hello API returns JSON content type."""
        response = client.get("/api/hello")
        assert response.headers["content-type"] == "application/json"

    def test_hello_api_response_structure(self):
        """Test that hello API response has all required fields."""
        response = client.get("/api/hello")
        data = response.json()
        
        # Ensure all expected keys are present
        expected_keys = {"message", "status", "service"}
        assert set(data.keys()) == expected_keys


class TestCORSConfiguration:
    """Test cases for CORS configuration."""

    def test_cors_headers_present(self):
        """Test that CORS headers are properly set."""
        response = client.get("/", headers={"Origin": "http://localhost:3000"})
        assert response.status_code == 200
        # CORS headers should be present
        assert "access-control-allow-origin" in response.headers

    def test_options_request(self):
        """Test that OPTIONS requests are handled for CORS preflight."""
        response = client.options(
            "/api/hello",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET"
            }
        )
        assert response.status_code == 200


class TestInvalidEndpoints:
    """Test cases for invalid endpoints."""

    def test_invalid_endpoint_404(self):
        """Test that invalid endpoints return 404."""
        response = client.get("/invalid/endpoint")
        assert response.status_code == 404

    def test_invalid_method_405(self):
        """Test that invalid HTTP methods return 405."""
        response = client.post("/health")
        assert response.status_code == 405


class TestApplicationMetadata:
    """Test cases for application metadata and configuration."""

    def test_openapi_docs_available(self):
        """Test that OpenAPI documentation is available."""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_openapi_json_available(self):
        """Test that OpenAPI JSON schema is available."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        # Verify it's valid JSON
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert data["info"]["title"] == "Hello World Backend API"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
