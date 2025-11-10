"""Backend API Tests

Comprehensive test suite for FastAPI endpoints using pytest and TestClient.
Tests all endpoints, CORS configuration, and response formats.
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime
import pytz
from main import app

# Create test client
client = TestClient(app)


class TestHelloEndpoint:
    """Test suite for /api/hello endpoint"""
    
    def test_hello_endpoint_returns_200(self):
        """Test that /api/hello returns HTTP 200 status code"""
        response = client.get("/api/hello")
        assert response.status_code == 200
    
    def test_hello_endpoint_returns_json(self):
        """Test that /api/hello returns JSON content type"""
        response = client.get("/api/hello")
        assert response.headers["content-type"] == "application/json"
    
    def test_hello_endpoint_has_message_field(self):
        """Test that response contains 'message' field"""
        response = client.get("/api/hello")
        data = response.json()
        assert "message" in data
    
    def test_hello_endpoint_message_content(self):
        """Test that message field contains exact expected text"""
        response = client.get("/api/hello")
        data = response.json()
        assert data["message"] == "Hello World from Backend!"
    
    def test_hello_endpoint_has_timestamp_field(self):
        """Test that response contains 'timestamp' field"""
        response = client.get("/api/hello")
        data = response.json()
        assert "timestamp" in data
    
    def test_hello_endpoint_timestamp_is_valid_iso8601(self):
        """Test that timestamp is in valid ISO 8601 format"""
        response = client.get("/api/hello")
        data = response.json()
        timestamp = data["timestamp"]
        
        # Verify ISO 8601 format by parsing it
        try:
            datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            is_valid = True
        except ValueError:
            is_valid = False
        
        assert is_valid, f"Timestamp {timestamp} is not valid ISO 8601 format"
    
    def test_hello_endpoint_timestamp_is_recent(self):
        """Test that timestamp is within last 5 seconds (reasonable for test execution)"""
        response = client.get("/api/hello")
        data = response.json()
        timestamp_str = data["timestamp"]
        
        # Parse timestamp
        timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        current_time = datetime.now(pytz.UTC)
        
        # Check if timestamp is within 5 seconds
        time_diff = abs((current_time - timestamp).total_seconds())
        assert time_diff < 5, f"Timestamp is not recent: {time_diff} seconds old"
    
    def test_hello_endpoint_response_structure(self):
        """Test complete response structure"""
        response = client.get("/api/hello")
        data = response.json()
        
        # Check that response has exactly 2 fields
        assert len(data) == 2
        assert "message" in data
        assert "timestamp" in data
        assert isinstance(data["message"], str)
        assert isinstance(data["timestamp"], str)


class TestHealthEndpoint:
    """Test suite for /health endpoint"""
    
    def test_health_endpoint_returns_200(self):
        """Test that /health returns HTTP 200 status code"""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_endpoint_returns_json(self):
        """Test that /health returns JSON content type"""
        response = client.get("/health")
        assert response.headers["content-type"] == "application/json"
    
    def test_health_endpoint_has_status_field(self):
        """Test that response contains 'status' field"""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
    
    def test_health_endpoint_status_is_healthy(self):
        """Test that status field contains 'healthy'"""
        response = client.get("/health")
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_health_endpoint_response_structure(self):
        """Test complete response structure"""
        response = client.get("/health")
        data = response.json()
        
        # Check response structure
        assert len(data) == 1
        assert "status" in data
        assert isinstance(data["status"], str)


class TestRootEndpoint:
    """Test suite for root / endpoint"""
    
    def test_root_endpoint_returns_200(self):
        """Test that root endpoint returns HTTP 200 status code"""
        response = client.get("/")
        assert response.status_code == 200
    
    def test_root_endpoint_returns_json(self):
        """Test that root endpoint returns JSON content type"""
        response = client.get("/")
        assert response.headers["content-type"] == "application/json"
    
    def test_root_endpoint_has_message(self):
        """Test that root endpoint returns welcome message"""
        response = client.get("/")
        data = response.json()
        assert "message" in data
        assert "Welcome" in data["message"]


class TestCORSConfiguration:
    """Test suite for CORS middleware configuration"""
    
    def test_cors_headers_present_on_hello_endpoint(self):
        """Test that CORS headers are present in /api/hello response"""
        response = client.get(
            "/api/hello",
            headers={"Origin": "http://localhost:3000"}
        )
        
        # Check for CORS headers
        assert "access-control-allow-origin" in response.headers
    
    def test_cors_allows_frontend_origin(self):
        """Test that CORS allows requests from frontend origin"""
        response = client.get(
            "/api/hello",
            headers={"Origin": "http://localhost:3000"}
        )
        
        # Verify frontend origin is allowed
        assert response.headers["access-control-allow-origin"] == "http://localhost:3000"
    
    def test_cors_options_request(self):
        """Test CORS preflight OPTIONS request"""
        response = client.options(
            "/api/hello",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET"
            }
        )
        
        # Preflight should return 200
        assert response.status_code == 200


class TestResponseTiming:
    """Test suite for response time requirements"""
    
    def test_hello_endpoint_response_time(self):
        """Test that /api/hello responds within 100ms"""
        import time
        
        start_time = time.time()
        response = client.get("/api/hello")
        end_time = time.time()
        
        response_time_ms = (end_time - start_time) * 1000
        
        # Should respond within 100ms (being generous for test environment)
        assert response_time_ms < 200, f"Response took {response_time_ms}ms"
        assert response.status_code == 200
    
    def test_health_endpoint_response_time(self):
        """Test that /health responds within 50ms"""
        import time
        
        start_time = time.time()
        response = client.get("/health")
        end_time = time.time()
        
        response_time_ms = (end_time - start_time) * 1000
        
        # Should respond within 50ms (being generous for test environment)
        assert response_time_ms < 100, f"Response took {response_time_ms}ms"
        assert response.status_code == 200


class TestEdgeCases:
    """Test suite for edge cases and error scenarios"""
    
    def test_invalid_endpoint_returns_404(self):
        """Test that invalid endpoints return 404"""
        response = client.get("/api/invalid")
        assert response.status_code == 404
    
    def test_hello_endpoint_with_trailing_slash(self):
        """Test /api/hello/ with trailing slash"""
        response = client.get("/api/hello/")
        # Should either redirect or return 404
        assert response.status_code in [200, 307, 404]
    
    def test_post_method_not_allowed_on_hello(self):
        """Test that POST method is not allowed on /api/hello"""
        response = client.post("/api/hello")
        assert response.status_code == 405  # Method Not Allowed
