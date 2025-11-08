"""Comprehensive tests for the Greeting API."""
import pytest
from fastapi.testclient import TestClient
from backend.main import app, GREETINGS

# Create test client
client = TestClient(app)


class TestRootEndpoint:
    """Tests for root endpoint."""
    
    def test_root_endpoint(self):
        """Test root endpoint returns correct response."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "message" in data
        assert "version" in data


class TestHealthEndpoint:
    """Tests for health check endpoint."""
    
    def test_health_check(self):
        """Test health check endpoint returns healthy status."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestGreetingEndpoint:
    """Tests for greeting endpoint."""
    
    def test_greet_user_english(self):
        """Test greeting user in English."""
        response = client.post(
            "/api/greet",
            json={"name": "Alice", "language": "en"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Alice"
        assert data["language"] == "en"
        assert "Alice" in data["message"]
        assert "Hello" in data["message"]
    
    def test_greet_user_spanish(self):
        """Test greeting user in Spanish."""
        response = client.post(
            "/api/greet",
            json={"name": "Carlos", "language": "es"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Carlos"
        assert data["language"] == "es"
        assert "Carlos" in data["message"]
        assert "Hola" in data["message"]
    
    def test_greet_user_french(self):
        """Test greeting user in French."""
        response = client.post(
            "/api/greet",
            json={"name": "Marie", "language": "fr"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Marie"
        assert data["language"] == "fr"
        assert "Marie" in data["message"]
        assert "Bonjour" in data["message"]
    
    def test_greet_user_german(self):
        """Test greeting user in German."""
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
    
    def test_greet_user_italian(self):
        """Test greeting user in Italian."""
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
    
    def test_greet_user_default_language(self):
        """Test greeting user with default language (English)."""
        response = client.post(
            "/api/greet",
            json={"name": "Bob"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Bob"
        assert data["language"] == "en"
        assert "Bob" in data["message"]
    
    def test_greet_user_unsupported_language(self):
        """Test greeting user with unsupported language defaults to English."""
        response = client.post(
            "/api/greet",
            json={"name": "John", "language": "xyz"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "John"
        assert data["language"] == "en"  # Should default to English
        assert "John" in data["message"]
    
    def test_greet_user_case_insensitive_language(self):
        """Test that language parameter is case insensitive."""
        response = client.post(
            "/api/greet",
            json={"name": "Alice", "language": "EN"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["language"] == "en"
    
    def test_greet_user_missing_name(self):
        """Test that missing name returns validation error."""
        response = client.post(
            "/api/greet",
            json={"language": "en"}
        )
        assert response.status_code == 422  # Validation error
    
    def test_greet_user_empty_name(self):
        """Test that empty name returns validation error."""
        response = client.post(
            "/api/greet",
            json={"name": "", "language": "en"}
        )
        assert response.status_code == 422  # Validation error
    
    def test_greet_user_special_characters(self):
        """Test greeting with special characters in name."""
        response = client.post(
            "/api/greet",
            json={"name": "José García-López", "language": "es"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "José García-López"
        assert "José García-López" in data["message"]
    
    def test_greet_user_long_name(self):
        """Test greeting with long name."""
        long_name = "A" * 100
        response = client.post(
            "/api/greet",
            json={"name": long_name, "language": "en"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == long_name
        assert long_name in data["message"]


class TestLanguagesEndpoint:
    """Tests for languages endpoint."""
    
    def test_get_supported_languages(self):
        """Test getting list of supported languages."""
        response = client.get("/api/languages")
        assert response.status_code == 200
        data = response.json()
        assert "languages" in data
        assert "count" in data
        assert isinstance(data["languages"], list)
        assert data["count"] == len(GREETINGS)
        
        # Verify all expected languages are present
        expected_languages = ["en", "es", "fr", "de", "it"]
        for lang in expected_languages:
            assert lang in data["languages"]


class TestCORS:
    """Tests for CORS configuration."""
    
    def test_cors_headers_present(self):
        """Test that CORS headers are present in response."""
        response = client.options(
            "/api/greet",
            headers={"Origin": "http://localhost",
                    "Access-Control-Request-Method": "POST"}
        )
        assert "access-control-allow-origin" in response.headers


class TestResponseModels:
    """Tests for response model validation."""
    
    def test_greeting_response_model(self):
        """Test that response matches expected model."""
        response = client.post(
            "/api/greet",
            json={"name": "Test", "language": "en"}
        )
        data = response.json()
        
        # Verify all required fields are present
        assert "message" in data
        assert "name" in data
        assert "language" in data
        
        # Verify field types
        assert isinstance(data["message"], str)
        assert isinstance(data["name"], str)
        assert isinstance(data["language"], str)


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""
    
    def test_greet_with_numeric_name(self):
        """Test greeting with numeric characters in name."""
        response = client.post(
            "/api/greet",
            json={"name": "User123", "language": "en"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "User123" in data["message"]
    
    def test_greet_with_emoji_in_name(self):
        """Test greeting with emoji in name."""
        response = client.post(
            "/api/greet",
            json={"name": "Alice 🌿", "language": "en"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "Alice 🌿" in data["message"]
    
    def test_multiple_consecutive_requests(self):
        """Test multiple consecutive requests work correctly."""
        names = ["Alice", "Bob", "Charlie", "David", "Eve"]
        
        for name in names:
            response = client.post(
                "/api/greet",
                json={"name": name, "language": "en"}
            )
            assert response.status_code == 200
            data = response.json()
            assert data["name"] == name
    
    def test_all_supported_languages(self):
        """Test that all supported languages work correctly."""
        for language in GREETINGS.keys():
            response = client.post(
                "/api/greet",
                json={"name": "Test", "language": language}
            )
            assert response.status_code == 200
            data = response.json()
            assert data["language"] == language
            assert "Test" in data["message"]