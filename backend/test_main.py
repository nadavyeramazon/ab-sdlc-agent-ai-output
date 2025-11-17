"""Comprehensive tests for FastAPI backend.

Tests cover:
- API endpoint functionality
- Response format validation
- CORS headers
- Health check
- Error handling
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime
import re
from main import app

# Create test client
client = TestClient(app)


class TestHelloEndpoint:
    """Test cases for /api/hello endpoint."""

    def test_hello_endpoint_returns_200(self):
        """Test that /api/hello returns 200 OK status."""
        response = client.get("/api/hello")
        assert response.status_code == 200

    def test_hello_endpoint_returns_correct_message(self):
        """Test that /api/hello returns the expected message."""
        response = client.get("/api/hello")
        data = response.json()
        assert data["message"] == "Hello World from Backend!"

    def test_hello_endpoint_includes_timestamp(self):
        """Test that /api/hello includes a timestamp field."""
        response = client.get("/api/hello")
        data = response.json()
        assert "timestamp" in data
        assert data["timestamp"] is not None

    def test_hello_endpoint_timestamp_is_iso8601(self):
        """Test that timestamp is in valid ISO 8601 format."""
        response = client.get("/api/hello")
        data = response.json()
        timestamp = data["timestamp"]
        
        # Check ISO 8601 format with regex
        iso8601_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$'
        assert re.match(iso8601_pattern, timestamp), f"Timestamp {timestamp} is not in ISO 8601 format"
        
        # Verify it can be parsed
        try:
            datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except ValueError:
            pytest.fail(f"Timestamp {timestamp} cannot be parsed as datetime")

    def test_hello_endpoint_content_type(self):
        """Test that /api/hello returns JSON content type."""
        response = client.get("/api/hello")
        assert response.headers["content-type"] == "application/json"

    def test_hello_endpoint_cors_headers(self):
        """Test that CORS headers are present for frontend origin."""
        response = client.get(
            "/api/hello",
            headers={"Origin": "http://localhost:3000"}
        )
        assert "access-control-allow-origin" in response.headers

    def test_hello_endpoint_response_structure(self):
        """Test that response has exactly the expected structure."""
        response = client.get("/api/hello")
        data = response.json()
        assert set(data.keys()) == {"message", "timestamp"}


class TestHealthEndpoint:
    """Test cases for /health endpoint."""

    def test_health_endpoint_returns_200(self):
        """Test that /health returns 200 OK status."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_endpoint_returns_healthy_status(self):
        """Test that /health returns healthy status."""
        response = client.get("/health")
        data = response.json()
        assert data["status"] == "healthy"

    def test_health_endpoint_content_type(self):
        """Test that /health returns JSON content type."""
        response = client.get("/health")
        assert response.headers["content-type"] == "application/json"

    def test_health_endpoint_response_structure(self):
        """Test that response has exactly the expected structure."""
        response = client.get("/health")
        data = response.json()
        assert set(data.keys()) == {"status"}


class TestPerformance:
    """Test cases for performance requirements."""

    def test_hello_endpoint_response_time(self):
        """Test that /api/hello responds within 100ms."""
        import time
        start = time.time()
        response = client.get("/api/hello")
        end = time.time()
        
        response_time_ms = (end - start) * 1000
        assert response.status_code == 200
        # Allow some margin for test environment
        assert response_time_ms < 200, f"Response time {response_time_ms}ms exceeds limit"

    def test_health_endpoint_response_time(self):
        """Test that /health responds within 100ms."""
        import time
        start = time.time()
        response = client.get("/health")
        end = time.time()
        
        response_time_ms = (end - start) * 1000
        assert response.status_code == 200
        assert response_time_ms < 200, f"Response time {response_time_ms}ms exceeds limit"


class TestCORS:
    """Test cases for CORS configuration."""

    def test_cors_allows_localhost_3000(self):
        """Test that CORS allows requests from localhost:3000."""
        response = client.get(
            "/api/hello",
            headers={"Origin": "http://localhost:3000"}
        )
        assert response.status_code == 200
        assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"

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
