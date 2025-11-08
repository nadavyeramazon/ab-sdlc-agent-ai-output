"""Comprehensive tests for the Greeting API"""
import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    """Create a test client fixture"""
    return TestClient(app)


class TestRootEndpoint:
    """Tests for the root endpoint"""
    
    def test_root_returns_welcome_message(self, client):
        """Test that root endpoint returns welcome information"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Welcome to the Greeting API" in data["message"]
        assert "version" in data
        assert "endpoints" in data
    
    def test_root_contains_endpoint_info(self, client):
        """Test that root endpoint contains endpoint information"""
        response = client.get("/")
        data = response.json()
        assert "/greet" in data["endpoints"]
        assert "/health" in data["endpoints"]


class TestHealthEndpoint:
    """Tests for the health check endpoint"""
    
    def test_health_check_returns_healthy(self, client):
        """Test that health check returns healthy status"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "greeting-api"


class TestGreetEndpoint:
    """Tests for the greet endpoint"""
    
    def test_greet_user_english(self, client):
        """Test greeting a user in English"""
        response = client.post(
            "/greet",
            json={"name": "Alice", "language": "en"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Alice"
        assert data["language"] == "en"
        assert "Hello, Alice" in data["message"]
        assert "Welcome" in data["message"]
    
    def test_greet_user_spanish(self, client):
        """Test greeting a user in Spanish"""
        response = client.post(
            "/greet",
            json={"name": "Carlos", "language": "es"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Carlos"
        assert data["language"] == "es"
        assert "¡Hola, Carlos" in data["message"]
        assert "Bienvenido" in data["message"]
    
    def test_greet_user_french(self, client):
        """Test greeting a user in French"""
        response = client.post(
            "/greet",
            json={"name": "Marie", "language": "fr"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Marie"
        assert data["language"] == "fr"
        assert "Bonjour, Marie" in data["message"]
        assert "Bienvenue" in data["message"]
    
    def test_greet_user_german(self, client):
        """Test greeting a user in German"""
        response = client.post(
            "/greet",
            json={"name": "Hans", "language": "de"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Hans"
        assert data["language"] == "de"
        assert "Hallo, Hans" in data["message"]
        assert "Willkommen" in data["message"]
    
    def test_greet_user_italian(self, client):
        """Test greeting a user in Italian"""
        response = client.post(
            "/greet",
            json={"name": "Giuseppe", "language": "it"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Giuseppe"
        assert data["language"] == "it"
        assert "Ciao, Giuseppe" in data["message"]
        assert "Benvenuto" in data["message"]
    
    def test_greet_user_default_language(self, client):
        """Test greeting with default language (English)"""
        response = client.post(
            "/greet",
            json={"name": "Bob"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Bob"
        assert data["language"] == "en"
        assert "Hello, Bob" in data["message"]
    
    def test_greet_user_with_whitespace(self, client):
        """Test that names with whitespace are trimmed"""
        response = client.post(
            "/greet",
            json={"name": "  Alice  ", "language": "en"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Alice"
    
    def test_greet_user_empty_name(self, client):
        """Test that empty name returns validation error"""
        response = client.post(
            "/greet",
            json={"name": "", "language": "en"}
        )
        assert response.status_code == 422
    
    def test_greet_user_whitespace_only_name(self, client):
        """Test that whitespace-only name returns validation error"""
        response = client.post(
            "/greet",
            json={"name": "   ", "language": "en"}
        )
        assert response.status_code == 422
    
    def test_greet_user_invalid_language(self, client):
        """Test that invalid language returns validation error"""
        response = client.post(
            "/greet",
            json={"name": "Alice", "language": "xyz"}
        )
        assert response.status_code == 422
    
    def test_greet_user_missing_name(self, client):
        """Test that missing name returns validation error"""
        response = client.post(
            "/greet",
            json={"language": "en"}
        )
        assert response.status_code == 422
    
    def test_greet_user_invalid_json(self, client):
        """Test that invalid JSON returns error"""
        response = client.post(
            "/greet",
            data="not json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422
    
    def test_greet_multiple_users(self, client):
        """Test greeting multiple users in sequence"""
        names = ["Alice", "Bob", "Charlie", "Diana"]
        languages = ["en", "es", "fr", "de"]
        
        for name, language in zip(names, languages):
            response = client.post(
                "/greet",
                json={"name": name, "language": language}
            )
            assert response.status_code == 200
            data = response.json()
            assert data["name"] == name
            assert data["language"] == language
            assert name in data["message"]


class TestCORS:
    """Tests for CORS configuration"""
    
    def test_cors_headers_present(self, client):
        """Test that CORS headers are present in response"""
        response = client.options(
            "/greet",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST"
            }
        )
        # CORS middleware should handle OPTIONS requests
        assert response.status_code in [200, 204]


class TestResponseModels:
    """Tests for response model validation"""
    
    def test_greet_response_has_required_fields(self, client):
        """Test that response contains all required fields"""
        response = client.post(
            "/greet",
            json={"name": "Alice", "language": "en"}
        )
        data = response.json()
        assert "message" in data
        assert "name" in data
        assert "language" in data
        assert isinstance(data["message"], str)
        assert isinstance(data["name"], str)
        assert isinstance(data["language"], str)
