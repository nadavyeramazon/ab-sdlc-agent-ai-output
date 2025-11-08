"""Comprehensive tests for the User Greeting API.

This module contains extensive tests for all endpoints and functionality
of the FastAPI greeting service.
"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app, GreetingRequest, GreetingResponse

# Create test client
client = TestClient(app)


class TestRootEndpoint:
    """Tests for the root endpoint."""
    
    def test_root_endpoint(self):
        """Test root endpoint returns correct information."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "service" in data
        assert "version" in data
        assert "status" in data
        assert "endpoints" in data
        assert data["service"] == "User Greeting API"
        assert data["version"] == "1.0.0"
        assert data["status"] == "active"
    
    def test_root_endpoint_structure(self):
        """Test root endpoint has correct endpoints listed."""
        response = client.get("/")
        data = response.json()
        assert "greet" in data["endpoints"]
        assert "health" in data["endpoints"]
        assert data["endpoints"]["greet"] == "/api/greet"
        assert data["endpoints"]["health"] == "/health"


class TestHealthEndpoint:
    """Tests for the health check endpoint."""
    
    def test_health_check(self):
        """Test health check endpoint returns healthy status."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "service" in data
        assert data["status"] == "healthy"
        assert data["service"] == "greeting-api"


class TestGreetingEndpoint:
    """Tests for the main greeting endpoint."""
    
    def test_greet_with_name_only(self):
        """Test greeting with just a name."""
        response = client.post(
            "/api/greet",
            json={"name": "Alice"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "name" in data
        assert "success" in data
        assert data["success"] is True
        assert data["name"] == "Alice"
        assert "Alice" in data["message"]
        assert "Hello" in data["message"]
    
    def test_greet_with_title_and_name(self):
        """Test greeting with title and name."""
        response = client.post(
            "/api/greet",
            json={"name": "Smith", "title": "Dr."}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["name"] == "Smith"
        assert "Dr. Smith" in data["message"]
    
    def test_greet_with_compound_name(self):
        """Test greeting with compound name (spaces, hyphens)."""
        response = client.post(
            "/api/greet",
            json={"name": "Mary-Jane O'Connor"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "Mary-Jane O'Connor" in data["message"]
    
    def test_greet_with_long_name(self):
        """Test greeting with maximum length name."""
        long_name = "A" * 100
        response = client.post(
            "/api/greet",
            json={"name": long_name}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert long_name in data["message"]
    
    def test_greet_trims_whitespace(self):
        """Test that names with leading/trailing whitespace are trimmed."""
        response = client.post(
            "/api/greet",
            json={"name": "  Bob  "}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Bob"
        assert "  Bob  " not in data["message"]
        assert "Bob" in data["message"]


class TestGreetingValidation:
    """Tests for request validation."""
    
    def test_empty_name_fails(self):
        """Test that empty name is rejected."""
        response = client.post(
            "/api/greet",
            json={"name": ""}
        )
        assert response.status_code == 422
    
    def test_whitespace_only_name_fails(self):
        """Test that whitespace-only name is rejected."""
        response = client.post(
            "/api/greet",
            json={"name": "   "}
        )
        assert response.status_code == 422
    
    def test_missing_name_fails(self):
        """Test that missing name field is rejected."""
        response = client.post(
            "/api/greet",
            json={}
        )
        assert response.status_code == 422
    
    def test_name_too_long_fails(self):
        """Test that name exceeding max length is rejected."""
        response = client.post(
            "/api/greet",
            json={"name": "A" * 101}
        )
        assert response.status_code == 422
    
    def test_invalid_characters_in_name_fails(self):
        """Test that names with invalid characters are rejected."""
        invalid_names = [
            "John123",
            "Alice@Domain",
            "Bob#Test",
            "Test$User"
        ]
        for name in invalid_names:
            response = client.post(
                "/api/greet",
                json={"name": name}
            )
            assert response.status_code == 422
    
    def test_title_too_long_fails(self):
        """Test that title exceeding max length is rejected."""
        response = client.post(
            "/api/greet",
            json={"name": "Alice", "title": "A" * 51}
        )
        assert response.status_code == 422
    
    def test_invalid_characters_in_title_fails(self):
        """Test that titles with invalid characters are rejected."""
        invalid_titles = [
            "Dr123",
            "Mr@",
            "Ms#"
        ]
        for title in invalid_titles:
            response = client.post(
                "/api/greet",
                json={"name": "Alice", "title": title}
            )
            assert response.status_code == 422
    
    def test_null_title_accepted(self):
        """Test that null title is accepted."""
        response = client.post(
            "/api/greet",
            json={"name": "Alice", "title": None}
        )
        assert response.status_code == 200
    
    def test_empty_title_accepted(self):
        """Test that empty string title is treated as no title."""
        response = client.post(
            "/api/greet",
            json={"name": "Alice", "title": ""}
        )
        assert response.status_code == 200
        data = response.json()
        assert "Alice" in data["message"]
        # Should not have title prefix since it's empty


class TestResponseStructure:
    """Tests for response structure and content."""
    
    def test_response_has_required_fields(self):
        """Test that response contains all required fields."""
        response = client.post(
            "/api/greet",
            json={"name": "Test"}
        )
        assert response.status_code == 200
        data = response.json()
        required_fields = ["message", "name", "success"]
        for field in required_fields:
            assert field in data
    
    def test_response_message_not_empty(self):
        """Test that greeting message is not empty."""
        response = client.post(
            "/api/greet",
            json={"name": "Test"}
        )
        data = response.json()
        assert len(data["message"]) > 0
    
    def test_response_success_is_boolean(self):
        """Test that success field is a boolean."""
        response = client.post(
            "/api/greet",
            json={"name": "Test"}
        )
        data = response.json()
        assert isinstance(data["success"], bool)


class TestEdgeCases:
    """Tests for edge cases and special scenarios."""
    
    def test_single_character_name(self):
        """Test greeting with single character name."""
        response = client.post(
            "/api/greet",
            json={"name": "A"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_name_with_multiple_spaces(self):
        """Test name with multiple spaces between words."""
        response = client.post(
            "/api/greet",
            json={"name": "John  Doe"}
        )
        assert response.status_code == 200
    
    def test_title_with_period(self):
        """Test title with period (e.g., 'Dr.')."""
        response = client.post(
            "/api/greet",
            json={"name": "Smith", "title": "Dr."}
        )
        assert response.status_code == 200
        data = response.json()
        assert "Dr. Smith" in data["message"]
    
    def test_various_valid_titles(self):
        """Test various valid title formats."""
        valid_titles = ["Mr", "Mrs", "Ms", "Dr", "Prof", "Mr.", "Mrs.", "Dr."]
        for title in valid_titles:
            response = client.post(
                "/api/greet",
                json={"name": "Smith", "title": title}
            )
            assert response.status_code == 200


class TestCORS:
    """Tests for CORS configuration."""
    
    def test_cors_headers_present(self):
        """Test that CORS headers are present in response."""
        response = client.options(
            "/api/greet",
            headers={"Origin": "http://localhost:3000"}
        )
        assert "access-control-allow-origin" in response.headers


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
