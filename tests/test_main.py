import pytest
from fastapi.testclient import TestClient
from backend.main import app, GREETINGS


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


class TestRootEndpoint:
    """Tests for the root endpoint"""
    
    def test_root_endpoint(self, client):
        """Test that root endpoint returns API information"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "endpoints" in data
        assert data["message"] == "Greeting User API"
        assert data["version"] == "1.0.0"


class TestHealthCheck:
    """Tests for the health check endpoint"""
    
    def test_health_check(self, client):
        """Test that health check endpoint returns healthy status"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "greeting-api"


class TestGreetUserPOST:
    """Tests for POST /greet endpoint"""
    
    def test_greet_user_default_language(self, client):
        """Test greeting with default language (English)"""
        response = client.post(
            "/greet",
            json={"name": "Alice"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Alice"
        assert data["language"] == "en"
        assert "Alice" in data["message"]
        assert data["message"] == GREETINGS["en"].format(name="Alice")
    
    def test_greet_user_english(self, client):
        """Test greeting in English"""
        response = client.post(
            "/greet",
            json={"name": "Bob", "language": "en"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Bob"
        assert data["language"] == "en"
        assert data["message"] == GREETINGS["en"].format(name="Bob")
    
    def test_greet_user_spanish(self, client):
        """Test greeting in Spanish"""
        response = client.post(
            "/greet",
            json={"name": "Carlos", "language": "es"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Carlos"
        assert data["language"] == "es"
        assert data["message"] == GREETINGS["es"].format(name="Carlos")
    
    def test_greet_user_french(self, client):
        """Test greeting in French"""
        response = client.post(
            "/greet",
            json={"name": "Marie", "language": "fr"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Marie"
        assert data["language"] == "fr"
        assert data["message"] == GREETINGS["fr"].format(name="Marie")
    
    def test_greet_user_german(self, client):
        """Test greeting in German"""
        response = client.post(
            "/greet",
            json={"name": "Hans", "language": "de"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Hans"
        assert data["language"] == "de"
        assert data["message"] == GREETINGS["de"].format(name="Hans")
    
    def test_greet_user_case_insensitive_language(self, client):
        """Test that language code is case insensitive"""
        response = client.post(
            "/greet",
            json={"name": "David", "language": "EN"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["language"] == "en"
    
    def test_greet_user_unsupported_language(self, client):
        """Test greeting with unsupported language returns error"""
        response = client.post(
            "/greet",
            json={"name": "Eve", "language": "it"}
        )
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "Unsupported language" in data["detail"]
    
    def test_greet_user_empty_name(self, client):
        """Test that empty name returns validation error"""
        response = client.post(
            "/greet",
            json={"name": "", "language": "en"}
        )
        assert response.status_code == 422  # Validation error
    
    def test_greet_user_missing_name(self, client):
        """Test that missing name returns validation error"""
        response = client.post(
            "/greet",
            json={"language": "en"}
        )
        assert response.status_code == 422  # Validation error
    
    def test_greet_user_long_name(self, client):
        """Test greeting with maximum length name"""
        long_name = "A" * 100
        response = client.post(
            "/greet",
            json={"name": long_name, "language": "en"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == long_name
    
    def test_greet_user_too_long_name(self, client):
        """Test that name exceeding max length returns validation error"""
        too_long_name = "A" * 101
        response = client.post(
            "/greet",
            json={"name": too_long_name, "language": "en"}
        )
        assert response.status_code == 422  # Validation error
    
    def test_greet_user_special_characters(self, client):
        """Test greeting with special characters in name"""
        response = client.post(
            "/greet",
            json={"name": "María José", "language": "es"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "María José"


class TestGreetUserGET:
    """Tests for GET /greet/{name} endpoint"""
    
    def test_greet_user_by_name_default_language(self, client):
        """Test GET greeting with default language"""
        response = client.get("/greet/Alice")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Alice"
        assert data["language"] == "en"
        assert data["message"] == GREETINGS["en"].format(name="Alice")
    
    def test_greet_user_by_name_with_language(self, client):
        """Test GET greeting with specified language"""
        response = client.get("/greet/Carlos?language=es")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Carlos"
        assert data["language"] == "es"
        assert data["message"] == GREETINGS["es"].format(name="Carlos")
    
    def test_greet_user_by_name_all_languages(self, client):
        """Test GET greeting in all supported languages"""
        for lang_code in GREETINGS.keys():
            response = client.get(f"/greet/TestUser?language={lang_code}")
            assert response.status_code == 200
            data = response.json()
            assert data["language"] == lang_code
            assert data["message"] == GREETINGS[lang_code].format(name="TestUser")
    
    def test_greet_user_by_name_unsupported_language(self, client):
        """Test GET greeting with unsupported language"""
        response = client.get("/greet/Frank?language=ja")
        assert response.status_code == 400
        data = response.json()
        assert "Unsupported language" in data["detail"]
    
    def test_greet_user_by_name_with_spaces(self, client):
        """Test GET greeting with name containing spaces"""
        response = client.get("/greet/John%20Doe")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "John Doe"
    
    def test_greet_user_by_name_special_characters(self, client):
        """Test GET greeting with special characters"""
        response = client.get("/greet/José")
        assert response.status_code == 200
        data = response.json()
        assert "José" in data["name"]


class TestResponseModels:
    """Tests for response model structure"""
    
    def test_greeting_response_structure(self, client):
        """Test that greeting response has correct structure"""
        response = client.post(
            "/greet",
            json={"name": "Test", "language": "en"}
        )
        assert response.status_code == 200
        data = response.json()
        
        # Check all required fields are present
        assert "message" in data
        assert "name" in data
        assert "language" in data
        
        # Check field types
        assert isinstance(data["message"], str)
        assert isinstance(data["name"], str)
        assert isinstance(data["language"], str)
        
        # Check field values
        assert len(data["message"]) > 0
        assert len(data["name"]) > 0
        assert len(data["language"]) > 0


class TestErrorHandling:
    """Tests for error handling"""
    
    def test_invalid_json(self, client):
        """Test that invalid JSON returns error"""
        response = client.post(
            "/greet",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422
    
    def test_invalid_method(self, client):
        """Test that invalid HTTP method returns error"""
        response = client.put("/greet")
        assert response.status_code == 405  # Method not allowed
    
    def test_nonexistent_endpoint(self, client):
        """Test that nonexistent endpoint returns 404"""
        response = client.get("/nonexistent")
        assert response.status_code == 404


class TestCORSConfiguration:
    """Tests for CORS configuration"""
    
    def test_cors_headers_present(self, client):
        """Test that CORS headers are present in response"""
        response = client.options(
            "/greet",
            headers={"Origin": "http://localhost:3000"}
        )
        # CORS middleware should handle OPTIONS requests
        assert response.status_code in [200, 204]


class TestEdgeCases:
    """Tests for edge cases"""
    
    def test_name_with_only_spaces(self, client):
        """Test that name with only spaces is rejected"""
        response = client.post(
            "/greet",
            json={"name": "   ", "language": "en"}
        )
        assert response.status_code == 422  # Validation error
    
    def test_name_with_numbers(self, client):
        """Test greeting with numbers in name"""
        response = client.post(
            "/greet",
            json={"name": "Agent007", "language": "en"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "Agent007" in data["message"]
    
    def test_name_with_emojis(self, client):
        """Test greeting with emojis in name"""
        response = client.post(
            "/greet",
            json={"name": "🎉 Party", "language": "en"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "🎉 Party" in data["message"]
    
    def test_multiple_requests(self, client):
        """Test multiple consecutive requests"""
        for i in range(5):
            response = client.post(
                "/greet",
                json={"name": f"User{i}", "language": "en"}
            )
            assert response.status_code == 200
            data = response.json()
            assert data["name"] == f"User{i}"
