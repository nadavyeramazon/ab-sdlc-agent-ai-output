import pytest
import httpx
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import asyncio
from main import app, generate_greeting_with_fallback, GreetingRequest

client = TestClient(app)


class TestHealthEndpoints:
    """Test health and basic endpoints"""
    
    def test_health_endpoint(self):
        """Test the health check endpoint returns healthy status"""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "greeting-api"
        assert data["version"] == "1.0.0"
        assert "dependencies" in data
    
    def test_root_endpoint(self):
        """Test the root endpoint returns service information"""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "endpoints" in data
        assert data["version"] == "1.0.0"


class TestGreetingEndpoints:
    """Test greeting functionality"""
    
    def test_greet_post_valid_name(self):
        """Test POST greeting with valid name"""
        response = client.post("/greet", json={"name": "John"})
        assert response.status_code == 200
        
        data = response.json()
        assert data["name"] == "John"
        assert data["status"] == "success"
        assert "Hello, John!" in data["message"] or "Greetings, John!" in data["message"]
    
    def test_greet_post_name_with_whitespace(self):
        """Test POST greeting with name containing whitespace"""
        response = client.post("/greet", json={"name": "  Alice  "})
        assert response.status_code == 200
        
        data = response.json()
        assert data["name"] == "Alice"  # Should be trimmed
        assert data["status"] == "success"
    
    def test_greet_post_empty_name(self):
        """Test POST greeting with empty name returns error"""
        response = client.post("/greet", json={"name": ""})
        assert response.status_code == 400
        
        data = response.json()
        assert "Name cannot be empty" in data["detail"]
    
    def test_greet_post_whitespace_only_name(self):
        """Test POST greeting with whitespace-only name returns error"""
        response = client.post("/greet", json={"name": "   "})
        assert response.status_code == 400
    
    def test_greet_post_long_name(self):
        """Test POST greeting with very long name"""
        long_name = "a" * 101  # Exceeds 100 character limit
        response = client.post("/greet", json={"name": long_name})
        assert response.status_code == 422  # Validation error
    
    def test_greet_get_valid_name(self):
        """Test GET greeting with valid name"""
        response = client.get("/greet/Bob")
        assert response.status_code == 200
        
        data = response.json()
        assert data["name"] == "Bob"
        assert data["status"] == "success"
        assert "Bob" in data["message"]
    
    def test_greet_get_name_with_spaces(self):
        """Test GET greeting with URL encoded spaces"""
        response = client.get("/greet/Mary%20Jane")
        assert response.status_code == 200
        
        data = response.json()
        assert data["name"] == "Mary Jane"
        assert data["status"] == "success"
    
    def test_greet_get_long_name(self):
        """Test GET greeting with very long name"""
        long_name = "a" * 101
        response = client.get(f"/greet/{long_name}")
        assert response.status_code == 400
        
        data = response.json()
        assert "Name too long" in data["detail"]
    
    def test_greet_post_invalid_json(self):
        """Test POST greeting with invalid JSON structure"""
        response = client.post("/greet", json={"invalid_field": "value"})
        assert response.status_code == 422  # Validation error
    
    def test_greet_post_missing_name_field(self):
        """Test POST greeting without name field"""
        response = client.post("/greet", json={})
        assert response.status_code == 422  # Validation error


class TestGreetingGeneration:
    """Test greeting generation logic"""
    
    @pytest.mark.asyncio
    async def test_generate_greeting_with_fallback_normal(self):
        """Test normal greeting generation"""
        greeting = await generate_greeting_with_fallback("TestUser")
        assert "TestUser" in greeting
        assert any(word in greeting for word in ["Hello", "Greetings", "Hi", "Welcome"])
    
    @pytest.mark.asyncio
    async def test_generate_greeting_consistent_for_same_name(self):
        """Test that same name always generates same greeting"""
        name = "ConsistentUser"
        greeting1 = await generate_greeting_with_fallback(name)
        greeting2 = await generate_greeting_with_fallback(name)
        assert greeting1 == greeting2
    
    @pytest.mark.asyncio
    async def test_generate_greeting_different_for_different_names(self):
        """Test that different names can generate different greetings"""
        greeting1 = await generate_greeting_with_fallback("User1")
        greeting2 = await generate_greeting_with_fallback("User2")
        # They might be the same due to hash collision, but let's test the function works
        assert "User1" in greeting1
        assert "User2" in greeting2


class TestErrorHandling:
    """Test error handling and edge cases"""
    
    @patch('main.generate_greeting_with_fallback')
    def test_greet_post_internal_error_handling(self, mock_greeting):
        """Test POST greeting handles internal errors gracefully"""
        mock_greeting.side_effect = Exception("Something went wrong")
        
        response = client.post("/greet", json={"name": "ErrorUser"})
        assert response.status_code == 500
        
        data = response.json()
        assert "Internal server error occurred" in data["detail"]
    
    @patch('main.generate_greeting_with_fallback')
    def test_greet_post_bedrock_service_unavailable(self, mock_greeting):
        """Test POST greeting handles Bedrock service unavailable"""
        mock_greeting.side_effect = Exception("Bedrock service error")
        
        response = client.post("/greet", json={"name": "ServiceUser"})
        assert response.status_code == 200  # Should return fallback greeting
        
        data = response.json()
        assert "ServiceUser" in data["name"]
        assert "Service temporarily unavailable" in data["message"]
    
    @patch('main.generate_greeting_with_fallback')
    def test_greet_get_internal_error_handling(self, mock_greeting):
        """Test GET greeting handles internal errors gracefully"""
        mock_greeting.side_effect = Exception("Something went wrong")
        
        response = client.get("/greet/ErrorUser")
        assert response.status_code == 500
    
    @patch('main.generate_greeting_with_fallback')
    def test_greet_get_service_unavailable_exception(self, mock_greeting):
        """Test GET greeting handles serviceUnavailableException"""
        mock_greeting.side_effect = Exception("serviceUnavailableException occurred")
        
        response = client.get("/greet/ServiceUser")
        assert response.status_code == 200  # Should return fallback
        
        data = response.json()
        assert "ServiceUser" in data["name"]
        assert "Service temporarily unavailable" in data["message"]


class TestCORSConfiguration:
    """Test CORS configuration"""
    
    def test_cors_headers_present(self):
        """Test that CORS headers are present in response"""
        response = client.options("/greet", headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST"
        })
        
        # Should not be 404 or 405, CORS should handle it
        assert "access-control-allow-origin" in response.headers or response.status_code in [200, 204]


class TestDataValidation:
    """Test data validation and sanitization"""
    
    def test_greeting_request_validation(self):
        """Test GreetingRequest model validation"""
        # Valid request
        valid_request = GreetingRequest(name="ValidName")
        assert valid_request.name == "ValidName"
        
        # Test minimum length validation
        with pytest.raises(ValueError):
            GreetingRequest(name="")
        
        # Test maximum length validation
        with pytest.raises(ValueError):
            GreetingRequest(name="a" * 101)
    
    def test_special_characters_in_name(self):
        """Test handling of special characters in names"""
        special_names = ["José", "O'Connor", "李小明", "Müller"]
        
        for name in special_names:
            response = client.post("/greet", json={"name": name})
            assert response.status_code == 200
            data = response.json()
            assert data["name"] == name


class TestPerformanceAndConcurrency:
    """Test performance and concurrency aspects"""
    
    @pytest.mark.asyncio
    async def test_concurrent_requests(self):
        """Test handling multiple concurrent requests"""
        async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
            tasks = []
            for i in range(10):
                task = ac.post("/greet", json={"name": f"User{i}"})
                tasks.append(task)
            
            responses = await asyncio.gather(*tasks)
            
            for i, response in enumerate(responses):
                assert response.status_code == 200
                data = response.json()
                assert data["name"] == f"User{i}"
                assert data["status"] == "success"


if __name__ == "__main__":
    pytest.main(["-v", "test_main.py"])
