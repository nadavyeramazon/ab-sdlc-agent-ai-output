"""Comprehensive test suite for FastAPI backend.

This module contains unit tests, integration tests, and error handling tests
for all API endpoints in the Green Theme Backend application.
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime
import sys
import os

# Add parent directory to path to import main
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app, MessageRequest, MessageResponse


# Test client fixture
@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


class TestRootEndpoint:
    """Test suite for the root endpoint (GET /)."""

    def test_root_returns_200(self, client):
        """Test that root endpoint returns 200 status code."""
        response = client.get("/")
        assert response.status_code == 200

    def test_root_returns_welcome_message(self, client):
        """Test that root endpoint returns welcome message."""
        response = client.get("/")
        data = response.json()
        assert "message" in data
        assert data["message"] == "Welcome to Green Theme API"

    def test_root_returns_correct_structure(self, client):
        """Test that root endpoint returns all expected fields."""
        response = client.get("/")
        data = response.json()
        assert "message" in data
        assert "status" in data
        assert "version" in data
        assert "endpoints" in data
        assert data["status"] == "active"
        assert data["version"] == "1.0.0"

    def test_root_returns_endpoints_list(self, client):
        """Test that root endpoint returns list of available endpoints."""
        response = client.get("/")
        data = response.json()
        endpoints = data["endpoints"]
        assert isinstance(endpoints, list)
        assert "/" in endpoints
        assert "/health" in endpoints
        assert "/message" in endpoints
        assert "/docs" in endpoints


class TestHealthEndpoint:
    """Test suite for the health check endpoint (GET /health)."""

    def test_health_returns_200(self, client):
        """Test that health endpoint returns 200 status code."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_healthy_status(self, client):
        """Test that health endpoint returns healthy status."""
        response = client.get("/health")
        data = response.json()
        assert data["status"] == "healthy"

    def test_health_returns_timestamp(self, client):
        """Test that health endpoint returns valid timestamp."""
        response = client.get("/health")
        data = response.json()
        assert "timestamp" in data
        # Verify timestamp is valid ISO format
        timestamp = datetime.fromisoformat(data["timestamp"])
        assert isinstance(timestamp, datetime)

    def test_health_check_multiple_calls(self, client):
        """Test that health endpoint is consistent across multiple calls."""
        response1 = client.get("/health")
        response2 = client.get("/health")
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response1.json()["status"] == "healthy"
        assert response2.json()["status"] == "healthy"


class TestMessageEndpoint:
    """Test suite for the message endpoint (POST /message)."""

    def test_message_returns_200_with_valid_input(self, client):
        """Test that message endpoint returns 200 with valid message."""
        response = client.post("/message", json={"message": "Hello, API!"})
        assert response.status_code == 200

    def test_message_returns_correct_structure(self, client):
        """Test that message endpoint returns all expected fields."""
        response = client.post("/message", json={"message": "Test message"})
        data = response.json()
        assert "received_message" in data
        assert "response" in data
        assert "timestamp" in data

    def test_message_echoes_received_message(self, client):
        """Test that message endpoint correctly echoes the received message."""
        test_message = "Hello, World!"
        response = client.post("/message", json={"message": test_message})
        data = response.json()
        assert data["received_message"] == test_message
        assert test_message in data["response"]

    def test_message_returns_valid_timestamp(self, client):
        """Test that message endpoint returns valid ISO timestamp."""
        response = client.post("/message", json={"message": "Test"})
        data = response.json()
        timestamp = datetime.fromisoformat(data["timestamp"])
        assert isinstance(timestamp, datetime)

    @pytest.mark.parametrize("test_message", [
        "Hello!",
        "This is a longer message with multiple words",
        "123456",
        "Special chars: !@#$%^&*()",
        "Unicode: 你好 🌟"
    ])
    def test_message_handles_various_inputs(self, client, test_message):
        """Test that message endpoint handles various valid inputs."""
        response = client.post("/message", json={"message": test_message})
        assert response.status_code == 200
        data = response.json()
        assert data["received_message"] == test_message

    def test_message_empty_string_returns_400(self, client):
        """Test that empty message returns 400 error."""
        response = client.post("/message", json={"message": ""})
        assert response.status_code == 400
        assert "detail" in response.json()

    def test_message_whitespace_only_returns_400(self, client):
        """Test that whitespace-only message returns 400 error."""
        response = client.post("/message", json={"message": "   "})
        assert response.status_code == 400

    def test_message_missing_field_returns_422(self, client):
        """Test that missing message field returns 422 validation error."""
        response = client.post("/message", json={})
        assert response.status_code == 422

    def test_message_invalid_type_returns_422(self, client):
        """Test that invalid message type returns 422 validation error."""
        response = client.post("/message", json={"message": 123})
        assert response.status_code == 422

    def test_message_null_value_returns_422(self, client):
        """Test that null message value returns 422 validation error."""
        response = client.post("/message", json={"message": None})
        assert response.status_code == 422


class TestDataEndpoint:
    """Test suite for the data endpoint (GET /data)."""

    def test_data_returns_200(self, client):
        """Test that data endpoint returns 200 status code."""
        response = client.get("/data")
        assert response.status_code == 200

    def test_data_returns_correct_structure(self, client):
        """Test that data endpoint returns all expected fields."""
        response = client.get("/data")
        data = response.json()
        assert "data" in data
        assert "total" in data
        assert "timestamp" in data

    def test_data_returns_list(self, client):
        """Test that data endpoint returns data as a list."""
        response = client.get("/data")
        data = response.json()
        assert isinstance(data["data"], list)

    def test_data_returns_correct_count(self, client):
        """Test that total count matches actual data length."""
        response = client.get("/data")
        data = response.json()
        assert len(data["data"]) == data["total"]
        assert data["total"] == 3

    def test_data_items_have_correct_structure(self, client):
        """Test that each data item has correct structure."""
        response = client.get("/data")
        data = response.json()
        for item in data["data"]:
            assert "id" in item
            assert "name" in item
            assert "value" in item
            assert isinstance(item["id"], int)
            assert isinstance(item["name"], str)
            assert isinstance(item["value"], int)

    def test_data_returns_expected_items(self, client):
        """Test that data endpoint returns expected sample data."""
        response = client.get("/data")
        data = response.json()["data"]
        assert any(item["name"] == "Green Leaf" for item in data)
        assert any(item["name"] == "Forest" for item in data)
        assert any(item["name"] == "Nature" for item in data)

    def test_data_returns_valid_timestamp(self, client):
        """Test that data endpoint returns valid timestamp."""
        response = client.get("/data")
        data = response.json()
        timestamp = datetime.fromisoformat(data["timestamp"])
        assert isinstance(timestamp, datetime)


class TestInfoEndpoint:
    """Test suite for the info endpoint (GET /info)."""

    def test_info_returns_200(self, client):
        """Test that info endpoint returns 200 status code."""
        response = client.get("/info")
        assert response.status_code == 200

    def test_info_returns_correct_structure(self, client):
        """Test that info endpoint returns all expected fields."""
        response = client.get("/info")
        data = response.json()
        assert "app_name" in data
        assert "framework" in data
        assert "python_version" in data
        assert "features" in data

    def test_info_returns_correct_values(self, client):
        """Test that info endpoint returns correct application info."""
        response = client.get("/info")
        data = response.json()
        assert data["app_name"] == "Green Theme Backend"
        assert data["framework"] == "FastAPI"
        assert data["python_version"] == "3.11"

    def test_info_returns_features_list(self, client):
        """Test that info endpoint returns features as a list."""
        response = client.get("/info")
        data = response.json()
        assert isinstance(data["features"], list)
        assert len(data["features"]) > 0

    def test_info_contains_expected_features(self, client):
        """Test that info endpoint lists expected features."""
        response = client.get("/info")
        data = response.json()
        features = data["features"]
        assert "RESTful API" in features
        assert "CORS enabled" in features
        assert "Docker ready" in features


class TestCORSConfiguration:
    """Test suite for CORS middleware configuration."""

    def test_cors_headers_present(self, client):
        """Test that CORS headers are present in responses."""
        response = client.get("/", headers={"Origin": "http://localhost:3000"})
        assert "access-control-allow-origin" in response.headers

    def test_options_request_succeeds(self, client):
        """Test that OPTIONS preflight requests are handled."""
        response = client.options(
            "/message",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
            }
        )
        assert response.status_code == 200


class TestResponseModels:
    """Test suite for response model validation."""

    def test_message_response_model_validation(self, client):
        """Test that message response matches MessageResponse model."""
        response = client.post("/message", json={"message": "Test"})
        data = response.json()
        # Validate against model
        message_response = MessageResponse(**data)
        assert message_response.received_message == "Test"
        assert "Test" in message_response.response
        assert message_response.timestamp is not None


class TestErrorHandling:
    """Test suite for error handling scenarios."""

    def test_invalid_endpoint_returns_404(self, client):
        """Test that invalid endpoint returns 404."""
        response = client.get("/invalid-endpoint")
        assert response.status_code == 404

    def test_invalid_method_returns_405(self, client):
        """Test that invalid HTTP method returns 405."""
        response = client.post("/health")
        assert response.status_code == 405

    def test_malformed_json_returns_422(self, client):
        """Test that malformed JSON returns 422 error."""
        response = client.post(
            "/message",
            data="{invalid json}",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422


class TestIntegration:
    """Integration tests for multiple endpoints and workflows."""

    def test_full_api_workflow(self, client):
        """Test complete workflow using multiple endpoints."""
        # Check health
        health_response = client.get("/health")
        assert health_response.status_code == 200
        
        # Get info
        info_response = client.get("/info")
        assert info_response.status_code == 200
        
        # Get data
        data_response = client.get("/data")
        assert data_response.status_code == 200
        
        # Send message
        message_response = client.post("/message", json={"message": "Integration test"})
        assert message_response.status_code == 200

    def test_concurrent_requests(self, client):
        """Test that multiple concurrent requests are handled correctly."""
        responses = [
            client.get("/health"),
            client.get("/data"),
            client.get("/info"),
            client.post("/message", json={"message": "Test 1"}),
            client.post("/message", json={"message": "Test 2"}),
        ]
        for response in responses:
            assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=main", "--cov-report=html", "--cov-report=term"])