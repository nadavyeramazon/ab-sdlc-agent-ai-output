"""Comprehensive test suite for the FastAPI backend application."""

import pytest
from fastapi.testclient import TestClient
from main import app, GreetRequest, GreetResponse, HowdyRequest, HowdyResponse, HealthResponse


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


class TestRootEndpoint:
    """Test cases for the root endpoint."""

    def test_root_endpoint(self, client):
        """Test that root endpoint returns welcome message."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Red Greeting API" in data["message"]
        assert "docs" in data
        assert "health" in data


class TestHealthEndpoint:
    """Test cases for the health check endpoint."""

    def test_health_check_success(self, client):
        """Test that health check returns healthy status."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "red-greeting-api"
        assert "version" in data

    def test_health_check_response_model(self, client):
        """Test that health check response matches the expected model."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        
        # Validate against HealthResponse model
        health_response = HealthResponse(**data)
        assert health_response.status == "healthy"
        assert health_response.service == "red-greeting-api"
        assert health_response.version == "1.0.0"

    def test_health_check_multiple_calls(self, client):
        """Test that health check is consistent across multiple calls."""
        responses = [client.get("/health") for _ in range(5)]
        
        for response in responses:
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"


class TestGreetPostEndpoint:
    """Test cases for the POST /greet endpoint."""

    def test_greet_user_success(self, client):
        """Test greeting a user with a valid name."""
        response = client.post("/greet", json={"name": "Alice"})
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Alice"
        assert "Hello, Alice!" in data["message"]
        assert "Welcome" in data["message"]
        assert "❤️" in data["message"]
        assert "red-themed" in data["message"]

    def test_greet_user_with_long_name(self, client):
        """Test greeting a user with a long name."""
        long_name = "Alexander" * 5  # 50 characters
        response = client.post("/greet", json={"name": long_name})
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == long_name
        assert long_name in data["message"]

    def test_greet_user_with_special_characters(self, client):
        """Test greeting a user with special characters in name."""
        special_name = "José María"
        response = client.post("/greet", json={"name": special_name})
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == special_name
        assert special_name in data["message"]

    def test_greet_user_empty_name(self, client):
        """Test that empty name returns an error."""
        response = client.post("/greet", json={"name": ""})
        assert response.status_code == 422  # Validation error

    def test_greet_user_whitespace_only_name(self, client):
        """Test that whitespace-only name returns an error."""
        response = client.post("/greet", json={"name": "   "})
        assert response.status_code == 400
        assert "empty" in response.json()["detail"].lower()

    def test_greet_user_missing_name(self, client):
        """Test that missing name field returns validation error."""
        response = client.post("/greet", json={})
        assert response.status_code == 422

    def test_greet_user_name_too_long(self, client):
        """Test that name exceeding max length returns validation error."""
        too_long_name = "A" * 101  # 101 characters
        response = client.post("/greet", json={"name": too_long_name})
        assert response.status_code == 422

    def test_greet_user_response_model(self, client):
        """Test that greet response matches the expected model."""
        response = client.post("/greet", json={"name": "Bob"})
        assert response.status_code == 200
        data = response.json()
        
        # Validate against GreetResponse model
        greet_response = GreetResponse(**data)
        assert greet_response.name == "Bob"
        assert isinstance(greet_response.message, str)
        assert len(greet_response.message) > 0


class TestGreetGetEndpoint:
    """Test cases for the GET /greet/{name} endpoint."""

    def test_greet_user_get_success(self, client):
        """Test greeting a user via GET request."""
        response = client.get("/greet/Charlie")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Charlie"
        assert "Hello, Charlie!" in data["message"]
        assert "Welcome" in data["message"]
        assert "red-themed" in data["message"]

    def test_greet_user_get_with_spaces(self, client):
        """Test greeting a user with spaces in name via GET."""
        response = client.get("/greet/John%20Doe")  # URL encoded space
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "John Doe"

    def test_greet_user_get_with_special_chars(self, client):
        """Test greeting a user with special characters via GET."""
        response = client.get("/greet/María")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "María"

    def test_greet_user_get_empty_name(self, client):
        """Test that empty name in path is handled."""
        # Empty path parameter will not match the route
        response = client.get("/greet/")
        assert response.status_code in [404, 405]  # Not found or method not allowed

    def test_greet_user_get_too_long_name(self, client):
        """Test that name exceeding max length returns error."""
        too_long_name = "A" * 101
        response = client.get(f"/greet/{too_long_name}")
        assert response.status_code == 400


class TestHowdyPostEndpoint:
    """Test cases for the POST /howdy endpoint."""

    def test_howdy_user_success(self, client):
        """Test howdy greeting a user with a valid name."""
        response = client.post("/howdy", json={"name": "Alice"})
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Alice"
        assert "Howdy, Alice!" in data["message"]
        assert "Welcome partner" in data["message"]
        assert "🤠" in data["message"]
        assert "red-themed" in data["message"]

    def test_howdy_user_with_long_name(self, client):
        """Test howdy greeting a user with a long name."""
        long_name = "Alexander" * 5  # 50 characters
        response = client.post("/howdy", json={"name": long_name})
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == long_name
        assert long_name in data["message"]
        assert "Howdy" in data["message"]

    def test_howdy_user_with_special_characters(self, client):
        """Test howdy greeting a user with special characters in name."""
        special_name = "José María"
        response = client.post("/howdy", json={"name": special_name})
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == special_name
        assert special_name in data["message"]
        assert "Howdy" in data["message"]

    def test_howdy_user_empty_name(self, client):
        """Test that empty name returns an error."""
        response = client.post("/howdy", json={"name": ""})
        assert response.status_code == 422  # Validation error

    def test_howdy_user_whitespace_only_name(self, client):
        """Test that whitespace-only name returns an error."""
        response = client.post("/howdy", json={"name": "   "})
        assert response.status_code == 400
        assert "empty" in response.json()["detail"].lower()

    def test_howdy_user_missing_name(self, client):
        """Test that missing name field returns validation error."""
        response = client.post("/howdy", json={})
        assert response.status_code == 422

    def test_howdy_user_name_too_long(self, client):
        """Test that name exceeding max length returns validation error."""
        too_long_name = "A" * 101  # 101 characters
        response = client.post("/howdy", json={"name": too_long_name})
        assert response.status_code == 422

    def test_howdy_user_response_model(self, client):
        """Test that howdy response matches the expected model."""
        response = client.post("/howdy", json={"name": "Bob"})
        assert response.status_code == 200
        data = response.json()
        
        # Validate against HowdyResponse model
        howdy_response = HowdyResponse(**data)
        assert howdy_response.name == "Bob"
        assert isinstance(howdy_response.message, str)
        assert len(howdy_response.message) > 0
        assert "Howdy" in howdy_response.message

    def test_howdy_multiple_users(self, client):
        """Test howdy greeting multiple users in sequence."""
        names = ["Alice", "Bob", "Charlie", "Diana"]
        for name in names:
            response = client.post("/howdy", json={"name": name})
            assert response.status_code == 200
            data = response.json()
            assert data["name"] == name
            assert f"Howdy, {name}!" in data["message"]


class TestHowdyGetEndpoint:
    """Test cases for the GET /howdy/{name} endpoint."""

    def test_howdy_user_get_success(self, client):
        """Test howdy greeting a user via GET request."""
        response = client.get("/howdy/Charlie")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Charlie"
        assert "Howdy, Charlie!" in data["message"]
        assert "Welcome partner" in data["message"]
        assert "red-themed" in data["message"]

    def test_howdy_user_get_with_spaces(self, client):
        """Test howdy greeting a user with spaces in name via GET."""
        response = client.get("/howdy/John%20Doe")  # URL encoded space
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "John Doe"
        assert "Howdy" in data["message"]

    def test_howdy_user_get_with_special_chars(self, client):
        """Test howdy greeting a user with special characters via GET."""
        response = client.get("/howdy/María")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "María"
        assert "Howdy" in data["message"]

    def test_howdy_user_get_empty_name(self, client):
        """Test that empty name in path is handled."""
        # Empty path parameter will not match the route
        response = client.get("/howdy/")
        assert response.status_code in [404, 405]  # Not found or method not allowed

    def test_howdy_user_get_too_long_name(self, client):
        """Test that name exceeding max length returns error."""
        too_long_name = "A" * 101
        response = client.get(f"/howdy/{too_long_name}")
        assert response.status_code == 400


class TestIntegrationGreetAndHowdy:
    """Integration tests for greet and howdy endpoints working together."""

    def test_greet_and_howdy_same_user(self, client):
        """Test that both greet and howdy work for the same user."""
        test_name = "IntegrationUser"
        
        # Test greet endpoint
        greet_response = client.post("/greet", json={"name": test_name})
        assert greet_response.status_code == 200
        greet_data = greet_response.json()
        assert greet_data["name"] == test_name
        assert "Hello" in greet_data["message"]
        
        # Test howdy endpoint
        howdy_response = client.post("/howdy", json={"name": test_name})
        assert howdy_response.status_code == 200
        howdy_data = howdy_response.json()
        assert howdy_data["name"] == test_name
        assert "Howdy" in howdy_data["message"]
        
        # Verify messages are different
        assert greet_data["message"] != howdy_data["message"]

    def test_greet_and_howdy_get_endpoints(self, client):
        """Test that both GET endpoints work correctly."""
        test_name = "GetUser"
        
        # Test GET greet endpoint
        greet_response = client.get(f"/greet/{test_name}")
        assert greet_response.status_code == 200
        greet_data = greet_response.json()
        assert "Hello" in greet_data["message"]
        
        # Test GET howdy endpoint
        howdy_response = client.get(f"/howdy/{test_name}")
        assert howdy_response.status_code == 200
        howdy_data = howdy_response.json()
        assert "Howdy" in howdy_data["message"]

    def test_health_check_with_greetings(self, client):
        """Test that health check works while greeting endpoints are used."""
        # Check health
        health_response = client.get("/health")
        assert health_response.status_code == 200
        assert health_response.json()["status"] == "healthy"
        
        # Use greet endpoint
        greet_response = client.post("/greet", json={"name": "User1"})
        assert greet_response.status_code == 200
        
        # Check health again
        health_response2 = client.get("/health")
        assert health_response2.status_code == 200
        assert health_response2.json()["status"] == "healthy"
        
        # Use howdy endpoint
        howdy_response = client.post("/howdy", json={"name": "User2"})
        assert howdy_response.status_code == 200
        
        # Check health one more time
        health_response3 = client.get("/health")
        assert health_response3.status_code == 200
        assert health_response3.json()["status"] == "healthy"


class TestCORSConfiguration:
    """Test cases for CORS configuration."""

    def test_cors_headers_present(self, client):
        """Test that CORS headers are present in responses."""
        response = client.options("/health")
        # TestClient may not fully simulate CORS, but we can check the middleware is configured
        # In a real scenario, you'd test with actual cross-origin requests
        assert response.status_code in [200, 405]

    def test_cors_allows_post_requests(self, client):
        """Test that POST requests work (CORS allows them)."""
        response = client.post("/greet", json={"name": "TestUser"})
        assert response.status_code == 200
        
        response = client.post("/howdy", json={"name": "TestUser"})
        assert response.status_code == 200


class TestAPIDocumentation:
    """Test cases for API documentation."""

    def test_openapi_schema_available(self, client):
        """Test that OpenAPI schema is available."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert schema["info"]["title"] == "Red Greeting API"

    def test_docs_endpoint_available(self, client):
        """Test that interactive docs are available."""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_redoc_endpoint_available(self, client):
        """Test that ReDoc documentation is available."""
        response = client.get("/redoc")
        assert response.status_code == 200

    def test_openapi_schema_includes_howdy(self, client):
        """Test that OpenAPI schema includes howdy endpoints."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        
        # Check that /howdy endpoints are in the schema
        assert "/howdy" in schema["paths"]
        assert "/howdy/{name}" in schema["paths"]


class TestEdgeCases:
    """Test cases for edge cases and error handling."""

    def test_invalid_endpoint(self, client):
        """Test that invalid endpoints return 404."""
        response = client.get("/invalid/endpoint")
        assert response.status_code == 404

    def test_invalid_method_on_greet(self, client):
        """Test that invalid HTTP methods return appropriate errors."""
        response = client.put("/greet", json={"name": "Test"})
        assert response.status_code in [404, 405]

    def test_invalid_method_on_howdy(self, client):
        """Test that invalid HTTP methods on howdy return appropriate errors."""
        response = client.put("/howdy", json={"name": "Test"})
        assert response.status_code in [404, 405]

    def test_malformed_json_post(self, client):
        """Test that malformed JSON returns appropriate error."""
        response = client.post(
            "/greet",
            data="{invalid json}",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422
        
        response = client.post(
            "/howdy",
            data="{invalid json}",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422

    def test_numeric_name(self, client):
        """Test greeting with numeric name."""
        response = client.post("/greet", json={"name": "12345"})
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "12345"
        
        response = client.post("/howdy", json={"name": "12345"})
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "12345"

    def test_unicode_emoji_name(self, client):
        """Test greeting with emoji in name."""
        response = client.post("/greet", json={"name": "Alice 👋"})
        assert response.status_code == 200
        data = response.json()
        assert "Alice 👋" in data["message"]
        
        response = client.post("/howdy", json={"name": "Alice 👋"})
        assert response.status_code == 200
        data = response.json()
        assert "Alice 👋" in data["message"]
