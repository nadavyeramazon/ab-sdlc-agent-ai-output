"""Comprehensive tests for FastAPI backend.

Tests cover:
- API endpoints functionality
- Response format validation
- CORS headers
- Performance requirements
- Error handling
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime
import time
from main import app

client = TestClient(app)


class TestHealthEndpoint:
    """Test suite for /health endpoint."""

    def test_health_endpoint_returns_200(self):
        """Verify health endpoint returns 200 status code."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_endpoint_returns_json(self):
        """Verify health endpoint returns JSON content type."""
        response = client.get("/health")
        assert response.headers["content-type"] == "application/json"

    def test_health_endpoint_structure(self):
        """Verify health endpoint returns correct JSON structure."""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"

    def test_health_endpoint_performance(self):
        """Verify health endpoint responds within 100ms."""
        start_time = time.time()
        response = client.get("/health")
        duration = (time.time() - start_time) * 1000  # Convert to ms
        
        assert response.status_code == 200
        assert duration < 100, f"Response took {duration}ms, expected < 100ms"


class TestHelloEndpoint:
    """Test suite for /api/hello endpoint."""

    def test_hello_endpoint_returns_200(self):
        """Verify hello endpoint returns 200 status code."""
        response = client.get("/api/hello")
        assert response.status_code == 200

    def test_hello_endpoint_returns_json(self):
        """Verify hello endpoint returns JSON content type."""
        response = client.get("/api/hello")
        assert response.headers["content-type"] == "application/json"

    def test_hello_endpoint_structure(self):
        """Verify hello endpoint returns correct JSON structure."""
        response = client.get("/api/hello")
        data = response.json()
        
        # Check required fields exist
        assert "message" in data
        assert "timestamp" in data
        
        # Check message content
        assert data["message"] == "Hello World from Backend!"

    def test_hello_endpoint_timestamp_format(self):
        """Verify timestamp is in ISO 8601 format."""
        response = client.get("/api/hello")
        data = response.json()
        timestamp = data["timestamp"]
        
        # Verify timestamp can be parsed and is in ISO format
        try:
            # Remove 'Z' suffix and parse
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            assert isinstance(dt, datetime)
        except ValueError:
            pytest.fail(f"Timestamp '{timestamp}' is not in valid ISO 8601 format")

    def test_hello_endpoint_timestamp_is_recent(self):
        """Verify timestamp reflects current time (within 5 seconds)."""
        response = client.get("/api/hello")
        data = response.json()
        timestamp = data["timestamp"]
        
        # Parse timestamp
        response_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        current_time = datetime.utcnow()
        
        # Check timestamp is within 5 seconds of current time
        time_diff = abs((current_time - response_time.replace(tzinfo=None)).total_seconds())
        assert time_diff < 5, f"Timestamp is {time_diff} seconds off from current time"

    def test_hello_endpoint_performance(self):
        """Verify hello endpoint responds within 100ms."""
        start_time = time.time()
        response = client.get("/api/hello")
        duration = (time.time() - start_time) * 1000  # Convert to ms
        
        assert response.status_code == 200
        assert duration < 100, f"Response took {duration}ms, expected < 100ms"


class TestCORS:
    """Test suite for CORS configuration."""

    def test_cors_headers_present_on_health(self):
        """Verify CORS headers are present on health endpoint."""
        response = client.get("/health", headers={"Origin": "http://localhost:3000"})
        
        # CORS headers should be present
        assert "access-control-allow-origin" in response.headers

    def test_cors_headers_present_on_hello(self):
        """Verify CORS headers are present on hello endpoint."""
        response = client.get("/api/hello", headers={"Origin": "http://localhost:3000"})
        
        # CORS headers should be present
        assert "access-control-allow-origin" in response.headers

    def test_cors_allows_localhost_3000(self):
        """Verify CORS allows requests from http://localhost:3000."""
        response = client.get("/api/hello", headers={"Origin": "http://localhost:3000"})
        
        # Should allow the frontend origin
        assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"


class TestIntegration:
    """Integration tests for multiple endpoints."""

    def test_all_endpoints_accessible(self):
        """Verify all required endpoints are accessible."""
        # Health check
        health_response = client.get("/health")
        assert health_response.status_code == 200
        
        # Hello endpoint
        hello_response = client.get("/api/hello")
        assert hello_response.status_code == 200

    def test_multiple_requests_consistency(self):
        """Verify backend handles multiple requests consistently."""
        responses = []
        
        for _ in range(5):
            response = client.get("/api/hello")
            responses.append(response)
        
        # All should return 200
        for response in responses:
            assert response.status_code == 200
            data = response.json()
            assert data["message"] == "Hello World from Backend!"
            assert "timestamp" in data
