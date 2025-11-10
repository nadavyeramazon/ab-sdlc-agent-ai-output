"""Comprehensive tests for FastAPI backend.

Tests all endpoints including the new /api/greet endpoint,
validates response structure, status codes, and business logic.
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


class TestGreetEndpoint:
    """Tests for /api/greet endpoint."""
    
    def test_greet_returns_200_with_valid_name(self):
        """Test that greet endpoint returns 200 with valid name."""
        response = client.post("/api/greet", json={"name": "John"})
        assert response.status_code == 200
    
    def test_greet_returns_json(self):
        """Test that greet endpoint returns JSON response."""
        response = client.post("/api/greet", json={"name": "John"})
        assert response.headers["content-type"] == "application/json"
    
    def test_greet_returns_personalized_greeting(self):
        """Test that greet endpoint returns personalized greeting."""
        response = client.post("/api/greet", json={"name": "John"})
        data = response.json()
        assert "greeting" in data
        assert "John" in data["greeting"]
        assert "Welcome to our purple-themed app" in data["greeting"]
    
    def test_greet_returns_timestamp(self):
        """Test that greet endpoint returns timestamp."""
        response = client.post("/api/greet", json={"name": "John"})
        data = response.json()
        assert "timestamp" in data
        
        # Validate timestamp format (ISO 8601)
        timestamp = data["timestamp"]
        try:
            datetime.fromisoformat(timestamp)
        except ValueError:
            pytest.fail(f"Invalid timestamp format: {timestamp}")
    
    def test_greet_response_structure(self):
        """Test that greet endpoint returns correct response structure."""
        response = client.post("/api/greet", json={"name": "John"})
        data = response.json()
        
        # Check all required fields are present
        assert set(data.keys()) == {"greeting", "timestamp"}
        
        # Check field types
        assert isinstance(data["greeting"], str)
        assert isinstance(data["timestamp"], str)
    
    def test_greet_with_empty_name_returns_400(self):
        """Test that greet endpoint returns 400 for empty name."""
        response = client.post("/api/greet", json={"name": ""})
        assert response.status_code == 422  # Pydantic validation error
    
    def test_greet_with_whitespace_name_returns_400(self):
        """Test that greet endpoint returns 400 for whitespace-only name."""
        response = client.post("/api/greet", json={"name": "   "})
        assert response.status_code == 422  # Pydantic validation error
    
    def test_greet_with_whitespace_name_contains_error_detail(self):
        """Test that error response contains helpful detail message."""
        response = client.post("/api/greet", json={"name": "   "})
        data = response.json()
        assert "detail" in data
    
    def test_greet_without_name_field_returns_422(self):
        """Test that greet endpoint returns 422 when name field is missing."""
        response = client.post("/api/greet", json={})
        assert response.status_code == 422
    
    def test_greet_with_different_names(self):
        """Test that greet endpoint works with various names."""
        test_names = ["Alice", "Bob", "Charlie", "David"]
        
        for name in test_names:
            response = client.post("/api/greet", json={"name": name})
            assert response.status_code == 200
            data = response.json()
            assert name in data["greeting"]
    
    def test_greet_trims_whitespace_from_name(self):
        """Test that greet endpoint trims whitespace from name."""
        response = client.post("/api/greet", json={"name": "  John  "})
        assert response.status_code == 200
        data = response.json()
        # Should contain trimmed name
        assert "Hello, John!" in data["greeting"]
    
    def test_greet_exact_message_format(self):
        """Test that greet endpoint returns exact expected format."""
        response = client.post("/api/greet", json={"name": "John"})
        data = response.json()
        expected_greeting = "Hello, John! Welcome to our purple-themed app!"
        assert data["greeting"] == expected_greeting


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
    
    def test_cors_headers_present_on_post(self):
        """Test that CORS headers are present in POST response."""
        response = client.options(
            "/api/greet",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST"
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
    
    def test_cors_allows_post_method(self):
        """Test that CORS allows POST method."""
        response = client.options(
            "/api/greet",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "content-type"
            }
        )
        
        assert "access-control-allow-methods" in response.headers


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
    
    def test_greet_response_time(self):
        """Test that greet endpoint responds within 100ms."""
        import time
        
        start_time = time.time()
        response = client.post("/api/greet", json={"name": "John"})
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000  # Convert to ms
        
        assert response.status_code == 200
        assert response_time < 100, f"Response time {response_time}ms exceeds 100ms"
