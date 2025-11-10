"""Comprehensive tests for FastAPI backend.

Tests all endpoints and validates response structure, status codes,
and business logic.
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from main import app

client = TestClient(app)


class TestHealthEndpoint:
    """Tests for /health endpoint."""
    
    def test_health_returns_200(self):
        """Test that health endpoint returns 200 status code."""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_returns_json(self):
        """Test that health endpoint returns JSON response."""
        response = client.get("/health")
        assert response.headers["content-type"] == "application/json"
    
    def test_health_returns_healthy_status(self):
        """Test that health endpoint returns healthy status."""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"


class TestHelloEndpoint:
    """Tests for /api/hello endpoint."""
    
    def test_hello_returns_200(self):
        """Test that hello endpoint returns 200 status code."""
        response = client.get("/api/hello")
        assert response.status_code == 200
    
    def test_hello_returns_json(self):
        """Test that hello endpoint returns JSON response."""
        response = client.get("/api/hello")
        assert response.headers["content-type"] == "application/json"
    
    def test_hello_returns_message(self):
        """Test that hello endpoint returns expected message."""
        response = client.get("/api/hello")
        data = response.json()
        assert "message" in data
        assert data["message"] == "Hello World from Backend!"
    
    def test_hello_returns_timestamp(self):
        """Test that hello endpoint returns timestamp."""
        response = client.get("/api/hello")
        data = response.json()
        assert "timestamp" in data
        
        # Validate timestamp format (ISO 8601)
        timestamp = data["timestamp"]
        try:
            datetime.fromisoformat(timestamp)
        except ValueError:
            pytest.fail(f"Invalid timestamp format: {timestamp}")
    
    def test_hello_response_structure(self):
        """Test that hello endpoint returns correct response structure."""
        response = client.get("/api/hello")
        data = response.json()
        
        # Check all required fields are present
        assert set(data.keys()) == {"message", "timestamp"}
        
        # Check field types
        assert isinstance(data["message"], str)
        assert isinstance(data["timestamp"], str)


class TestCORS:
    """Tests for CORS configuration."""
    
    def test_cors_headers_present(self):
        """Test that CORS headers are present in response."""
        response = client.options(
            "/api/hello",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET"
            }
        )
        
        # Check CORS headers are present
        assert "access-control-allow-origin" in response.headers
    
    def test_cors_allows_frontend_origin(self):
        """Test that CORS allows frontend origin."""
        response = client.get(
            "/api/hello",
            headers={"Origin": "http://localhost:3000"}
        )
        
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers


class TestAPIPerformance:
    """Tests for API performance requirements."""
    
    def test_hello_response_time(self):
        """Test that hello endpoint responds within 100ms."""
        import time
        
        start_time = time.time()
        response = client.get("/api/hello")
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000  # Convert to ms
        
        assert response.status_code == 200
        assert response_time < 100, f"Response time {response_time}ms exceeds 100ms"
    
    def test_health_response_time(self):
        """Test that health endpoint responds within 100ms."""
        import time
        
        start_time = time.time()
        response = client.get("/health")
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000  # Convert to ms
        
        assert response.status_code == 200
        assert response_time < 100, f"Response time {response_time}ms exceeds 100ms"
