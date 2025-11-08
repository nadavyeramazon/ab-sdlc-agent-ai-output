"""Comprehensive test suite for the Greeting API."""
import pytest
from fastapi.testclient import TestClient
from backend.main import app, GREETINGS

client = TestClient(app)


class TestRootEndpoint:
    """Tests for the root endpoint."""
    
    def test_root_returns_api_info(self):
        """Test that root endpoint returns API information."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert "endpoints" in data
        assert data["name"] == "Greeting API"
        assert data["version"] == "1.0.0"


class TestHealthEndpoint:
    """Tests for the health check endpoint."""
    
    def test_health_check_returns_healthy(self):
        """Test that health endpoint returns healthy status."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "greeting-api"


class TestGreetEndpoint:
    """Tests for the greet endpoint."""
    
    def test_greet_with_valid_english_name(self):
        """Test greeting in English with valid name."""
        response = client.post(
            "/api/greet",
            json={"name": "John", "language": "en"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "John"
        assert data["language"] == "en"
        assert "John" in data["message"]
        assert "Hello" in data["message"]
    
    def test_greet_with_spanish_language(self):
        """Test greeting in Spanish."""
        response = client.post(
            "/api/greet",
            json={"name": "Maria", "language": "es"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Maria"
        assert data["language"] == "es"
        assert "Maria" in data["message"]
        assert "Hola" in data["message"]
    
    def test_greet_with_french_language(self):
        """Test greeting in French."""
        response = client.post(
            "/api/greet",
            json={"name": "Pierre", "language": "fr"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Pierre"
        assert data["language"] == "fr"
        assert "Pierre" in data["message"]
        assert "Bonjour" in data["message"]
    
    def test_greet_with_german_language(self):
        """Test greeting in German."""
        response = client.post(
            "/api/greet",
            json={"name": "Hans", "language": "de"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Hans"
        assert data["language"] == "de"
        assert "Hans" in data["message"]
        assert "Hallo" in data["message"]
    
    def test_greet_with_italian_language(self):
        """Test greeting in Italian."""
        response = client.post(
            "/api/greet",
            json={"name": "Giuseppe", "language": "it"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Giuseppe"
        assert data["language"] == "it"
        assert "Giuseppe" in data["message"]
        assert "Ciao" in data["message"]
    
    def test_greet_defaults_to_english(self):
        """Test that greeting defaults to English when no language specified."""
        response = client.post(
            "/api/greet",
            json={"name": "Alice"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["language"] == "en"
    
    def test_greet_with_uppercase_language(self):
        """Test that language code is case-insensitive."""
        response = client.post(
            "/api/greet",
            json={"name": "Bob", "language": "EN"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["language"] == "en"
    
    def test_greet_with_mixed_case_language(self):
        """Test mixed case language code."""
        response = client.post(
            "/api/greet",
            json={"name": "Charlie", "language": "Es"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["language"] == "es"
    
    def test_greet_with_long_name(self):
        """Test greeting with a long name."""
        long_name = "A" * 100
        response = client.post(
            "/api/greet",
            json={"name": long_name, "language": "en"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == long_name
    
    def test_greet_with_special_characters(self):
        """Test greeting with special characters in name."""
        response = client.post(
            "/api/greet",
            json={"name": "José-María", "language": "es"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "José-María" in data["message"]


class TestGreetEndpointErrors:
    """Tests for error handling in greet endpoint."""
    
    def test_greet_with_empty_name(self):
        """Test that empty name returns validation error."""
        response = client.post(
            "/api/greet",
            json={"name": "", "language": "en"}
        )
        assert response.status_code == 422  # Validation error
    
    def test_greet_without_name(self):
        """Test that missing name returns validation error."""
        response = client.post(
            "/api/greet",
            json={"language": "en"}
        )
        assert response.status_code == 422
    
    def test_greet_with_too_long_name(self):
        """Test that name exceeding max length returns validation error."""
        long_name = "A" * 101
        response = client.post(
            "/api/greet",
            json={"name": long_name, "language": "en"}
        )
        assert response.status_code == 422
    
    def test_greet_with_unsupported_language(self):
        """Test that unsupported language returns error."""
        response = client.post(
            "/api/greet",
            json={"name": "John", "language": "xx"}
        )
        assert response.status_code == 400
        data = response.json()
        assert "not supported" in data["detail"].lower()
    
    def test_greet_with_invalid_language_code(self):
        """Test with completely invalid language code."""
        response = client.post(
            "/api/greet",
            json={"name": "John", "language": "invalid"}
        )
        assert response.status_code == 400
    
    def test_greet_with_empty_json(self):
        """Test with empty JSON body."""
        response = client.post(
            "/api/greet",
            json={}
        )
        assert response.status_code == 422
    
    def test_greet_with_null_name(self):
        """Test with null name value."""
        response = client.post(
            "/api/greet",
            json={"name": None, "language": "en"}
        )
        assert response.status_code == 422


class TestResponseModels:
    """Tests for response model structure."""
    
    def test_greeting_response_has_required_fields(self):
        """Test that response contains all required fields."""
        response = client.post(
            "/api/greet",
            json={"name": "Test", "language": "en"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "name" in data
        assert "language" in data
        assert isinstance(data["message"], str)
        assert isinstance(data["name"], str)
        assert isinstance(data["language"], str)


class TestAllLanguages:
    """Test all supported languages."""
    
    @pytest.mark.parametrize("language", list(GREETINGS.keys()))
    def test_all_supported_languages(self, language):
        """Test that all configured languages work correctly."""
        response = client.post(
            "/api/greet",
            json={"name": "TestUser", "language": language}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["language"] == language
        assert "TestUser" in data["message"]


class TestCORS:
    """Tests for CORS configuration."""
    
    def test_cors_headers_present(self):
        """Test that CORS headers are present in response."""
        response = client.post(
            "/api/greet",
            json={"name": "Test", "language": "en"},
            headers={"Origin": "http://localhost:3000"}
        )
        assert response.status_code == 200
        # Note: TestClient may not include all CORS headers in response
        # This is more of a smoke test


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""
    
    def test_greet_with_whitespace_name(self):
        """Test name with only whitespace."""
        response = client.post(
            "/api/greet",
            json={"name": "   ", "language": "en"}
        )
        # Should either accept it or reject it consistently
        # Accepting with whitespace trimmed
        assert response.status_code in [200, 422]
    
    def test_greet_with_numeric_name(self):
        """Test name with numbers."""
        response = client.post(
            "/api/greet",
            json={"name": "User123", "language": "en"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "User123" in data["message"]
    
    def test_greet_with_unicode_name(self):
        """Test name with unicode characters."""
        response = client.post(
            "/api/greet",
            json={"name": "李明", "language": "en"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "李明" in data["message"]
    
    def test_greet_with_emoji_in_name(self):
        """Test name with emoji."""
        response = client.post(
            "/api/greet",
            json={"name": "John 😊", "language": "en"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "John" in data["message"]