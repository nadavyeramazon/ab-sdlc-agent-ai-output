import pytest
from fastapi.testclient import TestClient
from main import app
import re

client = TestClient(app)


class TestHealthEndpoint:
    """Test suite for the /health endpoint."""
    
    def test_health_check_returns_200(self):
        """Test that health endpoint returns 200 status code."""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_check_returns_healthy_status(self):
        """Test that health endpoint returns correct status."""
        response = client.get("/health")
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_health_check_has_cors_headers(self):
        """Test that health endpoint includes CORS headers."""
        response = client.get(
            "/health",
            headers={"Origin": "http://localhost:3000"}
        )
        assert "access-control-allow-origin" in response.headers


class TestHelloEndpoint:
    """Test suite for the /api/hello endpoint."""
    
    def test_hello_returns_200(self):
        """Test that hello endpoint returns 200 status code."""
        response = client.get("/api/hello")
        assert response.status_code == 200
    
    def test_hello_returns_message(self):
        """Test that hello endpoint returns expected message."""
        response = client.get("/api/hello")
        data = response.json()
        assert "message" in data
        assert data["message"] == "Hello from the backend!"
    
    def test_hello_has_cors_headers(self):
        """Test that hello endpoint includes CORS headers."""
        response = client.get(
            "/api/hello",
            headers={"Origin": "http://localhost:3000"}
        )
        assert "access-control-allow-origin" in response.headers


class TestGreetEndpoint:
    """Test suite for the /api/greet endpoint."""
    
    def test_greet_with_valid_name_returns_200(self):
        """Test API-001: Valid name submission returns 200."""
        response = client.post("/api/greet", json={"name": "Alice"})
        assert response.status_code == 200
    
    def test_greet_with_valid_name_returns_greeting(self):
        """Test API-001: Valid name returns personalized greeting."""
        response = client.post("/api/greet", json={"name": "Alice"})
        data = response.json()
        assert "greeting" in data
        assert "Hello, Alice! Welcome to our purple-themed app!" in data["greeting"]
    
    def test_greet_with_valid_name_returns_timestamp(self):
        """Test API-006: Response includes ISO 8601 timestamp."""
        response = client.post("/api/greet", json={"name": "Alice"})
        data = response.json()
        assert "timestamp" in data
        # Validate ISO 8601 format with regex
        iso_pattern = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}Z'
        assert re.match(iso_pattern, data["timestamp"])
    
    def test_greet_with_empty_name_returns_400(self):
        """Test API-002: Empty name string returns 400."""
        response = client.post("/api/greet", json={"name": ""})
        assert response.status_code == 400
    
    def test_greet_with_empty_name_returns_error_message(self):
        """Test API-002: Empty name returns appropriate error message."""
        response = client.post("/api/greet", json={"name": ""})
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Name cannot be empty"
    
    def test_greet_with_whitespace_only_name_returns_400(self):
        """Test API-003: Whitespace-only name returns 400."""
        response = client.post("/api/greet", json={"name": "   "})
        assert response.status_code == 400
    
    def test_greet_with_whitespace_only_name_returns_error_message(self):
        """Test API-003: Whitespace-only name returns error message."""
        response = client.post("/api/greet", json={"name": "   "})
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Name cannot be empty"
    
    def test_greet_with_name_containing_spaces(self):
        """Test API-004: Name with spaces is handled correctly."""
        response = client.post("/api/greet", json={"name": "John Doe"})
        assert response.status_code == 200
        data = response.json()
        assert "John Doe" in data["greeting"]
    
    def test_greet_with_special_characters(self):
        """Test API-005: Name with special characters is handled correctly."""
        response = client.post("/api/greet", json={"name": "José"})
        assert response.status_code == 200
        data = response.json()
        assert "José" in data["greeting"]
    
    def test_greet_missing_name_field_returns_422(self):
        """Test that missing name field returns 422 (FastAPI validation)."""
        response = client.post("/api/greet", json={})
        assert response.status_code == 422
    
    def test_greet_has_cors_headers(self):
        """Test API-007: Response includes CORS headers."""
        response = client.post(
            "/api/greet",
            json={"name": "Test"},
            headers={"Origin": "http://localhost:3000"}
        )
        assert "access-control-allow-origin" in response.headers
        assert response.headers["access-control-allow-origin"] == "http://localhost:3000"


class TestCORSConfiguration:
    """Test suite for CORS configuration."""
    
    def test_cors_allows_post_method(self):
        """Test that CORS allows POST method."""
        response = client.options(
            "/api/greet",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST"
            }
        )
        assert response.status_code == 200
    
    def test_cors_allows_frontend_origin(self):
        """Test that CORS allows requests from frontend origin."""
        response = client.get(
            "/api/hello",
            headers={"Origin": "http://localhost:3000"}
        )
        assert response.headers["access-control-allow-origin"] == "http://localhost:3000"


class TestRegressionTests:
    """Regression test suite to ensure existing functionality is preserved."""
    
    def test_reg_008_hello_endpoint_returns_valid_json(self):
        """REG-008: Direct GET to /api/hello returns valid JSON."""
        response = client.get("/api/hello")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "message" in data
    
    def test_reg_009_health_endpoint_returns_healthy(self):
        """REG-009: Direct GET to /health returns healthy status."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_reg_010_hello_has_cors_headers(self):
        """REG-010: /api/hello response includes CORS headers."""
        response = client.get(
            "/api/hello",
            headers={"Origin": "http://localhost:3000"}
        )
        assert "access-control-allow-origin" in response.headers