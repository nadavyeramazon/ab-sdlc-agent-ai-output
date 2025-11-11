"""Comprehensive test suite for FastAPI backend.

Tests all endpoints, CORS configuration, response formats,
and error handling scenarios.
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime
import re
from main import app

# Create test client
client = TestClient(app)


class TestHealthEndpoint:
    """Test suite for /health endpoint."""
    
    def test_health_returns_200(self):
        """Test that health endpoint returns 200 OK status."""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_returns_json(self):
        """Test that health endpoint returns JSON content type."""
        response = client.get("/health")
        assert response.headers["content-type"] == "application/json"
    
    def test_health_returns_correct_structure(self):
        """Test that health endpoint returns correct JSON structure."""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
    
    def test_health_response_time(self):
        """Test that health endpoint responds quickly (< 100ms)."""
        import time
        start = time.time()
        response = client.get("/health")
        elapsed = (time.time() - start) * 1000  # Convert to ms
        assert response.status_code == 200
        assert elapsed < 100, f"Response time {elapsed}ms exceeds 100ms threshold"


class TestHelloEndpoint:
    """Test suite for /api/hello endpoint."""
    
    def test_hello_returns_200(self):
        """Test that hello endpoint returns 200 OK status."""
        response = client.get("/api/hello")
        assert response.status_code == 200
    
    def test_hello_returns_json(self):
        """Test that hello endpoint returns JSON content type."""
        response = client.get("/api/hello")
        assert response.headers["content-type"] == "application/json"
    
    def test_hello_returns_correct_structure(self):
        """Test that hello endpoint returns correct JSON structure."""
        response = client.get("/api/hello")
        data = response.json()
        
        # Check required fields exist
        assert "message" in data
        assert "timestamp" in data
        
        # Check field types
        assert isinstance(data["message"], str)
        assert isinstance(data["timestamp"], str)
    
    def test_hello_message_content(self):
        """Test that hello endpoint returns correct message."""
        response = client.get("/api/hello")
        data = response.json()
        assert data["message"] == "Hello World from Backend!"
    
    def test_hello_timestamp_format(self):
        """Test that timestamp is in ISO 8601 format."""
        response = client.get("/api/hello")
        data = response.json()
        timestamp = data["timestamp"]
        
        # Check ISO 8601 format with regex
        iso_pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z$"
        assert re.match(iso_pattern, timestamp), f"Timestamp {timestamp} is not in ISO 8601 format"
    
    def test_hello_timestamp_is_recent(self):
        """Test that timestamp is recent (within last 5 seconds)."""
        response = client.get("/api/hello")
        data = response.json()
        timestamp_str = data["timestamp"].replace("Z", "+00:00")
        timestamp = datetime.fromisoformat(timestamp_str)
        now = datetime.utcnow()
        
        # Check timestamp is recent (within 5 seconds)
        diff = abs((now - timestamp.replace(tzinfo=None)).total_seconds())
        assert diff < 5, f"Timestamp is {diff} seconds old, expected < 5 seconds"
    
    def test_hello_response_time(self):
        """Test that hello endpoint responds quickly (< 100ms)."""
        import time
        start = time.time()
        response = client.get("/api/hello")
        elapsed = (time.time() - start) * 1000  # Convert to ms
        assert response.status_code == 200
        assert elapsed < 100, f"Response time {elapsed}ms exceeds 100ms threshold"


class TestCORSConfiguration:
    """Test suite for CORS middleware configuration."""
    
    def test_cors_allows_localhost_3000(self):
        """Test that CORS allows requests from localhost:3000."""
        response = client.get(
            "/api/hello",
            headers={"Origin": "http://localhost:3000"}
        )
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers
        assert response.headers["access-control-allow-origin"] == "http://localhost:3000"
    
    def test_cors_preflight_request(self):
        """Test CORS preflight OPTIONS request."""
        response = client.options(
            "/api/hello",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET"
            }
        )
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers


class TestErrorHandling:
    """Test suite for error handling scenarios."""
    
    def test_invalid_endpoint_returns_404(self):
        """Test that invalid endpoint returns 404."""
        response = client.get("/api/invalid")
        assert response.status_code == 404
    
    def test_invalid_method_returns_405(self):
        """Test that invalid HTTP method returns 405."""
        response = client.post("/health")
        assert response.status_code == 405


class TestAPIDocumentation:
    """Test suite for API documentation endpoints."""
    
    def test_openapi_json_available(self):
        """Test that OpenAPI JSON schema is available."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert data["info"]["title"] == "Green Theme Hello World API"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
