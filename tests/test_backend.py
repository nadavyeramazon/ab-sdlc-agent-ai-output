"""Comprehensive tests for the purple-themed greeting API."""

import pytest
from fastapi.testclient import TestClient
from backend.main import app
import re

# Configure TestClient to trigger CORS middleware
client = TestClient(app, raise_server_exceptions=False)


class TestRegressionTests:
    """REG-001 to REG-010: Regression tests to ensure existing functionality."""

    def test_reg_008_hello_endpoint(self):
        """REG-008: GET /api/hello returns valid JSON response."""
        response = client.get("/api/hello")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["message"] == "Hello World from Backend!"

    def test_reg_009_health_endpoint(self):
        """REG-009: GET /health returns health status."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"

    def test_reg_010_cors_headers(self):
        """REG-010: CORS headers present in responses."""
        # Send Origin header to trigger CORS middleware
        response = client.get("/api/hello", headers={"Origin": "http://localhost:3000"})
        assert "access-control-allow-origin" in response.headers


class TestGreetingAPI:
    """API-001 to API-007: API tests for the new greet endpoint."""

    def test_api_001_greet_with_valid_name(self):
        """API-001: POST /api/greet with valid name returns greeting."""
        response = client.post(
            "/api/greet",
            json={"name": "Alice"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "greeting" in data
        assert "Alice" in data["greeting"]
        assert "Welcome to our purple-themed app!" in data["greeting"]
        assert "timestamp" in data

    def test_api_002_greet_with_empty_string(self):
        """API-002: POST /api/greet with empty string returns 400."""
        response = client.post(
            "/api/greet",
            json={"name": ""}
        )
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Name cannot be empty"

    def test_api_003_greet_with_whitespace(self):
        """API-003: POST /api/greet with whitespace only returns 400."""
        response = client.post(
            "/api/greet",
            json={"name": "   "}
        )
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Name cannot be empty"

    def test_api_004_greet_with_full_name(self):
        """API-004: POST /api/greet with full name returns greeting."""
        response = client.post(
            "/api/greet",
            json={"name": "John Doe"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "John Doe" in data["greeting"]

    def test_api_005_greet_with_special_characters(self):
        """API-005: POST /api/greet with special characters returns greeting."""
        response = client.post(
            "/api/greet",
            json={"name": "José O'Brien"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "José O'Brien" in data["greeting"]

    def test_api_006_timestamp_format(self):
        """API-006: Timestamp matches ISO 8601 format with Z suffix."""
        response = client.post(
            "/api/greet",
            json={"name": "Test"}
        )
        assert response.status_code == 200
        data = response.json()
        timestamp = data["timestamp"]
        # ISO 8601 format: YYYY-MM-DDTHH:MM:SS.ffffffZ
        iso_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}Z$'
        assert re.match(iso_pattern, timestamp), f"Timestamp {timestamp} does not match ISO 8601 format"

    def test_api_007_cors_headers_on_greet(self):
        """API-007: CORS headers present in /api/greet response."""
        # Send Origin header to trigger CORS middleware
        response = client.post(
            "/api/greet",
            json={"name": "Test"},
            headers={"Origin": "http://localhost:3000"}
        )
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers


class TestValidation:
    """Additional validation tests."""

    def test_missing_name_field(self):
        """Test that missing name field returns 422."""
        response = client.post(
            "/api/greet",
            json={}
        )
        assert response.status_code == 422

    def test_name_with_leading_trailing_spaces(self):
        """Test that names with leading/trailing spaces are trimmed."""
        response = client.post(
            "/api/greet",
            json={"name": "  Alice  "}
        )
        assert response.status_code == 200
        data = response.json()
        # The greeting should contain "Alice" without extra spaces
        assert "Hello, Alice!" in data["greeting"]

    def test_greeting_message_format(self):
        """Test that greeting message has correct format."""
        response = client.post(
            "/api/greet",
            json={"name": "Bob"}
        )
        assert response.status_code == 200
        data = response.json()
        expected_greeting = "Hello, Bob! Welcome to our purple-themed app!"
        assert data["greeting"] == expected_greeting

    def test_multiple_requests_independence(self):
        """Test that multiple requests work independently."""
        # First request
        response1 = client.post(
            "/api/greet",
            json={"name": "Alice"}
        )
        assert response1.status_code == 200
        data1 = response1.json()
        
        # Second request
        response2 = client.post(
            "/api/greet",
            json={"name": "Bob"}
        )
        assert response2.status_code == 200
        data2 = response2.json()
        
        # Verify they're different
        assert "Alice" in data1["greeting"]
        assert "Bob" in data2["greeting"]
        assert data1["greeting"] != data2["greeting"]


class TestEndpointCoexistence:
    """Test that all endpoints coexist without conflicts."""

    def test_all_endpoints_work_together(self):
        """Test that hello, health, and greet endpoints all work."""
        # Test hello endpoint
        hello_response = client.get("/api/hello")
        assert hello_response.status_code == 200
        
        # Test health endpoint
        health_response = client.get("/health")
        assert health_response.status_code == 200
        
        # Test greet endpoint
        greet_response = client.post(
            "/api/greet",
            json={"name": "Test User"}
        )
        assert greet_response.status_code == 200

    def test_endpoints_dont_interfere(self):
        """Test that calling one endpoint doesn't affect others."""
        # Call greet
        client.post("/api/greet", json={"name": "Alice"})
        
        # Verify hello still works
        hello_response = client.get("/api/hello")
        assert hello_response.status_code == 200
        assert hello_response.json()["message"] == "Hello World from Backend!"
        
        # Verify health still works
        health_response = client.get("/health")
        assert health_response.status_code == 200
        assert health_response.json()["status"] == "healthy"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])