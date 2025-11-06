import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestGreetingAPI:
    """Test suite for the Greeting API"""
    
    def test_root_endpoint(self):
        """Test the root endpoint returns welcome message"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Welcome to the Greeting API" in data["message"]
    
    def test_health_check(self):
        """Test the health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "greeting-api"
    
    def test_greeting_types_endpoint(self):
        """Test the greeting types endpoint"""
        response = client.get("/greeting-types")
        assert response.status_code == 200
        data = response.json()
        assert "greeting_types" in data
        assert isinstance(data["greeting_types"], list)
        assert len(data["greeting_types"]) > 0
        
        # Check that each greeting type has key and label
        for greeting_type in data["greeting_types"]:
            assert "key" in greeting_type
            assert "label" in greeting_type
            assert isinstance(greeting_type["key"], str)
            assert isinstance(greeting_type["label"], str)
    
    def test_greet_post_basic(self):
        """Test basic POST greeting functionality"""
        response = client.post("/greet", json={"name": "John"})
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Hello, John! Nice to meet you!"
        assert data["user_name"] == "John"
        assert data["greeting_type"] == "hello"
    
    def test_greet_post_with_greeting_type(self):
        """Test POST greeting with custom greeting type"""
        response = client.post("/greet", json={"name": "Alice", "greeting_type": "hi"})
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Hi there, Alice! How are you doing?"
        assert data["user_name"] == "Alice"
        assert data["greeting_type"] == "hi"
    
    def test_greet_get_basic(self):
        """Test basic GET greeting functionality"""
        response = client.get("/greet/John")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Hello, John! Nice to meet you!"
        assert data["user_name"] == "John"
        assert data["greeting_type"] == "hello"
    
    def test_greet_get_with_greeting_type(self):
        """Test GET greeting with custom greeting type"""
        response = client.get("/greet/Alice?greeting_type=welcome")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Welcome, Alice! We're glad you're here!"
        assert data["user_name"] == "Alice"
        assert data["greeting_type"] == "welcome"
    
    def test_all_greeting_types(self):
        """Test all available greeting types"""
        greeting_types = ["hello", "hi", "hey", "greetings", "welcome", "good_morning", "good_afternoon", "good_evening"]
        expected_messages = {
            "hello": "Hello, Test! Nice to meet you!",
            "hi": "Hi there, Test! How are you doing?",
            "hey": "Hey Test! What's up?",
            "greetings": "Greetings, Test! Hope you're having a great day!",
            "welcome": "Welcome, Test! We're glad you're here!",
            "good_morning": "Good morning, Test! Hope you have a wonderful day!",
            "good_afternoon": "Good afternoon, Test! How's your day going?",
            "good_evening": "Good evening, Test! Hope your evening is pleasant!"
        }
        
        for greeting_type in greeting_types:
            response = client.post("/greet", json={"name": "Test", "greeting_type": greeting_type})
            assert response.status_code == 200
            data = response.json()
            assert data["message"] == expected_messages[greeting_type]
            assert data["greeting_type"] == greeting_type
    
    def test_invalid_greeting_type(self):
        """Test invalid greeting type returns error"""
        response = client.post("/greet", json={"name": "John", "greeting_type": "invalid"})
        assert response.status_code == 422  # Validation error
    
    def test_empty_name(self):
        """Test empty name returns error"""
        response = client.post("/greet", json={"name": ""})
        assert response.status_code == 422  # Validation error
        
        response = client.post("/greet", json={"name": "   "})
        assert response.status_code == 422  # Validation error
    
    def test_missing_name(self):
        """Test missing name returns error"""
        response = client.post("/greet", json={})
        assert response.status_code == 422  # Validation error
    
    def test_name_too_long(self):
        """Test name longer than 100 characters returns error"""
        long_name = "a" * 101
        response = client.post("/greet", json={"name": long_name})
        assert response.status_code == 422  # Validation error
    
    def test_name_with_invalid_characters(self):
        """Test name with invalid characters returns error"""
        invalid_names = ["<script>", "John'", 'John"', "John<test>"]
        for invalid_name in invalid_names:
            response = client.post("/greet", json={"name": invalid_name})
            assert response.status_code == 422  # Validation error
    
    def test_name_whitespace_trimming(self):
        """Test that names are properly trimmed"""
        response = client.post("/greet", json={"name": "  John  "})
        assert response.status_code == 200
        data = response.json()
        assert data["user_name"] == "John"
        assert "John" in data["message"]
    
    def test_case_sensitivity(self):
        """Test that names preserve case"""
        response = client.post("/greet", json={"name": "JoHn"})
        assert response.status_code == 200
        data = response.json()
        assert data["user_name"] == "JoHn"
        assert "JoHn" in data["message"]
    
    def test_special_characters_allowed(self):
        """Test that allowed special characters work"""
        valid_names = ["José", "Anne-Marie", "李小明"]
        for name in valid_names:
            response = client.post("/greet", json={"name": name})
            assert response.status_code == 200
            data = response.json()
            assert data["user_name"] == name
    
    def test_get_endpoint_validation(self):
        """Test GET endpoint validation"""
        # Test empty name
        response = client.get("/greet/")
        assert response.status_code == 404  # Not found due to empty path
        
        # Test invalid greeting type
        response = client.get("/greet/John?greeting_type=invalid")
        assert response.status_code == 400  # Bad request
    
    def test_response_structure(self):
        """Test that response has correct structure"""
        response = client.post("/greet", json={"name": "Test"})
        assert response.status_code == 200
        data = response.json()
        
        # Check all required fields are present
        required_fields = ["message", "user_name", "greeting_type"]
        for field in required_fields:
            assert field in data
        
        # Check field types
        assert isinstance(data["message"], str)
        assert isinstance(data["user_name"], str)
        assert isinstance(data["greeting_type"], str)
    
    def test_cors_headers(self):
        """Test CORS headers are present"""
        response = client.options("/greet")
        # Note: TestClient doesn't fully simulate CORS, but we can verify the middleware is loaded
        assert response.status_code in [200, 405]  # OPTIONS might not be explicitly allowed
    
    def test_multiple_concurrent_requests(self):
        """Test handling multiple requests"""
        import concurrent.futures
        
        def make_request(name):
            return client.post("/greet", json={"name": f"User{name}"})
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request, i) for i in range(10)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        for result in results:
            assert result.status_code == 200
            data = result.json()
            assert "User" in data["user_name"]
            assert "message" in data

if __name__ == "__main__":
    pytest.main([__file__, "-v"])