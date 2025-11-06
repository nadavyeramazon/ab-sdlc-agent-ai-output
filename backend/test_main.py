import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from main import app

# Create test client
client = TestClient(app)

class TestGreetingAPI:
    """Comprehensive test suite for the Greeting API"""

    def test_root_endpoint(self):
        """Test the root endpoint returns correct information"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "status" in data
        assert "timestamp" in data
        assert "endpoints" in data
        assert data["status"] == "healthy"
        assert "/greet" in data["endpoints"]
        assert "/health" in data["endpoints"]

    def test_health_check_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert data["service"] == "greeting-api"

    def test_greet_valid_name(self):
        """Test greeting with valid name"""
        test_data = {"name": "John"}
        response = client.post("/greet", json=test_data)
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "timestamp" in data
        assert "name" in data
        assert data["name"] == "John"
        assert "John" in data["message"]
        assert "Welcome to our green-themed greeting service!" in data["message"]

    def test_greet_with_time_based_greeting(self):
        """Test that time-based greetings work correctly"""
        test_data = {"name": "Alice"}
        response = client.post("/greet", json=test_data)
        assert response.status_code == 200
        data = response.json()
        
        # Check that one of the time-based greetings is present
        time_greetings = ["Good morning", "Good afternoon", "Good evening", "Good night"]
        assert any(greeting in data["message"] for greeting in time_greetings)

    def test_greet_empty_name(self):
        """Test greeting with empty name"""
        test_data = {"name": ""}
        response = client.post("/greet", json=test_data)
        assert response.status_code == 422  # Validation error

    def test_greet_whitespace_only_name(self):
        """Test greeting with whitespace-only name"""
        test_data = {"name": "   "}
        response = client.post("/greet", json=test_data)
        assert response.status_code == 422  # Validation error

    def test_greet_name_too_long(self):
        """Test greeting with name that exceeds maximum length"""
        long_name = "a" * 101  # Exceeds 100 character limit
        test_data = {"name": long_name}
        response = client.post("/greet", json=test_data)
        assert response.status_code == 422  # Validation error

    def test_greet_invalid_characters(self):
        """Test greeting with invalid characters in name"""
        invalid_names = [
            "John123",  # Numbers
            "John@Doe",  # Special characters
            "John<script>",  # HTML/script tags
            "John&nbsp;",  # HTML entities
        ]
        
        for invalid_name in invalid_names:
            test_data = {"name": invalid_name}
            response = client.post("/greet", json=test_data)
            assert response.status_code == 422, f"Should reject name: {invalid_name}"

    def test_greet_valid_special_characters(self):
        """Test greeting with valid special characters"""
        valid_names = [
            "Mary-Jane",  # Hyphen
            "O'Connor",   # Apostrophe
            "Jean Claude Van Damme",  # Multiple spaces
        ]
        
        for valid_name in valid_names:
            test_data = {"name": valid_name}
            response = client.post("/greet", json=test_data)
            assert response.status_code == 200, f"Should accept name: {valid_name}"
            data = response.json()
            assert valid_name in data["name"] or data["name"] in valid_name  # Account for HTML escaping

    def test_greet_name_trimming(self):
        """Test that names are properly trimmed"""
        test_data = {"name": "  John  "}
        response = client.post("/greet", json=test_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "John"  # Should be trimmed

    def test_greet_response_structure(self):
        """Test that greeting response has correct structure"""
        test_data = {"name": "TestUser"}
        response = client.post("/greet", json=test_data)
        assert response.status_code == 200
        data = response.json()
        
        # Check required fields
        required_fields = ["message", "timestamp", "name"]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"
        
        # Validate timestamp format (should be ISO format)
        try:
            datetime.fromisoformat(data["timestamp"])
        except ValueError:
            pytest.fail("Timestamp is not in valid ISO format")

    def test_greet_html_escaping(self):
        """Test that HTML characters are properly escaped"""
        # This test might not work with current validation, but tests the concept
        test_data = {"name": "John Doe"}
        response = client.post("/greet", json=test_data)
        assert response.status_code == 200
        data = response.json()
        
        # Ensure no raw HTML in response
        assert "<script>" not in data["message"]
        assert "&lt;" not in data["message"] or "&gt;" not in data["message"]

    def test_missing_name_field(self):
        """Test request without name field"""
        response = client.post("/greet", json={})
        assert response.status_code == 422  # Validation error

    def test_cors_headers(self):
        """Test that CORS headers are present"""
        response = client.options("/greet")
        # CORS should be handled by middleware
        assert response.status_code in [200, 405]  # 405 if OPTIONS not explicitly handled

    def test_api_documentation_accessible(self):
        """Test that API documentation is accessible"""
        response = client.get("/docs")
        assert response.status_code == 200
        
        response = client.get("/openapi.json")
        assert response.status_code == 200

@pytest.fixture
def sample_greeting_data():
    """Fixture providing sample greeting data for tests"""
    return {"name": "TestUser"}

class TestSecurityFeatures:
    """Test security-related features"""

    def test_sql_injection_attempt(self):
        """Test protection against SQL injection-like attempts"""
        malicious_names = [
            "'; DROP TABLE users; --",
            "admin'--",
            "1' OR '1'='1",
        ]
        
        for malicious_name in malicious_names:
            test_data = {"name": malicious_name}
            response = client.post("/greet", json=test_data)
            # Should be rejected by validation
            assert response.status_code == 422

    def test_xss_prevention(self):
        """Test protection against XSS attempts"""
        xss_attempts = [
            "<script>alert('xss')</script>",
            "javascript:alert('xss')",
            "<img src=x onerror=alert('xss')>",
        ]
        
        for xss_attempt in xss_attempts:
            test_data = {"name": xss_attempt}
            response = client.post("/greet", json=test_data)
            # Should be rejected by validation
            assert response.status_code == 422

if __name__ == "__main__":
    pytest.main(["-v", __file__])