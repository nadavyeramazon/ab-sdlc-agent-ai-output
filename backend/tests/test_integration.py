"""Integration tests for the Red Greeting Application.

These tests verify that the frontend and backend work together correctly.
"""

import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    """Create a test client for integration testing."""
    return TestClient(app)


class TestFrontendBackendIntegration:
    """Integration tests simulating frontend-backend interactions."""

    def test_health_check_integration(self, client):
        """Test that health check endpoint works as expected by frontend."""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert "service" in data
        assert "version" in data
        assert data["status"] == "healthy"
        assert data["service"] == "red-greeting-api"

    def test_greet_flow_integration(self, client):
        """Test complete greet flow as frontend would use it."""
        # Step 1: Frontend checks health
        health_response = client.get("/health")
        assert health_response.status_code == 200
        assert health_response.json()["status"] == "healthy"
        
        # Step 2: User enters name and clicks "Get Greeting"
        user_name = "TestUser"
        greet_response = client.post("/greet", json={"name": user_name})
        assert greet_response.status_code == 200
        
        # Step 3: Frontend displays the greeting
        greet_data = greet_response.json()
        assert "message" in greet_data
        assert "name" in greet_data
        assert greet_data["name"] == user_name
        assert "Hello" in greet_data["message"]
        assert user_name in greet_data["message"]
        assert "red-themed" in greet_data["message"]
        assert "❤️" in greet_data["message"]

    def test_howdy_flow_integration(self, client):
        """Test complete howdy flow as frontend would use it."""
        # Step 1: Frontend checks health
        health_response = client.get("/health")
        assert health_response.status_code == 200
        assert health_response.json()["status"] == "healthy"
        
        # Step 2: User enters name and clicks "Get Howdy"
        user_name = "CowboyUser"
        howdy_response = client.post("/howdy", json={"name": user_name})
        assert howdy_response.status_code == 200
        
        # Step 3: Frontend displays the howdy greeting
        howdy_data = howdy_response.json()
        assert "message" in howdy_data
        assert "name" in howdy_data
        assert howdy_data["name"] == user_name
        assert "Howdy" in howdy_data["message"]
        assert user_name in howdy_data["message"]
        assert "partner" in howdy_data["message"]
        assert "red-themed" in howdy_data["message"]
        assert "🤠" in howdy_data["message"]

    def test_switching_between_greet_and_howdy(self, client):
        """Test user switching between greet and howdy buttons."""
        user_name = "SwitchUser"
        
        # User first clicks "Get Greeting"
        greet_response = client.post("/greet", json={"name": user_name})
        assert greet_response.status_code == 200
        greet_message = greet_response.json()["message"]
        assert "Hello" in greet_message
        
        # User then clicks "Get Howdy" with same name
        howdy_response = client.post("/howdy", json={"name": user_name})
        assert howdy_response.status_code == 200
        howdy_message = howdy_response.json()["message"]
        assert "Howdy" in howdy_message
        
        # Verify messages are different
        assert greet_message != howdy_message
        
        # User switches back to "Get Greeting"
        greet_response2 = client.post("/greet", json={"name": user_name})
        assert greet_response2.status_code == 200
        assert "Hello" in greet_response2.json()["message"]

    def test_error_handling_empty_name(self, client):
        """Test that frontend receives proper error for empty name."""
        # Try greet with whitespace-only name
        greet_response = client.post("/greet", json={"name": "   "})
        assert greet_response.status_code == 400
        assert "detail" in greet_response.json()
        assert "empty" in greet_response.json()["detail"].lower()
        
        # Try howdy with whitespace-only name
        howdy_response = client.post("/howdy", json={"name": "   "})
        assert howdy_response.status_code == 400
        assert "detail" in howdy_response.json()
        assert "empty" in howdy_response.json()["detail"].lower()

    def test_error_handling_missing_name(self, client):
        """Test that frontend receives proper error for missing name."""
        # Try greet without name field
        greet_response = client.post("/greet", json={})
        assert greet_response.status_code == 422
        
        # Try howdy without name field
        howdy_response = client.post("/howdy", json={})
        assert howdy_response.status_code == 422

    def test_error_handling_name_too_long(self, client):
        """Test that frontend receives proper error for name too long."""
        long_name = "A" * 101
        
        # Try greet with too long name
        greet_response = client.post("/greet", json={"name": long_name})
        assert greet_response.status_code == 422
        
        # Try howdy with too long name
        howdy_response = client.post("/howdy", json={"name": long_name})
        assert howdy_response.status_code == 422

    def test_multiple_users_sequential(self, client):
        """Test multiple users using the app sequentially."""
        users = [
            {"name": "Alice", "action": "greet"},
            {"name": "Bob", "action": "howdy"},
            {"name": "Charlie", "action": "greet"},
            {"name": "Diana", "action": "howdy"},
        ]
        
        for user in users:
            if user["action"] == "greet":
                response = client.post("/greet", json={"name": user["name"]})
                assert response.status_code == 200
                data = response.json()
                assert data["name"] == user["name"]
                assert "Hello" in data["message"]
            else:  # howdy
                response = client.post("/howdy", json={"name": user["name"]})
                assert response.status_code == 200
                data = response.json()
                assert data["name"] == user["name"]
                assert "Howdy" in data["message"]

    def test_cors_for_frontend(self, client):
        """Test that CORS is properly configured for frontend requests."""
        # Test CORS on greet endpoint
        greet_response = client.post(
            "/greet",
            json={"name": "TestUser"},
            headers={"Origin": "http://localhost:80"}
        )
        assert greet_response.status_code == 200
        
        # Test CORS on howdy endpoint
        howdy_response = client.post(
            "/howdy",
            json={"name": "TestUser"},
            headers={"Origin": "http://localhost:80"}
        )
        assert howdy_response.status_code == 200

    def test_api_documentation_accessible(self, client):
        """Test that API documentation is accessible for frontend developers."""
        # Test OpenAPI JSON
        openapi_response = client.get("/openapi.json")
        assert openapi_response.status_code == 200
        schema = openapi_response.json()
        
        # Verify it includes both greet and howdy endpoints
        assert "/greet" in schema["paths"]
        assert "/howdy" in schema["paths"]
        
        # Test interactive docs
        docs_response = client.get("/docs")
        assert docs_response.status_code == 200

    def test_special_characters_integration(self, client):
        """Test that special characters work end-to-end."""
        special_names = [
            "José",
            "François",
            "李明",
            "Алексей",
            "محمد",
        ]
        
        for name in special_names:
            # Test greet
            greet_response = client.post("/greet", json={"name": name})
            assert greet_response.status_code == 200
            assert greet_response.json()["name"] == name
            
            # Test howdy
            howdy_response = client.post("/howdy", json={"name": name})
            assert howdy_response.status_code == 200
            assert howdy_response.json()["name"] == name

    def test_red_theme_references(self, client):
        """Test that responses reference the red theme."""
        # Test greet message has red theme reference
        greet_response = client.post("/greet", json={"name": "User"})
        assert greet_response.status_code == 200
        assert "red-themed" in greet_response.json()["message"]
        
        # Test howdy message has red theme reference
        howdy_response = client.post("/howdy", json={"name": "User"})
        assert howdy_response.status_code == 200
        assert "red-themed" in howdy_response.json()["message"]
        
        # Test health check references red
        health_response = client.get("/health")
        assert health_response.status_code == 200
        assert "red-greeting-api" in health_response.json()["service"]
        
        # Test root endpoint references red
        root_response = client.get("/")
        assert root_response.status_code == 200
        assert "Red Greeting API" in root_response.json()["message"]

    def test_complete_user_journey(self, client):
        """Test a complete user journey through the application."""
        # 1. User opens the app - frontend checks health
        health_response = client.get("/health")
        assert health_response.status_code == 200
        assert health_response.json()["status"] == "healthy"
        
        # 2. User enters name "John"
        user_name = "John"
        
        # 3. User clicks "Get Greeting"
        greet_response = client.post("/greet", json={"name": user_name})
        assert greet_response.status_code == 200
        greet_data = greet_response.json()
        assert f"Hello, {user_name}!" in greet_data["message"]
        
        # 4. User is curious about howdy, clicks "Get Howdy"
        howdy_response = client.post("/howdy", json={"name": user_name})
        assert howdy_response.status_code == 200
        howdy_data = howdy_response.json()
        assert f"Howdy, {user_name}!" in howdy_data["message"]
        
        # 5. User clicks refresh health status
        health_response2 = client.get("/health")
        assert health_response2.status_code == 200
        assert health_response2.json()["status"] == "healthy"
        
        # 6. User tries different name
        new_name = "Sarah"
        greet_response2 = client.post("/greet", json={"name": new_name})
        assert greet_response2.status_code == 200
        assert f"Hello, {new_name}!" in greet_response2.json()["message"]
