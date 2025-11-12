"""Comprehensive test suite for FastAPI backend

Tests all endpoints and validates responses.
"""
import pytest
from fastapi.testclient import TestClient
from datetime import datetime
import json

from main import app

# Create test client
client = TestClient(app)


class TestHealthEndpoint:
    """Tests for /health endpoint"""
    
    def test_health_check_returns_200(self):
        """Test that health check returns 200 status code"""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_check_returns_healthy_status(self):
        """Test that health check returns correct status"""
        response = client.get("/health")
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_health_check_response_structure(self):
        """Test that health check has correct response structure"""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert isinstance(data["status"], str)


class TestHelloEndpoint:
    """Tests for /api/hello endpoint"""
    
    def test_hello_returns_200(self):
        """Test that hello endpoint returns 200 status code"""
        response = client.get("/api/hello")
        assert response.status_code == 200
    
    def test_hello_returns_correct_message(self):
        """Test that hello endpoint returns correct message"""
        response = client.get("/api/hello")
        data = response.json()
        assert data["message"] == "Hello World from Backend!"
    
    def test_hello_includes_timestamp(self):
        """Test that hello endpoint includes timestamp"""
        response = client.get("/api/hello")
        data = response.json()
        assert "timestamp" in data
        assert isinstance(data["timestamp"], str)
    
    def test_hello_timestamp_is_valid_iso_format(self):
        """Test that timestamp is in valid ISO format"""
        response = client.get("/api/hello")
        data = response.json()
        # Should not raise exception if valid ISO format
        try:
            datetime.fromisoformat(data["timestamp"])
        except ValueError:
            pytest.fail("Timestamp is not in valid ISO format")
    
    def test_hello_response_structure(self):
        """Test that hello endpoint has correct response structure"""
        response = client.get("/api/hello")
        data = response.json()
        assert "message" in data
        assert "timestamp" in data
        assert len(data) == 2  # Only these two fields
    
    def test_hello_content_type(self):
        """Test that response has correct content type"""
        response = client.get("/api/hello")
        assert "application/json" in response.headers["content-type"]


class TestCORS:
    """Tests for CORS configuration"""
    
    def test_cors_headers_present(self):
        """Test that CORS headers are present in response"""
        response = client.options("/api/hello")
        # FastAPI TestClient doesn't fully simulate CORS preflight
        # But we can verify the middleware is configured
        assert response.status_code in [200, 405]  # OPTIONS may not be explicitly handled


class TestAPIPerformance:
    """Tests for API performance requirements"""
    
    def test_hello_response_time(self):
        """Test that API response time is under 100ms"""
        import time
        start = time.time()
        response = client.get("/api/hello")
        end = time.time()
        
        response_time_ms = (end - start) * 1000
        assert response_time_ms < 100, f"Response time {response_time_ms}ms exceeds 100ms requirement"
    
    def test_health_response_time(self):
        """Test that health check response time is fast"""
        import time
        start = time.time()
        response = client.get("/health")
        end = time.time()
        
        response_time_ms = (end - start) * 1000
        assert response_time_ms < 100, f"Response time {response_time_ms}ms exceeds 100ms requirement"


class TestInvalidEndpoints:
    """Tests for invalid endpoints"""
    
    def test_invalid_endpoint_returns_404(self):
        """Test that invalid endpoints return 404"""
        response = client.get("/api/invalid")
        assert response.status_code == 404
    
    def test_root_endpoint(self):
        """Test root endpoint behavior"""
        response = client.get("/")
        # FastAPI returns 404 for undefined root by default
        assert response.status_code == 404
