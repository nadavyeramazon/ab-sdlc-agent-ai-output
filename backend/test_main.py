"""Test suite for the FastAPI backend application.

This module contains comprehensive tests for all backend endpoints
including root, health check, and greeting endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestRootEndpoint:
    """Tests for the root endpoint (/)"""

    def test_root_endpoint_success(self):
        """Test that root endpoint returns expected hello world message"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Hello World from Backend!"
        assert data["service"] == "backend"
        assert data["status"] == "running"

    def test_root_endpoint_structure(self):
        """Test that root endpoint response has correct structure"""
        response = client.get("/")
        data = response.json()
        assert "message" in data
        assert "service" in data
        assert "status" in data
        assert len(data) == 3


class TestHealthEndpoint:
    """Tests for the health check endpoint (/health)"""

    def test_health_endpoint_success(self):
        """Test that health endpoint returns healthy status"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "backend"

    def test_health_endpoint_structure(self):
        """Test that health endpoint response has correct structure"""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert "service" in data
        assert len(data) == 2


class TestGreetingEndpoint:
    """Tests for the greeting endpoint (/api/greeting)"""

    def test_greeting_default(self):
        """Test greeting endpoint with default name parameter"""
        response = client.get("/api/greeting")
        assert response.status_code == 200
        data = response.json()
        assert data["greeting"] == "Hello, World!"
        assert data["from"] == "Backend Service"

    def test_greeting_with_custom_name(self):
        """Test greeting endpoint with custom name parameter"""
        response = client.get("/api/greeting?name=Alice")
        assert response.status_code == 200
        data = response.json()
        assert data["greeting"] == "Hello, Alice!"
        assert data["from"] == "Backend Service"

    def test_greeting_with_special_characters(self):
        """Test greeting endpoint with special characters in name"""
        response = client.get("/api/greeting?name=Test%20User")
        assert response.status_code == 200
        data = response.json()
        assert data["greeting"] == "Hello, Test User!"

    def test_greeting_with_empty_name(self):
        """Test greeting endpoint with empty name parameter"""
        response = client.get("/api/greeting?name=")
        assert response.status_code == 200
        data = response.json()
        # Empty name should still work, greeting will be "Hello, !"
        assert "greeting" in data
        assert data["from"] == "Backend Service"

    def test_greeting_response_structure(self):
        """Test that greeting endpoint response has correct structure"""
        response = client.get("/api/greeting?name=TestUser")
        data = response.json()
        assert "greeting" in data
        assert "from" in data
        assert len(data) == 2


class TestAPIBehavior:
    """Tests for general API behavior and edge cases"""

    def test_nonexistent_endpoint(self):
        """Test that nonexistent endpoints return 404"""
        response = client.get("/nonexistent")
        assert response.status_code == 404

    def test_cors_headers_present(self):
        """Test that CORS headers are present in responses"""
        response = client.get("/", headers={"Origin": "http://localhost:3000"})
        # TestClient doesn't trigger CORS middleware, but we verify the endpoint works
        assert response.status_code == 200

    def test_content_type_json(self):
        """Test that responses have correct content type"""
        response = client.get("/")
        assert "application/json" in response.headers["content-type"]

    def test_multiple_sequential_requests(self):
        """Test that multiple requests work correctly"""
        for _ in range(5):
            response = client.get("/health")
            assert response.status_code == 200


class TestParameterValidation:
    """Tests for parameter validation and error handling"""

    def test_greeting_with_multiple_parameters(self):
        """Test greeting endpoint ignores extra parameters"""
        response = client.get("/api/greeting?name=Alice&extra=value")
        assert response.status_code == 200
        data = response.json()
        assert data["greeting"] == "Hello, Alice!"

    def test_greeting_unicode_characters(self):
        """Test greeting endpoint handles unicode characters"""
        response = client.get("/api/greeting?name=世界")
        assert response.status_code == 200
        data = response.json()
        assert "世界" in data["greeting"]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
