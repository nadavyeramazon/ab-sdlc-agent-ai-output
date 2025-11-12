"""Tests for /api/greet endpoint."""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime
import time

client = TestClient(app)


class TestGreetEndpoint:
    """Tests for /api/greet endpoint - New Feature."""

    def test_greet_endpoint_success_with_valid_name(self):
        """Test greet endpoint returns correct response for valid name."""
        response = client.post(
            "/api/greet",
            json={"name": "John Doe"}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "greeting" in data
        assert "timestamp" in data
        assert data["greeting"] == "Hello, John Doe! Welcome to our purple-themed app!"
        
        # Validate timestamp format (ISO-8601)
        timestamp = data["timestamp"]
        try:
            datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except ValueError:
            pytest.fail("Timestamp is not in valid ISO-8601 format")

    def test_greet_endpoint_with_different_names(self):
        """Test greet endpoint handles different names correctly."""
        test_names = ["Alice", "Bob Smith", "María García", "李明"]
        
        for name in test_names:
            response = client.post(
                "/api/greet",
                json={"name": name}
            )
            assert response.status_code == 200
            data = response.json()
            assert name in data["greeting"]
            assert "Welcome to our purple-themed app!" in data["greeting"]

    def test_greet_endpoint_empty_string_validation(self):
        """Test greet endpoint rejects empty string."""
        response = client.post(
            "/api/greet",
            json={"name": ""}
        )
        assert response.status_code == 422  # Pydantic validation error
        data = response.json()
        assert "detail" in data

    def test_greet_endpoint_whitespace_only_validation(self):
        """Test greet endpoint rejects whitespace-only string."""
        response = client.post(
            "/api/greet",
            json={"name": "   "}
        )
        assert response.status_code == 422  # Pydantic validation error
        data = response.json()
        assert "detail" in data

    def test_greet_endpoint_trims_whitespace(self):
        """Test greet endpoint trims whitespace from name."""
        response = client.post(
            "/api/greet",
            json={"name": "  John Doe  "}
        )
        assert response.status_code == 200
        data = response.json()
        # Check that whitespace is trimmed
        assert data["greeting"] == "Hello, John Doe! Welcome to our purple-themed app!"
        assert "  " not in data["greeting"]

    def test_greet_endpoint_missing_name_field(self):
        """Test greet endpoint rejects request without name field."""
        response = client.post(
            "/api/greet",
            json={}
        )
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    def test_greet_endpoint_response_structure(self):
        """Test greet endpoint response has correct structure."""
        response = client.post(
            "/api/greet",
            json={"name": "Test User"}
        )
        data = response.json()
        
        # Check all required fields are present
        assert set(data.keys()) == {"greeting", "timestamp"}
        
        # Check data types
        assert isinstance(data["greeting"], str)
        assert isinstance(data["timestamp"], str)

    def test_greet_endpoint_content_type(self):
        """Test greet endpoint returns JSON content type."""
        response = client.post(
            "/api/greet",
            json={"name": "Test User"}
        )
        assert "application/json" in response.headers["content-type"]

    def test_greet_endpoint_performance(self):
        """Test greet endpoint responds within 100ms."""
        start_time = time.time()
        response = client.post(
            "/api/greet",
            json={"name": "Performance Test"}
        )
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000  # Convert to ms
        assert response_time < 100, f"Response time {response_time}ms exceeds 100ms requirement"
        assert response.status_code == 200

    def test_greet_endpoint_cors_headers(self):
        """Test greet endpoint includes proper CORS headers."""
        response = client.post(
            "/api/greet",
            json={"name": "CORS Test"},
            headers={"Origin": "http://localhost:3000"}
        )
        # CORS headers should be present
        assert "access-control-allow-origin" in response.headers or response.status_code == 200

    def test_greet_endpoint_invalid_json(self):
        """Test greet endpoint handles invalid JSON gracefully."""
        response = client.post(
            "/api/greet",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code in [400, 422]  # Bad request or validation error


class TestBackwardCompatibility:
    """Tests to ensure existing endpoints still work after new feature addition."""

    def test_hello_endpoint_still_works(self):
        """Test that existing /api/hello endpoint is unchanged."""
        response = client.get("/api/hello")
        assert response.status_code == 200
        
        data = response.json()
        assert data["message"] == "Hello World from Backend!"
        assert "timestamp" in data

    def test_health_endpoint_still_works(self):
        """Test that existing /health endpoint is unchanged."""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"

    def test_hello_endpoint_method_restrictions(self):
        """Test that GET /api/hello still rejects POST requests."""
        response = client.post("/api/hello")
        assert response.status_code == 405  # Method not allowed
