"""Comprehensive tests for FastAPI backend.

Tests cover:
- Health check endpoint
- Hello endpoint functionality
- Response format validation
- CORS headers
- Timestamp format
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime
import re
from main import app

# Create test client
client = TestClient(app)


class TestHealthEndpoint:
    """Tests for /health endpoint."""

    def test_health_returns_200(self):
        """Health endpoint should return 200 OK status."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_json(self):
        """Health endpoint should return JSON content type."""
        response = client.get("/health")
        assert response.headers["content-type"] == "application/json"

    def test_health_returns_healthy_status(self):
        """Health endpoint should return status as 'healthy'."""
        response = client.get("/health")
        data = response.json()
        assert data["status"] == "healthy"

    def test_health_response_structure(self):
        """Health endpoint should return correct response structure."""
        response = client.get("/health")
        data = response.json()
        assert isinstance(data, dict)
        assert "status" in data
        assert len(data) == 1  # Only status field


class TestHelloEndpoint:
    """Tests for /api/hello endpoint."""

    def test_hello_returns_200(self):
        """Hello endpoint should return 200 OK status."""
        response = client.get("/api/hello")
        assert response.status_code == 200

    def test_hello_returns_json(self):
        """Hello endpoint should return JSON content type."""
        response = client.get("/api/hello")
        assert response.headers["content-type"] == "application/json"

    def test_hello_returns_correct_message(self):
        """Hello endpoint should return correct message text."""
        response = client.get("/api/hello")
        data = response.json()
        assert data["message"] == "Hello World from Backend!"

    def test_hello_response_structure(self):
        """Hello endpoint should return correct response structure."""
        response = client.get("/api/hello")
        data = response.json()
        assert isinstance(data, dict)
        assert "message" in data
        assert "timestamp" in data
        assert len(data) == 2  # Only message and timestamp fields

    def test_hello_timestamp_format(self):
        """Timestamp should be in ISO 8601 format."""
        response = client.get("/api/hello")
        data = response.json()
        timestamp = data["timestamp"]
        
        # Check ISO 8601 format with Z suffix
        iso_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z$'
        assert re.match(iso_pattern, timestamp), f"Timestamp {timestamp} doesn't match ISO 8601 format"
        
        # Verify timestamp can be parsed
        try:
            datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except ValueError:
            pytest.fail(f"Timestamp {timestamp} is not a valid datetime")

    def test_hello_timestamp_is_recent(self):
        """Timestamp should be within last few seconds (current time)."""
        response = client.get("/api/hello")
        data = response.json()
        timestamp_str = data["timestamp"]
        
        # Parse timestamp
        timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        now = datetime.utcnow()
        
        # Check timestamp is within 5 seconds of now
        time_diff = abs((now - timestamp.replace(tzinfo=None)).total_seconds())
        assert time_diff < 5, f"Timestamp is {time_diff} seconds off from current time"

    def test_hello_multiple_calls_different_timestamps(self):
        """Multiple calls should return different timestamps."""
        import time
        
        response1 = client.get("/api/hello")
        time.sleep(0.1)  # Small delay to ensure different timestamps
        response2 = client.get("/api/hello")
        
        timestamp1 = response1.json()["timestamp"]
        timestamp2 = response2.json()["timestamp"]
        
        assert timestamp1 != timestamp2, "Timestamps should be different for consecutive calls"


class TestCORS:
    """Tests for CORS configuration."""

    def test_cors_headers_present_on_hello(self):
        """CORS headers should be present on /api/hello endpoint."""
        response = client.get("/api/hello")
        assert "access-control-allow-origin" in response.headers

    def test_cors_allows_localhost_3000(self):
        """CORS should allow requests from localhost:3000."""
        response = client.get(
            "/api/hello",
            headers={"Origin": "http://localhost:3000"}
        )
        assert response.headers["access-control-allow-origin"] == "http://localhost:3000"

    def test_cors_options_request(self):
        """CORS preflight OPTIONS request should work."""
        response = client.options(
            "/api/hello",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            }
        )
        assert response.status_code == 200


class TestAPIPerformance:
    """Tests for API performance requirements."""

    def test_hello_response_time_under_100ms(self):
        """Hello endpoint should respond in under 100ms."""
        import time
        
        start = time.time()
        response = client.get("/api/hello")
        elapsed = (time.time() - start) * 1000  # Convert to milliseconds
        
        assert response.status_code == 200
        assert elapsed < 100, f"Response time {elapsed}ms exceeds 100ms requirement"

    def test_health_response_time_under_100ms(self):
        """Health endpoint should respond in under 100ms."""
        import time
        
        start = time.time()
        response = client.get("/health")
        elapsed = (time.time() - start) * 1000  # Convert to milliseconds
        
        assert response.status_code == 200
        assert elapsed < 100, f"Response time {elapsed}ms exceeds 100ms requirement"
