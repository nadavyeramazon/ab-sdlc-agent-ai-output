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
    
    def test_root_contains_supported_languages(self, client):
        """Test that root endpoint lists supported languages"""
        response = client.get("/")
        data = response.json()
        assert "supported_languages" in data
        assert "en" in data["supported_languages"]
        assert len(data["supported_languages"]) == 5


class TestHealthEndpoint:
    """Tests for the health check endpoint"""
    
    def test_health_check_returns_healthy(self, client):
        """Test that health check returns healthy status"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "greeting-api"
        assert "version" in data
        assert "timestamp" in data


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
        assert "timestamp" in data
    
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
    
    def test_greet_user_too_long_name(self, client):
        """Test that name exceeding max length returns validation error"""
        long_name = "A" * 101
        response = client.post(
            "/greet",
            json={"name": long_name, "language": "en"}
        )
        assert response.status_code == 422
    
    def test_greet_user_max_length_name(self, client):
        """Test that name at max length is accepted"""
        max_name = "A" * 100
        response = client.post(
            "/greet",
            json={"name": max_name, "language": "en"}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["name"]) == 100
    
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
    
    def test_greet_special_characters_in_name(self, client):
        """Test greeting with special characters in name"""
        names = ["José", "François", "Müller", "O'Brien"]
        for name in names:
            response = client.post(
                "/greet",
                json={"name": name, "language": "en"}
            )
            assert response.status_code == 200
            data = response.json()
            assert data["name"] == name


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
        assert "timestamp" in data
        assert isinstance(data["message"], str)
        assert isinstance(data["name"], str)
        assert isinstance(data["language"], str)
        assert isinstance(data["timestamp"], str)
    
    def test_health_response_structure(self, client):
        """Test that health check response has correct structure"""
        response = client.get("/health")
        data = response.json()
        required_fields = ["status", "service", "version", "timestamp"]
        for field in required_fields:
            assert field in data, f"Missing field: {field}"


class TestEdgeCases:
    """Tests for edge cases and boundary conditions"""
    
    def test_greet_with_unicode_emoji_name(self, client):
        """Test greeting with unicode and emoji in name"""
        response = client.post(
            "/greet",
            json={"name": "Alice 😊", "language": "en"}
        )
        assert response.status_code == 200
    
    def test_greet_concurrent_requests(self, client):
        """Test handling multiple concurrent requests"""
        import concurrent.futures
        
        def make_request(i):
            return client.post(
                "/greet",
                json={"name": f"User{i}", "language": "en"}
            )
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request, i) for i in range(20)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        assert all(r.status_code == 200 for r in results)
        assert len(results) == 20