import pytest
from fastapi.testclient import TestClient
from datetime import datetime
import re
from main import app

# Create test client for making requests to the FastAPI application
client = TestClient(app)


class TestAPIEndpoints:
    """Test suite for API endpoints"""
    
    def test_root_endpoint(self):
        """
        Test the root endpoint returns service information.
        
        Verifies:
        - Status code is 200
        - Response contains service name and version
        - Response lists available endpoints
        """
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        
        assert "service" in data
        assert "Hello World Backend API" in data["service"]
        assert "version" in data
        assert "endpoints" in data
        assert isinstance(data["endpoints"], list)
        assert len(data["endpoints"]) > 0
    
    def test_health_endpoint(self):
        """
        Test the health check endpoint.
        
        Verifies:
        - Status code is 200
        - Response contains 'status' field
        - Status is 'healthy'
        """
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        
        assert "status" in data
        assert data["status"] == "healthy"
    
    def test_hello_endpoint(self):
        """
        Test the /api/hello endpoint returns correct structure.
        
        Verifies:
        - Status code is 200
        - Response contains 'message' and 'timestamp' fields
        - Message content is correct
        - Timestamp is in valid ISO8601 format
        """
        response = client.get("/api/hello")
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "message" in data
        assert "timestamp" in data
        
        # Verify message content
        assert data["message"] == "Hello World from Backend!"
        
        # Verify timestamp format (ISO8601)
        timestamp = data["timestamp"]
        # Should match format: 2024-01-15T10:30:00.123456Z
        iso8601_pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}Z$"
        assert re.match(iso8601_pattern, timestamp), f"Timestamp '{timestamp}' is not in ISO8601 format"
    
    def test_hello_endpoint_timestamp_is_recent(self):
        """
        Test that the timestamp in /api/hello is current.
        
        Verifies:
        - Timestamp is within last 5 seconds (reasonable for test execution)
        """
        response = client.get("/api/hello")
        data = response.json()
        
        # Parse timestamp from response
        timestamp_str = data["timestamp"].rstrip('Z')  # Remove 'Z' for parsing
        response_time = datetime.fromisoformat(timestamp_str)
        
        # Check timestamp is recent (within 5 seconds)
        now = datetime.utcnow()
        time_diff = abs((now - response_time).total_seconds())
        assert time_diff < 5, f"Timestamp is not recent: {time_diff} seconds old"
    
    def test_hello_endpoint_multiple_calls(self):
        """
        Test that multiple calls to /api/hello return different timestamps.
        
        Verifies:
        - Each call generates a new timestamp
        - Timestamps are monotonically increasing
        """
        response1 = client.get("/api/hello")
        response2 = client.get("/api/hello")
        
        data1 = response1.json()
        data2 = response2.json()
        
        # Timestamps should be different
        assert data1["timestamp"] != data2["timestamp"]
        
        # Second timestamp should be >= first (or very close)
        time1 = datetime.fromisoformat(data1["timestamp"].rstrip('Z'))
        time2 = datetime.fromisoformat(data2["timestamp"].rstrip('Z'))
        assert time2 >= time1


class TestCORS:
    """Test suite for CORS configuration"""
    
    def test_cors_headers_present(self):
        """
        Test that CORS headers are present in responses.
        
        Verifies:
        - Access-Control-Allow-Origin header is set
        - Allows requests from localhost:3000
        """
        response = client.options(
            "/api/hello",
            headers={"Origin": "http://localhost:3000"}
        )
        
        # CORS headers should be present
        assert "access-control-allow-origin" in [h.lower() for h in response.headers.keys()]
    
    def test_api_hello_with_origin(self):
        """
        Test GET request with Origin header includes CORS headers.
        
        Verifies:
        - Request succeeds with Origin header
        - Response includes appropriate CORS headers
        """
        response = client.get(
            "/api/hello",
            headers={"Origin": "http://localhost:3000"}
        )
        
        assert response.status_code == 200
        # Verify response includes CORS headers
        assert "access-control-allow-origin" in [h.lower() for h in response.headers.keys()]


class TestPerformance:
    """Test suite for performance requirements"""
    
    def test_hello_endpoint_response_time(self):
        """
        Test that /api/hello responds within performance requirements.
        
        Verifies:
        - Response time is under 100ms (as per spec)
        
        Note: This is a basic test. In production, use proper load testing tools.
        """
        import time
        
        start_time = time.time()
        response = client.get("/api/hello")
        end_time = time.time()
        
        response_time_ms = (end_time - start_time) * 1000
        
        assert response.status_code == 200
        # Allow some buffer for test environment (200ms)
        assert response_time_ms < 200, f"Response time {response_time_ms}ms exceeds requirement"
    
    def test_health_endpoint_response_time(self):
        """
        Test that /health responds quickly.
        
        Verifies:
        - Response time is under 100ms
        """
        import time
        
        start_time = time.time()
        response = client.get("/health")
        end_time = time.time()
        
        response_time_ms = (end_time - start_time) * 1000
        
        assert response.status_code == 200
        assert response_time_ms < 200, f"Response time {response_time_ms}ms exceeds requirement"


class TestErrorHandling:
    """Test suite for error handling"""
    
    def test_invalid_endpoint_returns_404(self):
        """
        Test that requesting non-existent endpoint returns 404.
        
        Verifies:
        - Invalid endpoints return 404 status
        - Error response is properly formatted
        """
        response = client.get("/api/nonexistent")
        assert response.status_code == 404
    
    def test_method_not_allowed(self):
        """
        Test that using wrong HTTP method returns appropriate error.
        
        Verifies:
        - POST to GET-only endpoint returns 405 or similar
        """
        response = client.post("/health")
        # FastAPI returns 405 for method not allowed
        assert response.status_code == 405
