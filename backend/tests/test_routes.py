"""Tests for API routes."""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime
import time

client = TestClient(app)


class TestHelloEndpoint:
    """Tests for /api/hello endpoint."""

    def test_hello_endpoint_success(self):
        """Test hello endpoint returns correct response."""
        response = client.get("/api/hello")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "timestamp" in data
        assert data["message"] == "Hello World from Backend!"
        
        # Validate timestamp format (ISO-8601)
        timestamp = data["timestamp"]
        try:
            datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except ValueError:
            pytest.fail("Timestamp is not in valid ISO-8601 format")

    def test_hello_endpoint_response_structure(self):
        """Test hello endpoint response has correct structure."""
        response = client.get("/api/hello")
        data = response.json()
        
        # Check all required fields are present
        assert set(data.keys()) == {"message", "timestamp"}
        
        # Check data types
        assert isinstance(data["message"], str)
        assert isinstance(data["timestamp"], str)

    def test_hello_endpoint_content_type(self):
        """Test hello endpoint returns JSON content type."""
        response = client.get("/api/hello")
        assert "application/json" in response.headers["content-type"]

    def test_hello_endpoint_performance(self):
        """Test hello endpoint responds within 100ms."""
        start_time = time.time()
        response = client.get("/api/hello")
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000  # Convert to ms
        assert response_time < 100, f"Response time {response_time}ms exceeds 100ms requirement"
        assert response.status_code == 200


class TestHealthEndpoint:
    """Tests for /health endpoint."""

    def test_health_check_success(self):
        """Test health endpoint returns healthy status."""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"

    def test_health_check_response_structure(self):
        """Test health endpoint response has correct structure."""
        response = client.get("/health")
        data = response.json()
        
        # Check all required fields are present
        assert set(data.keys()) == {"status"}
        
        # Check data type
        assert isinstance(data["status"], str)

    def test_health_check_content_type(self):
        """Test health endpoint returns JSON content type."""
        response = client.get("/health")
        assert "application/json" in response.headers["content-type"]

    def test_health_check_performance(self):
        """Test health endpoint responds within 100ms."""
        start_time = time.time()
        response = client.get("/health")
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000  # Convert to ms
        assert response_time < 100, f"Response time {response_time}ms exceeds 100ms requirement"
        assert response.status_code == 200


class TestErrorHandling:
    """Tests for error handling."""

    def test_invalid_endpoint_returns_404(self):
        """Test that invalid endpoints return 404."""
        response = client.get("/api/invalid")
        assert response.status_code == 404

    def test_invalid_method_returns_405(self):
        """Test that invalid methods return 405."""
        response = client.post("/api/hello")
        assert response.status_code == 405
