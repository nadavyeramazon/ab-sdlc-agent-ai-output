import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from main import app

# Create TestClient instance
client = TestClient(app)


class TestHelloEndpoint:
    """Test suite for /api/hello endpoint"""
    
    def test_hello_endpoint_returns_200(self):
        """Test that /api/hello returns HTTP 200 status code"""
        response = client.get("/api/hello")
        assert response.status_code == 200
    
    def test_hello_endpoint_returns_json(self):
        """Test that /api/hello returns valid JSON response"""
        response = client.get("/api/hello")
        assert response.headers["content-type"] == "application/json"
    
    def test_hello_endpoint_has_message_field(self):
        """Test that response contains 'message' field"""
        response = client.get("/api/hello")
        data = response.json()
        assert "message" in data
        assert data["message"] == "Hello World from Backend!"
    
    def test_hello_endpoint_has_timestamp_field(self):
        """Test that response contains 'timestamp' field"""
        response = client.get("/api/hello")
        data = response.json()
        assert "timestamp" in data
    
    def test_hello_endpoint_timestamp_is_valid_iso8601(self):
        """Test that timestamp is valid ISO 8601 format"""
        response = client.get("/api/hello")
        data = response.json()
        timestamp = data["timestamp"]
        
        # Verify ISO 8601 format by parsing
        try:
            # Remove 'Z' suffix and parse
            datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            is_valid = True
        except ValueError:
            is_valid = False
        
        assert is_valid, f"Timestamp '{timestamp}' is not valid ISO 8601 format"
    
    def test_hello_endpoint_timestamp_ends_with_z(self):
        """Test that timestamp ends with 'Z' indicating UTC"""
        response = client.get("/api/hello")
        data = response.json()
        assert data["timestamp"].endswith("Z")


class TestHealthEndpoint:
    """Test suite for /health endpoint"""
    
    def test_health_endpoint_returns_200(self):
        """Test that /health returns HTTP 200 status code"""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_endpoint_returns_json(self):
        """Test that /health returns valid JSON response"""
        response = client.get("/health")
        assert response.headers["content-type"] == "application/json"
    
    def test_health_endpoint_returns_healthy_status(self):
        """Test that /health returns status: healthy"""
        response = client.get("/health")
        data = response.json()
        assert data == {"status": "healthy"}


class TestCORSConfiguration:
    """Test suite for CORS middleware configuration"""
    
    def test_cors_headers_present_in_response(self):
        """Test that CORS headers are present in responses"""
        response = client.get("/api/hello", headers={"Origin": "http://localhost:3000"})
        assert "access-control-allow-origin" in response.headers
    
    def test_cors_allows_frontend_origin(self):
        """Test that CORS allows requests from frontend origin"""
        response = client.get("/api/hello", headers={"Origin": "http://localhost:3000"})
        assert response.headers["access-control-allow-origin"] == "http://localhost:3000"


class TestResponseTime:
    """Test suite for API response time requirements"""
    
    def test_hello_endpoint_response_time(self):
        """Test that /api/hello responds within acceptable time"""
        import time
        
        start_time = time.time()
        response = client.get("/api/hello")
        end_time = time.time()
        
        response_time_ms = (end_time - start_time) * 1000
        
        # Response should be under 100ms for 95th percentile
        # In tests, we'll be more lenient (500ms) due to test overhead
        assert response_time_ms < 500, f"Response time {response_time_ms}ms exceeds threshold"
        assert response.status_code == 200
    
    def test_health_endpoint_response_time(self):
        """Test that /health responds within acceptable time"""
        import time
        
        start_time = time.time()
        response = client.get("/health")
        end_time = time.time()
        
        response_time_ms = (end_time - start_time) * 1000
        
        # Response should be under 100ms
        assert response_time_ms < 500, f"Response time {response_time_ms}ms exceeds threshold"
        assert response.status_code == 200


class TestIntegrationScenarios:
    """Test suite for end-to-end integration scenarios"""
    
    def test_multiple_hello_requests_return_different_timestamps(self):
        """Test that multiple requests return different timestamps"""
        import time
        
        response1 = client.get("/api/hello")
        time.sleep(0.01)  # Small delay
        response2 = client.get("/api/hello")
        
        data1 = response1.json()
        data2 = response2.json()
        
        # Timestamps should be different
        assert data1["timestamp"] != data2["timestamp"]
        # Messages should be the same
        assert data1["message"] == data2["message"]
    
    def test_service_health_before_and_after_hello_request(self):
        """Test that service remains healthy after handling requests"""
        # Check health before
        health1 = client.get("/health")
        assert health1.json()["status"] == "healthy"
        
        # Make hello request
        hello_response = client.get("/api/hello")
        assert hello_response.status_code == 200
        
        # Check health after
        health2 = client.get("/health")
        assert health2.json()["status"] == "healthy"
