"""Tests for FastAPI backend endpoints."""
import pytest
from fastapi.testclient import TestClient
from backend.main import app
import json
from datetime import datetime

client = TestClient(app)


class TestHealthEndpoint:
    """Tests for health check endpoint."""
    
    def test_health_check_returns_200(self):
        """Test that health endpoint returns 200 OK."""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_check_returns_correct_status(self):
        """Test that health endpoint returns healthy status."""
        response = client.get("/health")
        assert response.json() == {"status": "healthy"}


class TestHelloEndpoint:
    """Tests for hello world endpoint."""
    
    def test_hello_returns_200(self):
        """Test that hello endpoint returns 200 OK."""
        response = client.get("/api/hello")
        assert response.status_code == 200
    
    def test_hello_returns_message(self):
        """Test that hello endpoint returns correct message."""
        response = client.get("/api/hello")
        data = response.json()
        assert "message" in data
        assert data["message"] == "Hello from FastAPI backend!"
    
    def test_hello_cors_headers(self):
        """Test that CORS headers are present in hello response."""
        response = client.get("/api/hello")
        assert "access-control-allow-origin" in response.headers


class TestGreetEndpoint:
    """Tests for personalized greeting endpoint."""
    
    def test_greet_with_valid_name_returns_200(self):
        """Test that greet endpoint returns 200 with valid name."""
        response = client.post("/api/greet", json={"name": "John"})
        assert response.status_code == 200
    
    def test_greet_returns_correct_greeting(self):
        """Test that greet endpoint returns personalized greeting."""
        response = client.post("/api/greet", json={"name": "Alice"})
        data = response.json()
        assert "greeting" in data
        assert "Alice" in data["greeting"]
        assert "Welcome to our purple-themed app" in data["greeting"]
    
    def test_greet_returns_timestamp(self):
        """Test that greet endpoint returns ISO-8601 timestamp."""
        response = client.post("/api/greet", json={"name": "Bob"})
        data = response.json()
        assert "timestamp" in data
        # Verify it's a valid ISO-8601 format
        try:
            datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
        except ValueError:
            pytest.fail("Timestamp is not in valid ISO-8601 format")
    
    def test_greet_with_empty_string_returns_400(self):
        """Test that empty name returns 400 error."""
        response = client.post("/api/greet", json={"name": ""})
        assert response.status_code == 400
    
    def test_greet_with_whitespace_only_returns_400(self):
        """Test that whitespace-only name returns 400 error."""
        response = client.post("/api/greet", json={"name": "   "})
        assert response.status_code == 400
    
    def test_greet_error_message_for_empty_name(self):
        """Test that error message is correct for empty name."""
        response = client.post("/api/greet", json={"name": ""})
        data = response.json()
        assert "detail" in data
        assert "empty" in data["detail"].lower()
    
    def test_greet_with_missing_name_field_returns_422(self):
        """Test that missing name field returns 422 validation error."""
        response = client.post("/api/greet", json={})
        assert response.status_code == 422
    
    def test_greet_cors_headers(self):
        """Test that CORS headers are present in greet response."""
        response = client.post("/api/greet", json={"name": "Test"})
        assert "access-control-allow-origin" in response.headers
    
    def test_greet_response_time(self):
        """Test that greet endpoint responds quickly (< 1 second)."""
        import time
        start = time.time()
        response = client.post("/api/greet", json={"name": "Speed"})
        duration = time.time() - start
        assert response.status_code == 200
        assert duration < 1.0, f"Response took {duration}s, should be < 1s"
    
    def test_greet_with_special_characters(self):
        """Test greet endpoint with special characters in name."""
        response = client.post("/api/greet", json={"name": "José-María"})
        assert response.status_code == 200
        data = response.json()
        assert "José-María" in data["greeting"]
    
    def test_greet_with_long_name(self):
        """Test greet endpoint with long name."""
        long_name = "A" * 100
        response = client.post("/api/greet", json={"name": long_name})
        assert response.status_code == 200
        data = response.json()
        assert long_name in data["greeting"]


class TestRegressionTests:
    """Regression tests to ensure existing functionality still works."""
    
    def test_hello_endpoint_unchanged(self):
        """REG-008: Verify GET /api/hello returns expected response."""
        response = client.get("/api/hello")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello from FastAPI backend!"}
    
    def test_health_endpoint_unchanged(self):
        """REG-009: Verify GET /health returns expected response."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}
    
    def test_cors_for_existing_endpoints(self):
        """REG-010: Verify CORS headers present in existing endpoints."""
        hello_response = client.get("/api/hello")
        assert "access-control-allow-origin" in hello_response.headers
        
        health_response = client.get("/health")
        # Health endpoint should work (may or may not have CORS)
        assert health_response.status_code == 200
