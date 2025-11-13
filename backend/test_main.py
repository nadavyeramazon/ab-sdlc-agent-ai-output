import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from main import app

# Create test client
client = TestClient(app)

class TestHealthEndpoint:
    """Test suite for /health endpoint"""
    
    def test_health_check_returns_200(self):
        """Test that health endpoint returns 200 status code"""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_check_returns_json(self):
        """Test that health endpoint returns JSON content type"""
        response = client.get("/health")
        assert response.headers["content-type"] == "application/json"
    
    def test_health_check_returns_healthy_status(self):
        """Test that health endpoint returns status 'healthy'"""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"

class TestHelloEndpoint:
    """Test suite for /api/hello endpoint"""
    
    def test_hello_returns_200(self):
        """Test that hello endpoint returns 200 status code"""
        response = client.get("/api/hello")
        assert response.status_code == 200
    
    def test_hello_returns_json(self):
        """Test that hello endpoint returns JSON content type"""
        response = client.get("/api/hello")
        assert response.headers["content-type"] == "application/json"
    
    def test_hello_returns_correct_message(self):
        """Test that hello endpoint returns correct message"""
        response = client.get("/api/hello")
        data = response.json()
        assert "message" in data
        assert data["message"] == "Hello World from Backend!"
    
    def test_hello_returns_timestamp(self):
        """Test that hello endpoint returns a timestamp"""
        response = client.get("/api/hello")
        data = response.json()
        assert "timestamp" in data
        assert isinstance(data["timestamp"], str)
        assert len(data["timestamp"]) > 0
    
    def test_hello_timestamp_is_iso8601_format(self):
        """Test that timestamp is in ISO 8601 format"""
        response = client.get("/api/hello")
        data = response.json()
        timestamp = data["timestamp"]
        
        # Verify ISO 8601 format by parsing it
        try:
            # Remove 'Z' suffix and parse
            datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            is_valid = True
        except ValueError:
            is_valid = False
        
        assert is_valid, f"Timestamp {timestamp} is not in valid ISO 8601 format"
    
    def test_hello_timestamp_ends_with_z(self):
        """Test that timestamp ends with 'Z' (UTC indicator)"""
        response = client.get("/api/hello")
        data = response.json()
        assert data["timestamp"].endswith("Z")

class TestGreetEndpoint:
    """Test suite for /api/greet endpoint (new feature)"""
    
    def test_greet_returns_200_for_valid_name(self):
        """Test that greet endpoint returns 200 for valid name"""
        response = client.post("/api/greet", json={"name": "Alice"})
        assert response.status_code == 200
    
    def test_greet_returns_json(self):
        """Test that greet endpoint returns JSON content type"""
        response = client.post("/api/greet", json={"name": "Bob"})
        assert response.headers["content-type"] == "application/json"
    
    def test_greet_returns_correct_greeting_format(self):
        """Test that greet endpoint returns correct greeting format"""
        response = client.post("/api/greet", json={"name": "Alice"})
        data = response.json()
        assert "greeting" in data
        assert data["greeting"] == "Hello, Alice! Welcome to our purple-themed app!"
    
    def test_greet_returns_timestamp(self):
        """Test that greet endpoint returns a timestamp"""
        response = client.post("/api/greet", json={"name": "Charlie"})
        data = response.json()
        assert "timestamp" in data
        assert isinstance(data["timestamp"], str)
        assert len(data["timestamp"]) > 0
    
    def test_greet_timestamp_is_iso8601_format(self):
        """Test that timestamp is in ISO 8601 format"""
        response = client.post("/api/greet", json={"name": "David"})
        data = response.json()
        timestamp = data["timestamp"]
        
        # Verify ISO 8601 format by parsing it
        try:
            datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            is_valid = True
        except ValueError:
            is_valid = False
        
        assert is_valid, f"Timestamp {timestamp} is not in valid ISO 8601 format"
    
    def test_greet_timestamp_ends_with_z(self):
        """Test that timestamp ends with 'Z' (UTC indicator)"""
        response = client.post("/api/greet", json={"name": "Emma"})
        data = response.json()
        assert data["timestamp"].endswith("Z")
    
    def test_greet_rejects_empty_name(self):
        """Test that greet endpoint rejects empty name with 400 error"""
        response = client.post("/api/greet", json={"name": ""})
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Name cannot be empty"
    
    def test_greet_rejects_whitespace_only_name(self):
        """Test that greet endpoint rejects whitespace-only name"""
        response = client.post("/api/greet", json={"name": "   "})
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Name cannot be empty"
    
    def test_greet_trims_leading_trailing_whitespace(self):
        """Test that greet endpoint trims leading/trailing whitespace from name"""
        response = client.post("/api/greet", json={"name": "  Bob  "})
        assert response.status_code == 200
        data = response.json()
        assert data["greeting"] == "Hello, Bob! Welcome to our purple-themed app!"
    
    def test_greet_rejects_missing_name_field(self):
        """Test that greet endpoint rejects request without name field"""
        response = client.post("/api/greet", json={})
        # FastAPI validation returns 422 for missing required fields
        assert response.status_code == 422
    
    def test_greet_response_time(self):
        """Test that greet endpoint responds within 100ms"""
        import time
        start = time.time()
        response = client.post("/api/greet", json={"name": "Performance Test"})
        end = time.time()
        
        response_time_ms = (end - start) * 1000
        assert response.status_code == 200
        # Allow 200ms for test environment
        assert response_time_ms < 200, f"Response time {response_time_ms}ms exceeds 200ms"

class TestCORSHeaders:
    """Test suite for CORS configuration"""
    
    def test_cors_headers_present_on_hello_endpoint(self):
        """Test that CORS headers are present on /api/hello"""
        # CORS middleware requires Origin header to be present in request
        response = client.get(
            "/api/hello",
            headers={"Origin": "http://localhost:3000"}
        )
        assert "access-control-allow-origin" in response.headers
    
    def test_cors_allows_frontend_origin(self):
        """Test that CORS allows requests from frontend origin"""
        response = client.get(
            "/api/hello",
            headers={"Origin": "http://localhost:3000"}
        )
        assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"
    
    def test_cors_headers_present_on_health_endpoint(self):
        """Test that CORS headers are present on /health"""
        response = client.get(
            "/health",
            headers={"Origin": "http://localhost:3000"}
        )
        assert "access-control-allow-origin" in response.headers
    
    def test_cors_headers_present_on_greet_endpoint(self):
        """Test that CORS headers are present on POST /api/greet"""
        response = client.post(
            "/api/greet",
            json={"name": "Test"},
            headers={"Origin": "http://localhost:3000"}
        )
        assert "access-control-allow-origin" in response.headers
        assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"

class TestRootEndpoint:
    """Test suite for root endpoint"""
    
    def test_root_returns_200(self):
        """Test that root endpoint returns 200 status code"""
        response = client.get("/")
        assert response.status_code == 200
    
    def test_root_returns_api_info(self):
        """Test that root endpoint returns API information"""
        response = client.get("/")
        data = response.json()
        assert "name" in data
        assert "endpoints" in data
        assert isinstance(data["endpoints"], list)
    
    def test_root_includes_greet_endpoint(self):
        """Test that root endpoint includes /api/greet in endpoints list"""
        response = client.get("/")
        data = response.json()
        assert "/api/greet" in data["endpoints"]

class TestPerformance:
    """Test suite for performance requirements"""
    
    def test_hello_endpoint_response_time(self):
        """Test that /api/hello responds within 100ms"""
        import time
        start = time.time()
        response = client.get("/api/hello")
        end = time.time()
        
        response_time_ms = (end - start) * 1000
        assert response.status_code == 200
        # Allow 200ms for test environment (more lenient than production 100ms)
        assert response_time_ms < 200, f"Response time {response_time_ms}ms exceeds 200ms"
    
    def test_health_endpoint_response_time(self):
        """Test that /health responds within 100ms"""
        import time
        start = time.time()
        response = client.get("/health")
        end = time.time()
        
        response_time_ms = (end - start) * 1000
        assert response.status_code == 200
        # Allow 200ms for test environment
        assert response_time_ms < 200, f"Response time {response_time_ms}ms exceeds 200ms"

class TestBackwardCompatibility:
    """Test suite to ensure existing functionality is unchanged"""
    
    def test_hello_endpoint_unchanged(self):
        """Test that /api/hello endpoint response is unchanged"""
        response = client.get("/api/hello")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Hello World from Backend!"
        assert "timestamp" in data
    
    def test_health_endpoint_unchanged(self):
        """Test that /health endpoint response is unchanged"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
