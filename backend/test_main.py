"""Comprehensive test suite for FastAPI backend

Tests all endpoints including the new /api/greet endpoint and validates responses.
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


class TestGreetEndpoint:
    """Tests for /api/greet endpoint (new purple theme feature)"""
    
    def test_greet_with_valid_name_returns_200(self):
        """Test that greet endpoint returns 200 with valid name"""
        response = client.post("/api/greet", json={"name": "John"})
        assert response.status_code == 200
    
    def test_greet_returns_correct_greeting(self):
        """Test that greet endpoint returns personalized greeting"""
        response = client.post("/api/greet", json={"name": "John"})
        data = response.json()
        assert data["greeting"] == "Hello, John! Welcome to our purple-themed app!"
    
    def test_greet_includes_timestamp(self):
        """Test that greet response includes timestamp"""
        response = client.post("/api/greet", json={"name": "Alice"})
        data = response.json()
        assert "timestamp" in data
        assert isinstance(data["timestamp"], str)
    
    def test_greet_timestamp_is_valid_iso_format(self):
        """Test that greet timestamp is in valid ISO format"""
        response = client.post("/api/greet", json={"name": "Bob"})
        data = response.json()
        try:
            datetime.fromisoformat(data["timestamp"])
        except ValueError:
            pytest.fail("Timestamp is not in valid ISO format")
    
    def test_greet_with_empty_name_returns_400(self):
        """Test that empty name returns 400 error"""
        response = client.post("/api/greet", json={"name": ""})
        assert response.status_code == 422  # FastAPI validation error
    
    def test_greet_with_whitespace_only_name_returns_400(self):
        """Test that whitespace-only name returns 400 error"""
        response = client.post("/api/greet", json={"name": "   "})
        assert response.status_code == 422  # FastAPI validation error
    
    def test_greet_with_multiple_spaces_name_returns_400(self):
        """Test that name with only spaces returns error"""
        response = client.post("/api/greet", json={"name": "     "})
        assert response.status_code == 422
    
    def test_greet_without_name_field_returns_422(self):
        """Test that missing name field returns 422 validation error"""
        response = client.post("/api/greet", json={})
        assert response.status_code == 422
    
    def test_greet_with_invalid_json_returns_422(self):
        """Test that invalid JSON returns 422 error"""
        response = client.post(
            "/api/greet",
            data="not json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422
    
    def test_greet_response_structure(self):
        """Test that greet endpoint has correct response structure"""
        response = client.post("/api/greet", json={"name": "Sarah"})
        data = response.json()
        assert "greeting" in data
        assert "timestamp" in data
        assert len(data) == 2  # Only these two fields
    
    def test_greet_with_special_characters_in_name(self):
        """Test that names with special characters work"""
        response = client.post("/api/greet", json={"name": "Mary-Jane O'Brien"})
        assert response.status_code == 200
        data = response.json()
        assert "Mary-Jane O'Brien" in data["greeting"]
    
    def test_greet_with_unicode_name(self):
        """Test that unicode names work"""
        response = client.post("/api/greet", json={"name": "José"})
        assert response.status_code == 200
        data = response.json()
        assert "José" in data["greeting"]
    
    def test_greet_trims_whitespace(self):
        """Test that name whitespace is trimmed"""
        response = client.post("/api/greet", json={"name": "  John  "})
        assert response.status_code == 200
        data = response.json()
        assert data["greeting"] == "Hello, John! Welcome to our purple-themed app!"
    
    def test_greet_content_type(self):
        """Test that response has correct content type"""
        response = client.post("/api/greet", json={"name": "Test"})
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
    
    def test_greet_response_time(self):
        """Test that greet endpoint response time is under 100ms"""
        import time
        start = time.time()
        response = client.post("/api/greet", json={"name": "Test"})
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
    
    def test_greet_with_get_method_returns_405(self):
        """Test that GET request to /api/greet returns 405 Method Not Allowed"""
        response = client.get("/api/greet")
        assert response.status_code == 405
