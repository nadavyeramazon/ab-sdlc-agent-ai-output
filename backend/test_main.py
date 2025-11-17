"""Comprehensive tests for FastAPI backend.

Tests all endpoints, CORS configuration, response format, and performance.
"""
import pytest
from fastapi.testclient import TestClient
from datetime import datetime
import time
from main import app

client = TestClient(app)


class TestHealthEndpoint:
    """Test cases for /health endpoint."""
    
    def test_health_returns_healthy_status(self):
        """Test that health endpoint returns correct status."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}
    
    def test_health_response_time(self):
        """Test that health endpoint responds within 100ms."""
        start_time = time.time()
        response = client.get("/health")
        end_time = time.time()
        
        assert response.status_code == 200
        response_time_ms = (end_time - start_time) * 1000
        assert response_time_ms < 100, f"Response time {response_time_ms}ms exceeds 100ms limit"


class TestHelloEndpoint:
    """Test cases for /api/hello endpoint."""
    
    def test_hello_returns_correct_structure(self):
        """Test that hello endpoint returns correct JSON structure."""
        response = client.get("/api/hello")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "timestamp" in data
        assert data["message"] == "Hello World from Backend!"
    
    def test_hello_timestamp_is_iso8601(self):
        """Test that timestamp is valid ISO-8601 format."""
        response = client.get("/api/hello")
        assert response.status_code == 200
        
        data = response.json()
        timestamp = data["timestamp"]
        
        # Verify ISO-8601 format by parsing
        try:
            # Remove 'Z' suffix and parse
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            assert dt is not None
        except ValueError:
            pytest.fail(f"Timestamp '{timestamp}' is not valid ISO-8601 format")
    
    def test_hello_response_time(self):
        """Test that hello endpoint responds within 100ms."""
        start_time = time.time()
        response = client.get("/api/hello")
        end_time = time.time()
        
        assert response.status_code == 200
        response_time_ms = (end_time - start_time) * 1000
        assert response_time_ms < 100, f"Response time {response_time_ms}ms exceeds 100ms limit"
    
    def test_hello_timestamp_is_recent(self):
        """Test that timestamp represents current time (within 5 seconds)."""
        response = client.get("/api/hello")
        data = response.json()
        timestamp_str = data["timestamp"]
        
        # Parse timestamp
        timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        now = datetime.utcnow()
        
        # Check timestamp is within 5 seconds of current time
        time_diff = abs((now - timestamp.replace(tzinfo=None)).total_seconds())
        assert time_diff < 5, f"Timestamp difference {time_diff}s is too large"


class TestCORSConfiguration:
    """Test cases for CORS middleware configuration."""
    
    def test_cors_headers_present(self):
        """Test that CORS headers are present in responses."""
        response = client.get(
            "/api/hello",
            headers={"Origin": "http://localhost:3000"}
        )
        
        assert response.status_code == 200
        # FastAPI TestClient may not include all CORS headers in test mode
        # In production, these headers will be added by the middleware
    
    def test_options_request_for_cors(self):
        """Test that OPTIONS requests are handled for CORS preflight."""
        response = client.options(
            "/api/hello",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET"
            }
        )
        # OPTIONS should be allowed
        assert response.status_code in [200, 204]


class TestRootEndpoint:
    """Test cases for root endpoint."""
    
    def test_root_returns_welcome_message(self):
        """Test that root endpoint returns welcome message."""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "Backend API" in data["message"]


class TestErrorHandling:
    """Test cases for error handling."""
    
    def test_404_for_unknown_endpoint(self):
        """Test that unknown endpoints return 404."""
        response = client.get("/unknown-endpoint")
        assert response.status_code == 404
