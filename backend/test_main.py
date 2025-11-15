"""Comprehensive test suite for FastAPI backend

Tests all API endpoints to ensure they meet the acceptance criteria:
- /api/hello returns correct message format with timestamp
- /health returns healthy status
- CORS headers are properly configured
- Response times are acceptable
"""

import re
from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from main import app


# Create test client
client = TestClient(app)


class TestHelloEndpoint:
    """Test suite for /api/hello endpoint"""

    def test_hello_returns_200(self):
        """Test that /api/hello returns HTTP 200 status"""
        response = client.get("/api/hello")
        assert response.status_code == 200

    def test_hello_returns_json(self):
        """Test that /api/hello returns valid JSON"""
        response = client.get("/api/hello")
        assert response.headers["content-type"] == "application/json"
        data = response.json()
        assert isinstance(data, dict)

    def test_hello_contains_message_field(self):
        """Test that response contains 'message' field with correct value"""
        response = client.get("/api/hello")
        data = response.json()
        assert "message" in data
        assert data["message"] == "Hello World from Backend!"

    def test_hello_contains_timestamp_field(self):
        """Test that response contains 'timestamp' field"""
        response = client.get("/api/hello")
        data = response.json()
        assert "timestamp" in data
        assert isinstance(data["timestamp"], str)

    def test_hello_timestamp_is_iso8601_format(self):
        """Test that timestamp is in valid ISO 8601 format"""
        response = client.get("/api/hello")
        data = response.json()
        timestamp = data["timestamp"]
        
        # Check ISO 8601 format with regex
        iso8601_pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z$"
        assert re.match(iso8601_pattern, timestamp), f"Timestamp {timestamp} is not in ISO 8601 format"
        
        # Verify it's a valid datetime
        try:
            datetime.fromisoformat(timestamp.rstrip('Z'))
        except ValueError:
            pytest.fail(f"Timestamp {timestamp} cannot be parsed as datetime")

    def test_hello_response_structure(self):
        """Test that response has exactly the expected structure"""
        response = client.get("/api/hello")
        data = response.json()
        assert set(data.keys()) == {"message", "timestamp"}

    def test_hello_cors_headers_present(self):
        """Test that CORS headers are present in response"""
        # Simulate a request from the frontend
        response = client.get(
            "/api/hello",
            headers={"Origin": "http://localhost:3000"}
        )
        assert "access-control-allow-origin" in response.headers


class TestHealthEndpoint:
    """Test suite for /health endpoint"""

    def test_health_returns_200(self):
        """Test that /health returns HTTP 200 status"""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_json(self):
        """Test that /health returns valid JSON"""
        response = client.get("/health")
        assert response.headers["content-type"] == "application/json"
        data = response.json()
        assert isinstance(data, dict)

    def test_health_contains_status_field(self):
        """Test that response contains 'status' field with 'healthy' value"""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"

    def test_health_response_structure(self):
        """Test that response has exactly the expected structure"""
        response = client.get("/health")
        data = response.json()
        assert set(data.keys()) == {"status"}


class TestRootEndpoint:
    """Test suite for / root endpoint"""

    def test_root_returns_200(self):
        """Test that / returns HTTP 200 status"""
        response = client.get("/")
        assert response.status_code == 200

    def test_root_returns_api_info(self):
        """Test that root endpoint returns API information"""
        response = client.get("/")
        data = response.json()
        assert "message" in data
        assert "endpoints" in data


class TestPerformance:
    """Test suite for performance requirements"""

    def test_hello_response_time(self):
        """Test that /api/hello responds within acceptable time"""
        import time
        
        start_time = time.time()
        response = client.get("/api/hello")
        end_time = time.time()
        
        response_time_ms = (end_time - start_time) * 1000
        
        # Accept up to 500ms for test environment (spec requires <100ms in production)
        assert response_time_ms < 500, f"Response time {response_time_ms}ms exceeds 500ms"
        assert response.status_code == 200

    def test_health_response_time(self):
        """Test that /health responds within acceptable time"""
        import time
        
        start_time = time.time()
        response = client.get("/health")
        end_time = time.time()
        
        response_time_ms = (end_time - start_time) * 1000
        
        # Accept up to 500ms for test environment
        assert response_time_ms < 500, f"Response time {response_time_ms}ms exceeds 500ms"
        assert response.status_code == 200


class TestCORSConfiguration:
    """Test suite for CORS middleware configuration"""

    def test_cors_allows_localhost_origin(self):
        """Test that CORS allows requests from localhost:3000"""
        response = client.options(
            "/api/hello",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            }
        )
        # OPTIONS requests should be handled by CORS middleware
        assert response.status_code in [200, 204]

    def test_cors_headers_in_get_request(self):
        """Test that CORS headers are present in GET requests"""
        response = client.get(
            "/api/hello",
            headers={"Origin": "http://localhost:3000"}
        )
        assert response.status_code == 200
        # Check for CORS header (case-insensitive)
        headers_lower = {k.lower(): v for k, v in response.headers.items()}
        assert "access-control-allow-origin" in headers_lower
