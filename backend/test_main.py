"""Comprehensive tests for FastAPI backend.

Tests all endpoints, validates response structure, status codes,
and business logic including performance requirements."""

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
            datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
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


class TestGreetEndpoint:
    """Tests for /api/greet endpoint."""
    
    def test_greet_with_valid_name_returns_200(self):
        """Test that greet endpoint returns 200 with valid name."""
        response = client.post("/api/greet", json={"name": "Alice"})
        assert response.status_code == 200
    
    def test_greet_returns_personalized_message(self):
        """Test that greet endpoint returns personalized message."""
        response = client.post("/api/greet", json={"name": "Bob"})
        data = response.json()
        assert "greeting" in data
        assert "Bob" in data["greeting"]
        assert "purple-themed app" in data["greeting"]
    
    def test_greet_returns_timestamp(self):
        """Test that greet endpoint returns timestamp."""
        response = client.post("/api/greet", json={"name": "Charlie"})
        data = response.json()
        assert "timestamp" in data
        
        # Validate timestamp format (ISO 8601)
        timestamp = data["timestamp"]
        try:
            datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except ValueError:
            pytest.fail(f"Invalid timestamp format: {timestamp}")
    
    def test_greet_with_empty_name_returns_400(self):
        """Test that greet endpoint returns 400 with empty name."""
        response = client.post("/api/greet", json={"name": ""})
        assert response.status_code == 400
        assert "detail" in response.json()
    
    def test_greet_with_whitespace_only_name_returns_400(self):
        """Test that greet endpoint returns 400 with whitespace-only name."""
        response = client.post("/api/greet", json={"name": "   "})
        assert response.status_code == 400
        assert "detail" in response.json()
    
    def test_greet_without_name_field_returns_422(self):
        """Test that greet endpoint returns 422 without name field."""
        response = client.post("/api/greet", json={})
        assert response.status_code == 422
    
    def test_greet_with_name_longer_than_100_chars_returns_422(self):
        """Test that greet endpoint rejects names longer than 100 characters."""
        long_name = "a" * 101
        response = client.post("/api/greet", json={"name": long_name})
        assert response.status_code == 422
    
    def test_greet_trims_whitespace_from_name(self):
        """Test that greet endpoint trims whitespace from name."""
        response = client.post("/api/greet", json={"name": "  David  "})
        data = response.json()
        assert "David" in data["greeting"]
        assert "  David  " not in data["greeting"]
    
    def test_greet_with_special_characters(self):
        """Test that greet endpoint handles special characters."""
        response = client.post("/api/greet", json={"name": "José"})
        assert response.status_code == 200
        data = response.json()
        assert "José" in data["greeting"]
    
    def test_greet_response_structure(self):
        """Test that greet endpoint returns correct response structure."""
        response = client.post("/api/greet", json={"name": "Eve"})
        data = response.json()
        
        # Check all required fields are present
        assert set(data.keys()) == {"greeting", "timestamp"}
        
        # Check field types
        assert isinstance(data["greeting"], str)
        assert isinstance(data["timestamp"], str)


class TestRootEndpoint:
    """Tests for / root endpoint."""
    
    def test_root_returns_200(self):
        """Test that root endpoint returns 200 status code."""
        response = client.get("/")
        assert response.status_code == 200
    
    def test_root_returns_service_info(self):
        """Test that root endpoint returns service information."""
        response = client.get("/")
        data = response.json()
        
        assert "service" in data
        assert "version" in data
        assert "theme" in data
        assert data["theme"] == "purple"
        assert "endpoints" in data


class TestCORS:
    """Tests for CORS configuration."""
    
    def test_cors_headers_present_on_get(self):
        """Test that CORS headers are present in GET response."""
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
    
    def test_cors_allows_post_from_frontend(self):
        """Test that CORS allows POST from frontend origin."""
        response = client.post(
            "/api/greet",
            json={"name": "Frank"},
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
    
    def test_greet_response_time(self):
        """Test that greet endpoint responds within 100ms."""
        import time
        
        start_time = time.time()
        response = client.post("/api/greet", json={"name": "George"})
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


class TestErrorHandling:
    """Tests for error handling."""
    
    def test_invalid_endpoint_returns_404(self):
        """Test that invalid endpoint returns 404."""
        response = client.get("/api/invalid")
        assert response.status_code == 404
    
    def test_invalid_json_in_greet_returns_422(self):
        """Test that invalid JSON in greet request returns 422."""
        response = client.post(
            "/api/greet",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422
