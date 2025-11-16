"""Comprehensive test suite for FastAPI backend.

Tests cover:
- API endpoint functionality
- Response format validation
- CORS header verification
- Health check endpoint
- Response time requirements
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime
import time
from main import app

# Create test client
client = TestClient(app)


class TestHelloEndpoint:
    """Test suite for /api/hello endpoint."""

    def test_hello_endpoint_returns_200(self):
        """Test that /api/hello returns HTTP 200 status code."""
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
        assert data["message"] == "Hello World from Backend!"

    def test_hello_endpoint_has_timestamp_field(self):
        """Test that response contains 'timestamp' field."""
        response = client.get("/api/hello")
        data = response.json()
        assert "timestamp" in data
        
        # Validate timestamp format (ISO 8601)
        timestamp = data["timestamp"]
        assert timestamp.endswith("Z")
        # Parse to verify it's a valid ISO format timestamp
        datetime.fromisoformat(timestamp.replace("Z", "+00:00"))

    def test_hello_endpoint_response_structure(self):
        """Test complete response structure matches specification."""
        response = client.get("/api/hello")
        data = response.json()
        
        # Verify exactly two fields
        assert len(data) == 2
        assert "message" in data
        assert "timestamp" in data
        
        # Verify types
        assert isinstance(data["message"], str)
        assert isinstance(data["timestamp"], str)

    def test_hello_endpoint_response_time(self):
        """Test that /api/hello responds within 100ms."""
        start_time = time.time()
        response = client.get("/api/hello")
        end_time = time.time()
        
        response_time_ms = (end_time - start_time) * 1000
        assert response_time_ms < 100, f"Response time {response_time_ms}ms exceeds 100ms requirement"

    def test_hello_endpoint_cors_headers(self):
        """Test that CORS headers are present in response."""
        response = client.get("/api/hello", headers={"Origin": "http://localhost:3000"})
        
        # Check for CORS headers
        assert "access-control-allow-origin" in response.headers
        assert response.headers["access-control-allow-origin"] == "http://localhost:3000"


class TestHealthEndpoint:
    """Test suite for /health endpoint."""

    def test_health_endpoint_returns_200(self):
        """Test that /health returns HTTP 200 status code."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_endpoint_returns_json(self):
        """Test that /health returns JSON content type."""
        response = client.get("/health")
        assert response.headers["content-type"] == "application/json"

    def test_health_endpoint_has_status_field(self):
        """Test that response contains 'status' field with 'healthy' value."""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"

    def test_health_endpoint_response_structure(self):
        """Test complete response structure matches specification."""
        response = client.get("/health")
        data = response.json()
        
        # Verify exactly one field
        assert len(data) == 1
        assert "status" in data
        assert isinstance(data["status"], str)

    def test_health_endpoint_response_time(self):
        """Test that /health responds within 100ms."""
        start_time = time.time()
        response = client.get("/health")
        end_time = time.time()
        
        response_time_ms = (end_time - start_time) * 1000
        assert response_time_ms < 100, f"Response time {response_time_ms}ms exceeds 100ms requirement"

    def test_health_endpoint_cors_headers(self):
        """Test that CORS headers are present in response."""
        response = client.get("/health", headers={"Origin": "http://localhost:3000"})
        
        # Check for CORS headers
        assert "access-control-allow-origin" in response.headers
        assert response.headers["access-control-allow-origin"] == "http://localhost:3000"


class TestAPIIntegration:
    """Integration tests for API functionality."""

    def test_multiple_hello_requests(self):
        """Test that multiple requests to /api/hello work correctly."""
        responses = [client.get("/api/hello") for _ in range(5)]
        
        for response in responses:
            assert response.status_code == 200
            data = response.json()
            assert data["message"] == "Hello World from Backend!"
            assert "timestamp" in data

    def test_timestamps_are_unique(self):
        """Test that consecutive requests have different timestamps."""
        response1 = client.get("/api/hello")
        time.sleep(0.01)  # Small delay to ensure different timestamps
        response2 = client.get("/api/hello")
        
        timestamp1 = response1.json()["timestamp"]
        timestamp2 = response2.json()["timestamp"]
        
        # Timestamps should be different
        assert timestamp1 != timestamp2

    def test_cors_preflight_request(self):
        """Test that CORS preflight requests are handled correctly."""
        response = client.options(
            "/api/hello",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            }
        )
        
        # Preflight should be successful
        assert response.status_code in [200, 204]

    def test_api_endpoints_exist(self):
        """Test that both required endpoints exist and are accessible."""
        # Test /api/hello
        hello_response = client.get("/api/hello")
        assert hello_response.status_code == 200
        
        # Test /health
        health_response = client.get("/health")
        assert health_response.status_code == 200

    def test_invalid_endpoint_returns_404(self):
        """Test that invalid endpoints return 404."""
        response = client.get("/api/invalid")
        assert response.status_code == 404
