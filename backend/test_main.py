"""Comprehensive test suite for FastAPI backend.

Tests cover all endpoints, CORS configuration, response models,
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
    
    def test_health_check_returns_200(self):
        """Test that health check returns 200 status code."""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_check_returns_correct_json(self):
        """Test that health check returns correct JSON structure."""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
    
    def test_health_check_content_type(self):
        """Test that health check returns application/json content type."""
        response = client.get("/health")
        assert "application/json" in response.headers["content-type"]


class TestHelloEndpoint:
    """Test suite for /api/hello endpoint."""
    
    def test_hello_returns_200(self):
        """Test that hello endpoint returns 200 status code."""
        response = client.get("/api/hello")
        assert response.status_code == 200
    
    def test_hello_returns_correct_message(self):
        """Test that hello endpoint returns correct message."""
        response = client.get("/api/hello")
        data = response.json()
        assert "message" in data
        assert data["message"] == "Hello World from Backend!"
    
    def test_hello_returns_timestamp(self):
        """Test that hello endpoint returns a timestamp."""
        response = client.get("/api/hello")
        data = response.json()
        assert "timestamp" in data
        assert data["timestamp"] is not None
    
    def test_hello_timestamp_is_iso8601_format(self):
        """Test that timestamp is in ISO8601 format."""
        response = client.get("/api/hello")
        data = response.json()
        timestamp = data["timestamp"]
        
        # Verify ISO8601 format with regex
        iso8601_pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z$"
        assert re.match(iso8601_pattern, timestamp), f"Timestamp {timestamp} is not in ISO8601 format"
    
    def test_hello_timestamp_is_recent(self):
        """Test that timestamp is recent (within last minute)."""
        response = client.get("/api/hello")
        data = response.json()
        timestamp_str = data["timestamp"].rstrip("Z")
        timestamp = datetime.fromisoformat(timestamp_str)
        now = datetime.utcnow()
        
        # Timestamp should be within 60 seconds of now
        time_diff = abs((now - timestamp).total_seconds())
        assert time_diff < 60, f"Timestamp is not recent: {time_diff} seconds ago"
    
    def test_hello_content_type(self):
        """Test that hello endpoint returns application/json content type."""
        response = client.get("/api/hello")
        assert "application/json" in response.headers["content-type"]
    
    def test_hello_json_structure(self):
        """Test that hello endpoint returns correct JSON structure."""
        response = client.get("/api/hello")
        data = response.json()
        
        # Verify all required fields are present
        assert len(data) == 2, "Response should have exactly 2 fields"
        assert "message" in data
        assert "timestamp" in data
        
        # Verify field types
        assert isinstance(data["message"], str)
        assert isinstance(data["timestamp"], str)


class TestCORS:
    """Test suite for CORS configuration."""
    
    def test_cors_headers_present_on_hello_endpoint(self):
        """Test that CORS headers are present on hello endpoint."""
        response = client.options("/api/hello")
        assert "access-control-allow-origin" in response.headers
    
    def test_cors_allows_frontend_origin(self):
        """Test that CORS allows frontend origin."""
        response = client.get(
            "/api/hello",
            headers={"Origin": "http://localhost:3000"}
        )
        assert "access-control-allow-origin" in response.headers


class TestPerformance:
    """Test suite for performance requirements."""
    
    def test_hello_endpoint_response_time(self):
        """Test that hello endpoint responds within 100ms."""
        import time
        
        start = time.time()
        response = client.get("/api/hello")
        end = time.time()
        
        response_time_ms = (end - start) * 1000
        assert response.status_code == 200
        assert response_time_ms < 100, f"Response time {response_time_ms}ms exceeds 100ms requirement"
    
    def test_health_endpoint_response_time(self):
        """Test that health endpoint responds within 100ms."""
        import time
        
        start = time.time()
        response = client.get("/health")
        end = time.time()
        
        response_time_ms = (end - start) * 1000
        assert response.status_code == 200
        assert response_time_ms < 100, f"Response time {response_time_ms}ms exceeds 100ms requirement"


class TestErrorHandling:
    """Test suite for error handling."""
    
    def test_nonexistent_endpoint_returns_404(self):
        """Test that accessing non-existent endpoint returns 404."""
        response = client.get("/api/nonexistent")
        assert response.status_code == 404
    
    def test_wrong_method_on_hello_endpoint(self):
        """Test that POST method on GET-only endpoint returns 405."""
        response = client.post("/api/hello")
        assert response.status_code == 405


class TestAPIDocumentation:
    """Test suite for API documentation endpoints."""
    
    def test_openapi_schema_available(self):
        """Test that OpenAPI schema is available."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert "paths" in data
    
    def test_docs_endpoint_available(self):
        """Test that /docs endpoint is available."""
        response = client.get("/docs")
        assert response.status_code == 200
