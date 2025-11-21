"""Comprehensive tests for FastAPI backend.

Tests all endpoints, response formats, CORS headers, and data validation.
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime
import re
from main import app

# Create test client
client = TestClient(app)


class TestHelloEndpoint:
    """Tests for GET /api/hello endpoint."""

    def test_hello_returns_200(self):
        """Verify endpoint returns 200 OK status."""
        response = client.get("/api/hello")
        assert response.status_code == 200

    def test_hello_returns_json(self):
        """Verify response content type is JSON."""
        response = client.get("/api/hello")
        assert response.headers["content-type"] == "application/json"

    def test_hello_has_correct_structure(self):
        """Verify JSON response has message and timestamp fields."""
        response = client.get("/api/hello")
        data = response.json()
        assert "message" in data
        assert "timestamp" in data

    def test_hello_message_content(self):
        """Verify message field contains expected text."""
        response = client.get("/api/hello")
        data = response.json()
        assert data["message"] == "Hello World from Backend!"

    def test_hello_timestamp_is_iso8601(self):
        """Verify timestamp is in valid ISO-8601 format."""
        response = client.get("/api/hello")
        data = response.json()
        timestamp = data["timestamp"]
        
        # ISO-8601 format: YYYY-MM-DDTHH:MM:SS.ffffffZ
        iso8601_pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}Z$"
        assert re.match(iso8601_pattern, timestamp), f"Timestamp {timestamp} is not in ISO-8601 format"

    def test_hello_timestamp_is_recent(self):
        """Verify timestamp is recent (within last 5 seconds)."""
        response = client.get("/api/hello")
        data = response.json()
        timestamp_str = data["timestamp"].rstrip('Z')
        timestamp = datetime.fromisoformat(timestamp_str)
        now = datetime.utcnow()
        
        # Check timestamp is within 5 seconds of current time
        time_diff = abs((now - timestamp).total_seconds())
        assert time_diff < 5, f"Timestamp {timestamp} is not recent (diff: {time_diff}s)"

    def test_hello_cors_headers_present(self):
        """Verify CORS headers are present in response."""
        response = client.get(
            "/api/hello",
            headers={"Origin": "http://localhost:3000"}
        )
        assert "access-control-allow-origin" in response.headers


class TestHealthEndpoint:
    """Tests for GET /health endpoint."""

    def test_health_returns_200(self):
        """Verify health check returns 200 OK status."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_json(self):
        """Verify response content type is JSON."""
        response = client.get("/health")
        assert response.headers["content-type"] == "application/json"

    def test_health_has_status_field(self):
        """Verify JSON response has status field."""
        response = client.get("/health")
        data = response.json()
        assert "status" in data

    def test_health_status_is_healthy(self):
        """Verify status field returns 'healthy'."""
        response = client.get("/health")
        data = response.json()
        assert data["status"] == "healthy"


class TestPerformance:
    """Performance tests for API endpoints."""

    def test_hello_response_time(self):
        """Verify /api/hello responds within 100ms."""
        import time
        start = time.time()
        response = client.get("/api/hello")
        end = time.time()
        
        response_time_ms = (end - start) * 1000
        assert response_time_ms < 100, f"Response time {response_time_ms}ms exceeds 100ms threshold"

    def test_health_response_time(self):
        """Verify /health responds within 100ms."""
        import time
        start = time.time()
        response = client.get("/health")
        end = time.time()
        
        response_time_ms = (end - start) * 1000
        assert response_time_ms < 100, f"Response time {response_time_ms}ms exceeds 100ms threshold"


class TestCORS:
    """Tests for CORS configuration."""

    def test_cors_allows_frontend_origin(self):
        """Verify CORS allows requests from frontend origin."""
        response = client.get(
            "/api/hello",
            headers={"Origin": "http://localhost:3000"}
        )
        assert response.headers["access-control-allow-origin"] == "http://localhost:3000"

    def test_cors_allows_credentials(self):
        """Verify CORS allows credentials."""
        response = client.get(
            "/api/hello",
            headers={"Origin": "http://localhost:3000"}
        )
        assert "access-control-allow-credentials" in response.headers
