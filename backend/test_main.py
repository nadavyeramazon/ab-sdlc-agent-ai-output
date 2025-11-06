import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestRootEndpoint:
    """Tests for the root endpoint"""
    
    def test_root_endpoint_returns_welcome_message(self):
        """Test that root endpoint returns correct welcome message"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["message"] == "Welcome to the Greeting API"
        assert "version" in data
    
    def test_root_endpoint_returns_json(self):
        """Test that root endpoint returns JSON content type"""
        response = client.get("/")
        assert response.headers["content-type"] == "application/json"


class TestGreetEndpoint:
    """Tests for the greeting endpoint"""
    
    def test_greet_with_valid_name(self):
        """Test greeting with a valid name"""
        response = client.post(
            "/greet",
            json={"name": "Alice"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Alice" in data["message"]
        assert "Welcome to our green-themed application" in data["message"]
    
    def test_greet_with_name_containing_spaces(self):
        """Test greeting with a name containing spaces"""
        response = client.post(
            "/greet",
            json={"name": "John Doe"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "John Doe" in data["message"]
    
    def test_greet_with_name_containing_hyphen(self):
        """Test greeting with a name containing hyphen"""
        response = client.post(
            "/greet",
            json={"name": "Mary-Jane"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "Mary-Jane" in data["message"]
    
    def test_greet_with_name_containing_apostrophe(self):
        """Test greeting with a name containing apostrophe"""
        response = client.post(
            "/greet",
            json={"name": "O'Brien"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "O'Brien" in data["message"]
    
    def test_greet_with_empty_string(self):
        """Test that empty string is rejected"""
        response = client.post(
            "/greet",
            json={"name": ""}
        )
        assert response.status_code == 422
    
    def test_greet_with_whitespace_only(self):
        """Test that whitespace-only name is rejected"""
        response = client.post(
            "/greet",
            json={"name": "   "}
        )
        assert response.status_code == 422
    
    def test_greet_with_too_long_name(self):
        """Test that names exceeding max length are rejected"""
        long_name = "A" * 101
        response = client.post(
            "/greet",
            json={"name": long_name}
        )
        assert response.status_code == 422
    
    def test_greet_with_invalid_characters(self):
        """Test that names with invalid characters are rejected"""
        response = client.post(
            "/greet",
            json={"name": "Alice<script>alert('xss')</script>"}
        )
        assert response.status_code == 422
    
    def test_greet_with_special_characters(self):
        """Test that names with special characters are rejected"""
        response = client.post(
            "/greet",
            json={"name": "Alice@#$%"}
        )
        assert response.status_code == 422
    
    def test_greet_without_name_field(self):
        """Test that missing name field is rejected"""
        response = client.post(
            "/greet",
            json={}
        )
        assert response.status_code == 422
    
    def test_greet_with_invalid_json(self):
        """Test that invalid JSON is rejected"""
        response = client.post(
            "/greet",
            data="not json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422
    
    def test_greet_returns_json(self):
        """Test that greet endpoint returns JSON content type"""
        response = client.post(
            "/greet",
            json={"name": "Alice"}
        )
        assert "application/json" in response.headers["content-type"]
    
    def test_greet_response_structure(self):
        """Test that greet response has correct structure"""
        response = client.post(
            "/greet",
            json={"name": "Alice"}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "message" in data
        assert isinstance(data["message"], str)
    
    def test_greet_trims_whitespace(self):
        """Test that names with leading/trailing whitespace are trimmed"""
        response = client.post(
            "/greet",
            json={"name": "  Alice  "}
        )
        assert response.status_code == 200
        data = response.json()
        # Should contain trimmed name
        assert "Alice" in data["message"]
        # Should not contain extra spaces around name
        assert "  Alice  " not in data["message"]


class TestHealthEndpoint:
    """Tests for the health check endpoint"""
    
    def test_health_check_returns_healthy(self):
        """Test that health check returns healthy status"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
    
    def test_health_check_returns_service_name(self):
        """Test that health check returns service identifier"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "service" in data
        assert data["service"] == "greeting-api"
    
    def test_health_check_returns_json(self):
        """Test that health check returns JSON content type"""
        response = client.get("/health")
        assert response.headers["content-type"] == "application/json"


class TestCORS:
    """Tests for CORS configuration"""
    
    def test_cors_headers_present(self):
        """Test that CORS headers are present in response"""
        response = client.options(
            "/greet",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST"
            }
        )
        assert "access-control-allow-origin" in response.headers
    
    def test_post_with_cors_origin(self):
        """Test POST request with CORS origin header"""
        response = client.post(
            "/greet",
            json={"name": "Alice"},
            headers={"Origin": "http://localhost:3000"}
        )
        assert response.status_code == 200
