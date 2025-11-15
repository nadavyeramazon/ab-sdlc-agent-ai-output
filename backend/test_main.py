"""Comprehensive test suite for the FastAPI backend.

Tests cover:
- /api/hello endpoint functionality
- /health endpoint functionality
- Response structure validation
- CORS headers verification
- Timestamp format validation
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime
import re
from main import app

# Create test client
client = TestClient(app)


class TestHelloEndpoint:
    """Test suite for /api/hello endpoint."""

    def test_hello_endpoint_returns_200(self):
        """Test that /api/hello returns 200 OK status."""
        response = client.get("/api/hello")
        assert response.status_code == 200

    def test_hello_endpoint_returns_json(self):
        """Test that /api/hello returns JSON content type."""
        response = client.get("/api/hello")
        assert response.headers["content-type"] == "application/json"

    def test_hello_endpoint_has_message_field(self):
        """Test that response contains 'message' field."""
        response = client.get("/api/hello")
        data = response.json()
        assert "message" in data

    def test_hello_endpoint_message_content(self):
        """Test that message field contains expected text."""
        response = client.get("/api/hello")
        data = response.json()
        assert data["message"] == "Hello World from Backend!"

    def test_hello_endpoint_has_timestamp_field(self):
        """Test that response contains 'timestamp' field."""
        response = client.get("/api/hello")
        data = response.json()
        assert "timestamp" in data

    def test_hello_endpoint_timestamp_format(self):
        """Test that timestamp is in valid ISO 8601 format with Z suffix."""
        response = client.get("/api/hello")
        data = response.json()
        timestamp = data["timestamp"]
        
        # Validate ISO 8601 format: YYYY-MM-DDTHH:MM:SS.ffffffZ
        iso_pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z$"
        assert re.match(iso_pattern, timestamp), f"Timestamp {timestamp} is not in ISO 8601 format"

    def test_hello_endpoint_timestamp_is_recent(self):
        """Test that timestamp is current (within last 5 seconds)."""
        response = client.get("/api/hello")
        data = response.json()
        timestamp_str = data["timestamp"].rstrip("Z")
        timestamp = datetime.fromisoformat(timestamp_str)
        now = datetime.utcnow()
        
        # Check timestamp is within 5 seconds
        time_diff = abs((now - timestamp).total_seconds())
        assert time_diff < 5, f"Timestamp is not recent: {time_diff} seconds old"

    def test_hello_endpoint_response_structure(self):
        """Test that response has exactly the expected fields."""
        response = client.get("/api/hello")
        data = response.json()
        assert set(data.keys()) == {"message", "timestamp"}


class TestHealthEndpoint:
    """Test suite for /health endpoint."""

    def test_health_endpoint_returns_200(self):
        """Test that /health returns 200 OK status."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_endpoint_returns_json(self):
        """Test that /health returns JSON content type."""
        response = client.get("/health")
        assert response.headers["content-type"] == "application/json"

    def test_health_endpoint_has_status_field(self):
        """Test that response contains 'status' field."""
        response = client.get("/health")
        data = response.json()
        assert "status" in data

    def test_health_endpoint_status_value(self):
        """Test that status field has value 'healthy'."""
        response = client.get("/health")
        data = response.json()
        assert data["status"] == "healthy"

    def test_health_endpoint_response_structure(self):
        """Test that response has exactly the expected fields."""
        response = client.get("/health")
        data = response.json()
        assert set(data.keys()) == {"status"}


class TestCORSConfiguration:
    """Test suite for CORS configuration."""

    def test_cors_headers_present(self):
        """Test that CORS headers are present in response."""
        response = client.get(
            "/api/hello",
            headers={"Origin": "http://localhost:3000"}
        )
        assert "access-control-allow-origin" in response.headers

    def test_cors_allows_frontend_origin(self):
        """Test that CORS allows the frontend origin."""
        response = client.get(
            "/api/hello",
            headers={"Origin": "http://localhost:3000"}
        )
        assert response.headers["access-control-allow-origin"] == "http://localhost:3000"


class TestPerformance:
    """Test suite for performance requirements."""

    def test_hello_endpoint_response_time(self):
        """Test that /api/hello responds within 100ms."""
        import time
        start = time.time()
        response = client.get("/api/hello")
        duration = (time.time() - start) * 1000  # Convert to milliseconds
        
        assert response.status_code == 200
        assert duration < 100, f"Response time {duration}ms exceeds 100ms requirement"

    def test_health_endpoint_response_time(self):
        """Test that /health responds within 100ms."""
        import time
        start = time.time()
        response = client.get("/health")
        duration = (time.time() - start) * 1000  # Convert to milliseconds
        
        assert response.status_code == 200
        assert duration < 100, f"Response time {duration}ms exceeds 100ms requirement"
