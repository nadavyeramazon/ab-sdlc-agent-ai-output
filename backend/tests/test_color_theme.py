"""Tests to verify the red color theme is properly implemented."""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestRedTheme:
    """Test suite for verifying red theme implementation."""

    def test_health_service_name_is_red_themed(self):
        """Test that health check returns red-themed service name."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "red" in data["service"].lower()
        assert data["service"] == "red-greeting-api"

    def test_root_mentions_red(self):
        """Test that root endpoint mentions red theme."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        # Check if 'Red' is mentioned in the message
        assert "Red" in data["message"]

    def test_greet_post_includes_red_theme(self):
        """Test that POST /greet mentions red-themed application."""
        response = client.post("/greet", json={"name": "TestUser"})
        assert response.status_code == 200
        data = response.json()
        assert "red-themed" in data["message"].lower()

    def test_greet_get_includes_red_theme(self):
        """Test that GET /greet/{name} mentions red-themed application."""
        response = client.get("/greet/TestUser")
        assert response.status_code == 200
        data = response.json()
        assert "red-themed" in data["message"].lower()

    def test_howdy_post_includes_red_theme(self):
        """Test that POST /howdy mentions red-themed application."""
        response = client.post("/howdy", json={"name": "TestUser"})
        assert response.status_code == 200
        data = response.json()
        assert "red-themed" in data["message"].lower()

    def test_howdy_get_includes_red_theme(self):
        """Test that GET /howdy/{name} mentions red-themed application."""
        response = client.get("/howdy/TestUser")
        assert response.status_code == 200
        data = response.json()
        assert "red-themed" in data["message"].lower()

    def test_greet_response_has_heart_emoji(self):
        """Test that greet responses include heart emoji for red theme."""
        response = client.post("/greet", json={"name": "TestUser"})
        assert response.status_code == 200
        data = response.json()
        assert "❤️" in data["message"]

    def test_howdy_response_has_cowboy_emoji(self):
        """Test that howdy responses include cowboy emoji."""
        response = client.post("/howdy", json={"name": "TestUser"})
        assert response.status_code == 200
        data = response.json()
        assert "🤠" in data["message"]

    def test_api_title_is_red_themed(self):
        """Test that API title includes 'Red'."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "Red" in data["info"]["title"]

    def test_no_green_theme_in_responses(self):
        """Test that responses don't mention green theme."""
        # Test multiple endpoints
        endpoints = [
            client.get("/health"),
            client.get("/"),
            client.post("/greet", json={"name": "Test"}),
            client.get("/greet/Test"),
            client.post("/howdy", json={"name": "Test"}),
            client.get("/howdy/Test"),
        ]
        
        for response in endpoints:
            assert response.status_code == 200
            text = response.text.lower()
            # Should not mention green theme
            assert "green" not in text or "evergreen" in text  # Allow "evergreen" as a word
