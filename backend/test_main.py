"""Comprehensive test suite for FastAPI backend.

Tests all endpoints, response formats, CORS configuration,
and error handling scenarios including the new /api/greet endpoint.
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timezone
import re
from main import app

# Create test client
client = TestClient(app)


class TestHelloEndpoint:
    """Test suite for /api/hello endpoint."""

    def test_hello_endpoint_returns_200(self):
        """Test that /api/hello returns 200 status code."""
        response = client.get("/api/hello")
        assert response.status_code == 200

    def test_hello_endpoint_returns_json(self):
        """Test that /api/hello returns JSON content type."""
        response = client.get("/api/hello")
        assert "application/json" in response.headers["content-type"]

    def test_hello_endpoint_has_message_field(self):
        """Test that response contains message field."""
        response = client.get("/api/hello")
        data = response.json()
        assert "message" in data
        assert data["message"] == "Hello World from Backend!"

    def test_hello_endpoint_has_timestamp_field(self):
        """Test that response contains timestamp field."""
        response = client.get("/api/hello")
        data = response.json()
        assert "timestamp" in data

    def test_hello_endpoint_timestamp_is_iso8601(self):
        """Test that timestamp is in ISO 8601 format."""
        response = client.get("/api/hello")
        data = response.json()
        timestamp = data["timestamp"]
        # ISO 8601 format with Z suffix: 2024-01-15T10:30:00.microsZ or 2024-01-15T10:30:00Z
        # Pattern matches: YYYY-MM-DDTHH:MM:SS.microsZ or YYYY-MM-DDTHH:MM:SSZ
        iso8601_pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$"
        assert re.match(iso8601_pattern, timestamp), f"Timestamp {timestamp} is not in ISO 8601 format"

    def test_hello_endpoint_timestamp_is_recent(self):
        """Test that timestamp is recent (within last 5 seconds)."""
        response = client.get("/api/hello")
        data = response.json()
        timestamp_str = data["timestamp"].rstrip("Z")
        # Parse timestamp as timezone-aware datetime
        timestamp = datetime.fromisoformat(timestamp_str).replace(tzinfo=timezone.utc)
        # Use timezone-aware datetime for comparison
        now = datetime.now(timezone.utc)
        time_diff = (now - timestamp).total_seconds()
        assert abs(time_diff) < 5, f"Timestamp is not recent: {time_diff} seconds difference"

    def test_hello_endpoint_response_structure(self):
        """Test complete response structure."""
        response = client.get("/api/hello")
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) == 2  # Should have exactly 2 fields
        assert isinstance(data["message"], str)
        assert isinstance(data["timestamp"], str)


class TestGreetEndpoint:
    """Test suite for /api/greet endpoint."""

    def test_greet_endpoint_returns_200_with_valid_name(self):
        """Test that /api/greet returns 200 status code with valid name."""
        response = client.post("/api/greet", json={"name": "John"})
        assert response.status_code == 200

    def test_greet_endpoint_returns_json(self):
        """Test that /api/greet returns JSON content type."""
        response = client.post("/api/greet", json={"name": "John"})
        assert "application/json" in response.headers["content-type"]

    def test_greet_endpoint_returns_personalized_greeting(self):
        """Test that response contains personalized greeting."""
        response = client.post("/api/greet", json={"name": "John"})
        data = response.json()
        assert "greeting" in data
        assert data["greeting"] == "Hello, John! Welcome to our purple-themed app!"

    def test_greet_endpoint_has_timestamp_field(self):
        """Test that response contains timestamp field."""
        response = client.post("/api/greet", json={"name": "Jane"})
        data = response.json()
        assert "timestamp" in data

    def test_greet_endpoint_timestamp_is_iso8601(self):
        """Test that timestamp is in ISO 8601 format."""
        response = client.post("/api/greet", json={"name": "Test"})
        data = response.json()
        timestamp = data["timestamp"]
        iso8601_pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$"
        assert re.match(iso8601_pattern, timestamp), f"Timestamp {timestamp} is not in ISO 8601 format"

    def test_greet_endpoint_rejects_empty_name(self):
        """Test that endpoint returns 400 for empty name."""
        response = client.post("/api/greet", json={"name": ""})
        assert response.status_code == 422  # Pydantic validation error
        data = response.json()
        assert "detail" in data

    def test_greet_endpoint_rejects_whitespace_name(self):
        """Test that endpoint returns 400 for whitespace-only name."""
        response = client.post("/api/greet", json={"name": "   "})
        assert response.status_code == 422  # Pydantic validation error
        data = response.json()
        assert "detail" in data

    def test_greet_endpoint_trims_name(self):
        """Test that endpoint trims whitespace from name."""
        response = client.post("/api/greet", json={"name": "  Alice  "})
        assert response.status_code == 200
        data = response.json()
        assert data["greeting"] == "Hello, Alice! Welcome to our purple-themed app!"

    def test_greet_endpoint_response_structure(self):
        """Test complete response structure."""
        response = client.post("/api/greet", json={"name": "Bob"})
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) == 2  # Should have exactly 2 fields
        assert isinstance(data["greeting"], str)
        assert isinstance(data["timestamp"], str)

    def test_greet_endpoint_response_time(self):
        """Test that /api/greet responds within 100ms."""
        import time
        start = time.time()
        response = client.post("/api/greet", json={"name": "Test"})
        end = time.time()
        response_time_ms = (end - start) * 1000
        assert response.status_code == 200
        assert response_time_ms < 100, f"Response time {response_time_ms}ms exceeds 100ms"

    def test_greet_endpoint_handles_multiple_requests(self):
        """Test that endpoint can handle multiple consecutive requests."""
        names = ["Alice", "Bob", "Charlie", "Diana", "Eve"]
        for name in names:
            response = client.post("/api/greet", json={"name": name})
            assert response.status_code == 200
            data = response.json()
            assert data["greeting"] == f"Hello, {name}! Welcome to our purple-themed app!"
            assert "timestamp" in data


class TestHealthEndpoint:
    """Test suite for /health endpoint."""

    def test_health_endpoint_returns_200(self):
        """Test that /health returns 200 status code."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_endpoint_returns_json(self):
        """Test that /health returns JSON content type."""
        response = client.get("/health")
        assert "application/json" in response.headers["content-type"]

    def test_health_endpoint_has_status_field(self):
        """Test that response contains status field."""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"

    def test_health_endpoint_response_structure(self):
        """Test complete response structure."""
        response = client.get("/health")
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) == 1  # Should have exactly 1 field
        assert isinstance(data["status"], str)


class TestCORSConfiguration:
    """Test suite for CORS middleware configuration."""

    def test_cors_allows_frontend_origin(self):
        """Test that CORS allows requests from frontend origin."""
        response = client.options(
            "/api/hello",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET"
            }
        )
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers

    def test_cors_headers_present_in_response(self):
        """Test that CORS headers are present in API responses."""
        response = client.get(
            "/api/hello",
            headers={"Origin": "http://localhost:3000"}
        )
        assert "access-control-allow-origin" in response.headers

    def test_cors_allows_post_requests(self):
        """Test that CORS allows POST requests for greet endpoint."""
        response = client.options(
            "/api/greet",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST"
            }
        )
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers


class TestErrorHandling:
    """Test suite for error handling."""

    def test_nonexistent_endpoint_returns_404(self):
        """Test that non-existent endpoints return 404."""
        response = client.get("/api/nonexistent")
        assert response.status_code == 404

    def test_wrong_method_on_hello_returns_405(self):
        """Test that wrong HTTP methods return 405."""
        response = client.post("/api/hello")
        assert response.status_code == 405

    def test_wrong_method_on_greet_returns_405(self):
        """Test that GET method on greet endpoint returns 405."""
        response = client.get("/api/greet")
        assert response.status_code == 405

    def test_greet_endpoint_missing_name_field(self):
        """Test that missing name field returns 422 validation error."""
        response = client.post("/api/greet", json={})
        assert response.status_code == 422

    def test_greet_endpoint_invalid_json(self):
        """Test that invalid JSON returns 422 error."""
        response = client.post(
            "/api/greet",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422


class TestPerformance:
    """Test suite for performance requirements."""

    def test_hello_endpoint_response_time(self):
        """Test that /api/hello responds within 100ms."""
        import time
        start = time.time()
        response = client.get("/api/hello")
        end = time.time()
        response_time_ms = (end - start) * 1000
        assert response.status_code == 200
        assert response_time_ms < 100, f"Response time {response_time_ms}ms exceeds 100ms"

    def test_health_endpoint_response_time(self):
        """Test that /health responds within 100ms."""
        import time
        start = time.time()
        response = client.get("/health")
        end = time.time()
        response_time_ms = (end - start) * 1000
        assert response.status_code == 200
        assert response_time_ms < 100, f"Response time {response_time_ms}ms exceeds 100ms"


class TestMultipleRequests:
    """Test suite for handling multiple requests."""

    def test_hello_endpoint_handles_multiple_requests(self):
        """Test that endpoint can handle multiple consecutive requests."""
        for _ in range(5):
            response = client.get("/api/hello")
            assert response.status_code == 200
            data = response.json()
            assert data["message"] == "Hello World from Backend!"
            assert "timestamp" in data

    def test_timestamps_are_different_across_requests(self):
        """Test that timestamps are updated for each request.
        
        Since timestamps now include milliseconds, consecutive requests
        should have different timestamps even without explicit delays.
        """
        response1 = client.get("/api/hello")
        response2 = client.get("/api/hello")
        
        timestamp1 = response1.json()["timestamp"]
        timestamp2 = response2.json()["timestamp"]
        
        # With millisecond precision, timestamps should be different
        # even for requests made immediately after each other
        # However, to be safe, we can still add a tiny sleep if needed
        assert timestamp1 != timestamp2, "Timestamps should be different for different requests"
