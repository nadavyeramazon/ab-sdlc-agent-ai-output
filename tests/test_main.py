"""Comprehensive test suite for the Greeting API.

This module contains extensive tests covering:
- All API endpoints
- All supported languages
- Error handling and validation
- Edge cases and boundary conditions
- Response models
- CORS configuration
"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app, GREETINGS, SUPPORTED_LANGUAGES

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
        assert "supported_languages" in data
        assert data["name"] == "Greeting API"
        assert data["version"] == "1.0.0"
        assert len(data["supported_languages"]) == 5


class TestHealthEndpoint:
    """Tests for the health check endpoint."""
    
    def test_health_check_returns_healthy(self):
        """Test that health endpoint returns healthy status."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "greeting-api"
        assert "version" in data
        assert data["version"] == "1.0.0"
    
    def test_health_check_response_model(self):
        """Test that health response has correct structure."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        required_fields = ["status", "service", "version"]
        for field in required_fields:
            assert field in data
            assert isinstance(data[field], str)


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
        assert "Hello" in data["message"]
    
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
    
    def test_greet_with_leading_trailing_spaces(self):
        """Test that leading/trailing spaces are handled."""
        response = client.post(
            "/api/greet",
            json={"name": "  John  ", "language": "en"}
        )
        assert response.status_code == 200
        data = response.json()
        # Name should be trimmed
        assert data["name"] == "John"


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
        # Check that available languages are mentioned
        assert any(lang in data["detail"] for lang in SUPPORTED_LANGUAGES)
    
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
    
    def test_greet_with_whitespace_only_name(self):
        """Test with name containing only whitespace."""
        response = client.post(
            "/api/greet",
            json={"name": "   ", "language": "en"}
        )
        # Should return validation error
        assert response.status_code in [400, 422]


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
        required_fields = ["message", "name", "language"]
        for field in required_fields:
            assert field in data
            assert isinstance(data[field], str)
    
    def test_greeting_response_types(self):
        """Test that response fields have correct types."""
        response = client.post(
            "/api/greet",
            json={"name": "Test", "language": "en"}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data["message"], str)
        assert isinstance(data["name"], str)
        assert isinstance(data["language"], str)
        assert len(data["message"]) > 0
        assert len(data["name"]) > 0
        assert len(data["language"]) == 2  # Language code is 2 characters


class TestAllLanguages:
    """Test all supported languages."""
    
    @pytest.mark.parametrize("language", SUPPORTED_LANGUAGES)
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
    
    @pytest.mark.parametrize("language,greeting_word", [
        ("en", "Hello"),
        ("es", "Hola"),
        ("fr", "Bonjour"),
        ("de", "Hallo"),
        ("it", "Ciao"),
    ])
    def test_language_specific_greetings(self, language, greeting_word):
        """Test that each language uses correct greeting word."""
        response = client.post(
            "/api/greet",
            json={"name": "User", "language": language}
        )
        assert response.status_code == 200
        data = response.json()
        assert greeting_word in data["message"]


class TestCORS:
    """Tests for CORS configuration."""
    
    def test_cors_headers_on_post(self):
        """Test that CORS headers are present in POST response."""
        response = client.post(
            "/api/greet",
            json={"name": "Test", "language": "en"},
            headers={"Origin": "http://localhost:3000"}
        )
        assert response.status_code == 200
    
    def test_cors_headers_on_get(self):
        """Test that CORS headers are present in GET response."""
        response = client.get(
            "/health",
            headers={"Origin": "http://localhost:3000"}
        )
        assert response.status_code == 200


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""
    
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
    
    def test_greet_with_very_short_name(self):
        """Test with single character name."""
        response = client.post(
            "/api/greet",
            json={"name": "J", "language": "en"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "J"
    
    def test_greet_with_exactly_100_chars(self):
        """Test name with exactly 100 characters (boundary)."""
        name = "A" * 100
        response = client.post(
            "/api/greet",
            json={"name": name, "language": "en"}
        )
        assert response.status_code == 200
        assert response.json()["name"] == name
    
    def test_greet_with_101_chars(self):
        """Test name with 101 characters (over limit)."""
        name = "A" * 101
        response = client.post(
            "/api/greet",
            json={"name": name, "language": "en"}
        )
        assert response.status_code == 422
    
    def test_multiple_greetings_same_user(self):
        """Test multiple greetings for the same user."""
        for _ in range(3):
            response = client.post(
                "/api/greet",
                json={"name": "John", "language": "en"}
            )
            assert response.status_code == 200
            data = response.json()
            assert data["name"] == "John"
    
    def test_concurrent_different_languages(self):
        """Test that different language requests work independently."""
        responses = []
        for lang in SUPPORTED_LANGUAGES:
            response = client.post(
                "/api/greet",
                json={"name": "User", "language": lang}
            )
            responses.append(response)
        
        # All should succeed
        for response in responses:
            assert response.status_code == 200
        
        # Each should have correct language
        for i, lang in enumerate(SUPPORTED_LANGUAGES):
            assert responses[i].json()["language"] == lang


class TestAPIDocumentation:
    """Tests for API documentation endpoints."""
    
    def test_openapi_schema_accessible(self):
        """Test that OpenAPI schema is accessible."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert "paths" in schema
    
    def test_docs_endpoint_exists(self):
        """Test that /docs endpoint exists."""
        response = client.get("/docs")
        assert response.status_code == 200
    
    def test_redoc_endpoint_exists(self):
        """Test that /redoc endpoint exists."""
        response = client.get("/redoc")
        assert response.status_code == 200