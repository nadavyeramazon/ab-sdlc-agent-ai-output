"""
Comprehensive backend API tests using pytest and FastAPI TestClient.

Tests cover:
- All API endpoints (/api/hello, /health)
- Successful responses
- Error cases
- Response structure validation
- Status codes
- Edge cases
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from main import app


@pytest.fixture
def client():
    """
    Pytest fixture to create a TestClient instance for testing.
    
    Returns:
        TestClient: FastAPI test client
    """
    return TestClient(app)


class TestHelloEndpoint:
    """Test suite for /api/hello endpoint"""
    
    def test_hello_success(self, client):
        """Test successful response from /api/hello endpoint"""
        response = client.get("/api/hello")
        
        # Check status code
        assert response.status_code == 200
        
        # Check response structure
        data = response.json()
        assert "message" in data
        assert "timestamp" in data
        
        # Check message content
        assert data["message"] == "Hello World from Backend!"
        
        # Check timestamp format (ISO-8601 with Z suffix)
        assert data["timestamp"].endswith("Z")
        
        # Validate timestamp is parseable
        timestamp_str = data["timestamp"].rstrip("Z")
        try:
            datetime.fromisoformat(timestamp_str)
        except ValueError:
            pytest.fail("Timestamp is not in valid ISO-8601 format")
    
    def test_hello_response_types(self, client):
        """Test that response values are correct types"""
        response = client.get("/api/hello")
        data = response.json()
        
        assert isinstance(data["message"], str)
        assert isinstance(data["timestamp"], str)
    
    def test_hello_content_type(self, client):
        """Test that response has correct Content-Type header"""
        response = client.get("/api/hello")
        
        assert "application/json" in response.headers["content-type"]
    
    def test_hello_timestamp_recent(self, client):
        """Test that timestamp is recent (within last minute)"""
        response = client.get("/api/hello")
        data = response.json()
        
        # Parse the timestamp
        timestamp_str = data["timestamp"].rstrip("Z")
        response_time = datetime.fromisoformat(timestamp_str)
        current_time = datetime.utcnow()
        
        # Check timestamp is within reasonable range (1 minute)
        time_diff = abs((current_time - response_time).total_seconds())
        assert time_diff < 60, "Timestamp should be within the last minute"
    
    def test_hello_multiple_requests(self, client):
        """Test that multiple requests return consistent structure"""
        for _ in range(3):
            response = client.get("/api/hello")
            assert response.status_code == 200
            data = response.json()
            assert "message" in data
            assert "timestamp" in data
            assert data["message"] == "Hello World from Backend!"
    
    def test_hello_method_not_allowed(self, client):
        """Test that non-GET methods are not allowed"""
        # POST should not be allowed
        response = client.post("/api/hello")
        assert response.status_code == 405
        
        # PUT should not be allowed
        response = client.put("/api/hello")
        assert response.status_code == 405
        
        # DELETE should not be allowed
        response = client.delete("/api/hello")
        assert response.status_code == 405


class TestHealthEndpoint:
    """Test suite for /health endpoint"""
    
    def test_health_success(self, client):
        """Test successful response from /health endpoint"""
        response = client.get("/health")
        
        # Check status code
        assert response.status_code == 200
        
        # Check response structure
        data = response.json()
        assert "status" in data
        
        # Check status value
        assert data["status"] == "healthy"
    
    def test_health_response_types(self, client):
        """Test that response values are correct types"""
        response = client.get("/health")
        data = response.json()
        
        assert isinstance(data["status"], str)
    
    def test_health_content_type(self, client):
        """Test that response has correct Content-Type header"""
        response = client.get("/health")
        
        assert "application/json" in response.headers["content-type"]
    
    def test_health_response_minimal(self, client):
        """Test that health response only contains expected fields"""
        response = client.get("/health")
        data = response.json()
        
        # Should only have 'status' field
        assert len(data) == 1
        assert list(data.keys()) == ["status"]
    
    def test_health_idempotent(self, client):
        """Test that multiple health checks return the same result"""
        responses = [client.get("/health") for _ in range(5)]
        
        for response in responses:
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
    
    def test_health_method_not_allowed(self, client):
        """Test that non-GET methods are not allowed"""
        # POST should not be allowed
        response = client.post("/health")
        assert response.status_code == 405
        
        # PUT should not be allowed
        response = client.put("/health")
        assert response.status_code == 405
        
        # DELETE should not be allowed
        response = client.delete("/health")
        assert response.status_code == 405


class TestAPIErrors:
    """Test suite for error cases and edge cases"""
    
    def test_nonexistent_endpoint(self, client):
        """Test that nonexistent endpoints return 404"""
        response = client.get("/api/nonexistent")
        assert response.status_code == 404
    
    def test_root_endpoint(self, client):
        """Test that root endpoint behavior is defined"""
        response = client.get("/")
        # Should either return 404 or a valid response
        assert response.status_code in [200, 404]
    
    def test_api_prefix_without_endpoint(self, client):
        """Test that /api without endpoint returns 404"""
        response = client.get("/api")
        assert response.status_code == 404
        
        response = client.get("/api/")
        assert response.status_code == 404
    
    def test_case_sensitive_endpoints(self, client):
        """Test that endpoints are case-sensitive"""
        # Uppercase should not work
        response = client.get("/API/HELLO")
        assert response.status_code == 404
        
        response = client.get("/HEALTH")
        assert response.status_code == 404
    
    def test_trailing_slash_handling(self, client):
        """Test endpoint behavior with trailing slashes"""
        # Test /api/hello with trailing slash
        response = client.get("/api/hello/")
        # FastAPI typically redirects or returns 404
        assert response.status_code in [200, 307, 404]
        
        # Test /health with trailing slash
        response = client.get("/health/")
        assert response.status_code in [200, 307, 404]


class TestCORSConfiguration:
    """Test suite for CORS middleware configuration"""
    
    def test_cors_headers_present(self, client):
        """Test that CORS headers are present in responses"""
        response = client.get("/api/hello", headers={"Origin": "http://localhost:3000"})
        
        # Check for CORS headers
        assert "access-control-allow-origin" in response.headers
    
    def test_cors_allowed_origin(self, client):
        """Test that allowed origin is correctly configured"""
        response = client.get("/api/hello", headers={"Origin": "http://localhost:3000"})
        
        # Should allow localhost:3000
        assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"


class TestResponsePerformance:
    """Test suite for response timing and performance"""
    
    def test_hello_response_fast(self, client):
        """Test that /api/hello responds quickly"""
        import time
        
        start = time.time()
        response = client.get("/api/hello")
        duration = time.time() - start
        
        assert response.status_code == 200
        # Should respond within 1 second
        assert duration < 1.0, f"Response took {duration}s, should be under 1s"
    
    def test_health_response_fast(self, client):
        """Test that /health responds quickly"""
        import time
        
        start = time.time()
        response = client.get("/health")
        duration = time.time() - start
        
        assert response.status_code == 200
        # Should respond within 1 second
        assert duration < 1.0, f"Response took {duration}s, should be under 1s"


# Integration test
def test_all_endpoints_available(client):
    """
    Integration test to verify all documented endpoints are accessible
    """
    endpoints = [
        ("/api/hello", 200),
        ("/health", 200),
    ]
    
    for endpoint, expected_status in endpoints:
        response = client.get(endpoint)
        assert response.status_code == expected_status, \
            f"Endpoint {endpoint} returned {response.status_code}, expected {expected_status}"
