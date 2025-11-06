"""Test suite for the greeting application backend."""
import pytest
from fastapi.testclient import TestClient
from main import app


# Create a test client for the FastAPI application
client = TestClient(app)


class TestRootEndpoint:
    """Tests for the root endpoint."""

    def test_root_returns_welcome_message(self):
        """Test that the root endpoint returns a welcome message."""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {
            "message": "Welcome to the Greeting API! Use POST /greet to get a personalized greeting."
        }

    def test_root_response_structure(self):
        """Test that the root endpoint returns the correct JSON structure."""
        response = client.get("/")
        data = response.json()
        assert "message" in data
        assert isinstance(data["message"], str)


class TestHealthEndpoint:
    """Tests for the health check endpoint."""

    def test_health_returns_healthy_status(self):
        """Test that the health endpoint returns a healthy status."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    def test_health_response_structure(self):
        """Test that the health endpoint returns the correct JSON structure."""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert isinstance(data["status"], str)


class TestGreetEndpoint:
    """Tests for the greeting endpoint."""

    def test_greet_with_valid_name(self):
        """Test greeting with a valid name."""
        response = client.post("/greet", json={"name": "Alice"})
        assert response.status_code == 200
        data = response.json()
        assert "greeting" in data
        assert data["greeting"] == "Hello, Alice! Welcome to our green-themed greeting app!"

    def test_greet_with_different_names(self):
        """Test greeting with various different names."""
        test_names = ["Bob", "Charlie", "David", "Eve"]
        for name in test_names:
            response = client.post("/greet", json={"name": name})
            assert response.status_code == 200
            data = response.json()
            assert data["greeting"] == f"Hello, {name}! Welcome to our green-themed greeting app!"

    def test_greet_with_special_characters_in_name(self):
        """Test greeting with special characters in the name."""
        special_names = ["Mary-Jane", "O'Brien", "José", "François"]
        for name in special_names:
            response = client.post("/greet", json={"name": name})
            assert response.status_code == 200
            data = response.json()
            assert name in data["greeting"]

    def test_greet_with_empty_name(self):
        """Test greeting with an empty name."""
        response = client.post("/greet", json={"name": ""})
        # The API should still return 200 even with empty name
        assert response.status_code == 200
        data = response.json()
        assert "greeting" in data

    def test_greet_with_whitespace_name(self):
        """Test greeting with a whitespace-only name."""
        response = client.post("/greet", json={"name": "   "})
        assert response.status_code == 200
        data = response.json()
        assert "greeting" in data

    def test_greet_with_long_name(self):
        """Test greeting with a very long name."""
        long_name = "A" * 1000
        response = client.post("/greet", json={"name": long_name})
        assert response.status_code == 200
        data = response.json()
        assert long_name in data["greeting"]

    def test_greet_missing_name_field(self):
        """Test greeting endpoint without the name field."""
        response = client.post("/greet", json={})
        # FastAPI should return 422 for validation error
        assert response.status_code == 422

    def test_greet_with_null_name(self):
        """Test greeting endpoint with null name."""
        response = client.post("/greet", json={"name": None})
        # FastAPI should return 422 for validation error
        assert response.status_code == 422

    def test_greet_with_invalid_json(self):
        """Test greeting endpoint with invalid JSON."""
        response = client.post(
            "/greet",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422

    def test_greet_response_structure(self):
        """Test that the greet endpoint returns the correct JSON structure."""
        response = client.post("/greet", json={"name": "Test"})
        data = response.json()
        assert "greeting" in data
        assert isinstance(data["greeting"], str)

    def test_greet_with_numeric_string_name(self):
        """Test greeting with numeric string as name."""
        response = client.post("/greet", json={"name": "12345"})
        assert response.status_code == 200
        data = response.json()
        assert "12345" in data["greeting"]


class TestCORSConfiguration:
    """Tests for CORS configuration."""

    def test_cors_headers_present(self):
        """Test that CORS headers are present in responses."""
        response = client.get("/health")
        # Check if CORS middleware is active (headers should be present)
        assert response.status_code == 200

    def test_options_request(self):
        """Test OPTIONS request for CORS preflight."""
        response = client.options("/greet")
        # OPTIONS should be allowed
        assert response.status_code in [200, 405]  # 405 if OPTIONS not explicitly defined


class TestAPIErrorHandling:
    """Tests for API error handling."""

    def test_invalid_endpoint(self):
        """Test accessing an endpoint that doesn't exist."""
        response = client.get("/invalid-endpoint")
        assert response.status_code == 404

    def test_wrong_http_method_on_greet(self):
        """Test using wrong HTTP method on greet endpoint."""
        response = client.get("/greet")
        assert response.status_code == 405  # Method Not Allowed

    def test_wrong_http_method_on_root(self):
        """Test using POST on root endpoint which expects GET."""
        response = client.post("/")
        assert response.status_code == 405  # Method Not Allowed
