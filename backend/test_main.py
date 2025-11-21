"""
Comprehensive backend tests for FastAPI application.

This test suite covers:
- /api/hello endpoint (GET)
- /health endpoint (GET)
- Response validation
- Status codes
- JSON structure
- Edge cases and error scenarios
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from main import app


# Test client fixture
@pytest.fixture
def client():
    """
    Create a TestClient instance for testing FastAPI endpoints.
    This fixture is reused across all tests.
    """
    return TestClient(app)


class TestHelloEndpoint:
    """Test suite for /api/hello endpoint"""

    def test_hello_endpoint_success(self, client):
        """Test successful response from /api/hello endpoint"""
        response = client.get("/api/hello")
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"

    def test_hello_endpoint_status_code(self, client):
        """Test that /api/hello returns 200 status code"""
        response = client.get("/api/hello")
        
        assert response.status_code == 200

    def test_hello_endpoint_json_structure(self, client):
        """Test that /api/hello returns correct JSON structure"""
        response = client.get("/api/hello")
        data = response.json()
        
        # Verify required keys are present
        assert "message" in data
        assert "timestamp" in data
        
        # Verify correct number of keys
        assert len(data) == 2

    def test_hello_endpoint_message_content(self, client):
        """Test that /api/hello returns expected message content"""
        response = client.get("/api/hello")
        data = response.json()
        
        assert data["message"] == "Hello World from Backend!"
        assert isinstance(data["message"], str)

    def test_hello_endpoint_timestamp_format(self, client):
        """Test that /api/hello returns timestamp in ISO-8601 format"""
        response = client.get("/api/hello")
        data = response.json()
        
        # Verify timestamp is a string
        assert isinstance(data["timestamp"], str)
        
        # Verify timestamp ends with 'Z' (UTC indicator)
        assert data["timestamp"].endswith("Z")
        
        # Verify timestamp can be parsed as ISO format
        timestamp_str = data["timestamp"].rstrip("Z")
        try:
            parsed_time = datetime.fromisoformat(timestamp_str)
            assert parsed_time is not None
        except ValueError:
            pytest.fail("Timestamp is not in valid ISO-8601 format")

    def test_hello_endpoint_timestamp_is_recent(self, client):
        """Test that /api/hello returns a recent timestamp (within last minute)"""
        response = client.get("/api/hello")
        data = response.json()
        
        # Parse the timestamp
        timestamp_str = data["timestamp"].rstrip("Z")
        endpoint_time = datetime.fromisoformat(timestamp_str)
        current_time = datetime.utcnow()
        
        # Check that timestamp is within last 60 seconds
        time_difference = (current_time - endpoint_time).total_seconds()
        assert time_difference >= 0, "Timestamp is in the future"
        assert time_difference < 60, "Timestamp is too old (more than 60 seconds)"

    def test_hello_endpoint_multiple_calls(self, client):
        """Test that multiple calls to /api/hello return consistent structure"""
        for _ in range(3):
            response = client.get("/api/hello")
            data = response.json()
            
            assert response.status_code == 200
            assert "message" in data
            assert "timestamp" in data
            assert data["message"] == "Hello World from Backend!"

    def test_hello_endpoint_with_trailing_slash(self, client):
        """Test /api/hello endpoint with trailing slash (should fail as not defined)"""
        response = client.get("/api/hello/")
        
        # FastAPI by default doesn't redirect, so this should return 404
        assert response.status_code == 404

    def test_hello_endpoint_case_sensitivity(self, client):
        """Test that endpoint is case-sensitive"""
        response = client.get("/api/HELLO")
        
        # Should return 404 as endpoint is case-sensitive
        assert response.status_code == 404

    def test_hello_endpoint_wrong_method_post(self, client):
        """Test that POST method is not allowed on /api/hello"""
        response = client.post("/api/hello")
        
        # Should return 405 Method Not Allowed
        assert response.status_code == 405

    def test_hello_endpoint_wrong_method_put(self, client):
        """Test that PUT method is not allowed on /api/hello"""
        response = client.put("/api/hello")
        
        # Should return 405 Method Not Allowed
        assert response.status_code == 405

    def test_hello_endpoint_wrong_method_delete(self, client):
        """Test that DELETE method is not allowed on /api/hello"""
        response = client.delete("/api/hello")
        
        # Should return 405 Method Not Allowed
        assert response.status_code == 405


class TestHealthEndpoint:
    """Test suite for /health endpoint"""

    def test_health_endpoint_success(self, client):
        """Test successful response from /health endpoint"""
        response = client.get("/health")
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"

    def test_health_endpoint_status_code(self, client):
        """Test that /health returns 200 status code"""
        response = client.get("/health")
        
        assert response.status_code == 200

    def test_health_endpoint_json_structure(self, client):
        """Test that /health returns correct JSON structure"""
        response = client.get("/health")
        data = response.json()
        
        # Verify required key is present
        assert "status" in data
        
        # Verify it only contains the status key
        assert len(data) == 1

    def test_health_endpoint_status_value(self, client):
        """Test that /health returns 'healthy' status"""
        response = client.get("/health")
        data = response.json()
        
        assert data["status"] == "healthy"
        assert isinstance(data["status"], str)

    def test_health_endpoint_multiple_calls(self, client):
        """Test that multiple calls to /health are consistent"""
        for _ in range(5):
            response = client.get("/health")
            data = response.json()
            
            assert response.status_code == 200
            assert data["status"] == "healthy"

    def test_health_endpoint_with_trailing_slash(self, client):
        """Test /health endpoint with trailing slash (should fail as not defined)"""
        response = client.get("/health/")
        
        # FastAPI by default doesn't redirect, so this should return 404
        assert response.status_code == 404

    def test_health_endpoint_wrong_method_post(self, client):
        """Test that POST method is not allowed on /health"""
        response = client.post("/health")
        
        # Should return 405 Method Not Allowed
        assert response.status_code == 405

    def test_health_endpoint_wrong_method_put(self, client):
        """Test that PUT method is not allowed on /health"""
        response = client.put("/health")
        
        # Should return 405 Method Not Allowed
        assert response.status_code == 405

    def test_health_endpoint_wrong_method_delete(self, client):
        """Test that DELETE method is not allowed on /health"""
        response = client.delete("/health")
        
        # Should return 405 Method Not Allowed
        assert response.status_code == 405

    def test_health_endpoint_case_sensitivity(self, client):
        """Test that endpoint is case-sensitive"""
        response = client.get("/HEALTH")
        
        # Should return 404 as endpoint is case-sensitive
        assert response.status_code == 404


class TestCORSConfiguration:
    """Test suite for CORS middleware configuration"""

    def test_cors_headers_present(self, client):
        """Test that CORS headers are present in responses"""
        response = client.get("/api/hello", headers={"Origin": "http://localhost:3000"})
        
        # CORS headers should be present
        assert "access-control-allow-origin" in response.headers

    def test_cors_allows_frontend_origin(self, client):
        """Test that CORS allows requests from frontend origin"""
        response = client.get(
            "/api/hello",
            headers={"Origin": "http://localhost:3000"}
        )
        
        assert response.status_code == 200
        assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"


class TestApplicationRoutes:
    """Test suite for general application routing"""

    def test_nonexistent_route_returns_404(self, client):
        """Test that accessing non-existent route returns 404"""
        response = client.get("/nonexistent")
        
        assert response.status_code == 404

    def test_root_path_returns_404(self, client):
        """Test that root path returns 404 (no root endpoint defined)"""
        response = client.get("/")
        
        assert response.status_code == 404

    def test_api_prefix_without_endpoint(self, client):
        """Test that /api without endpoint returns 404"""
        response = client.get("/api")
        
        assert response.status_code == 404

    def test_api_prefix_with_trailing_slash(self, client):
        """Test that /api/ without endpoint returns 404"""
        response = client.get("/api/")
        
        assert response.status_code == 404


class TestResponseHeaders:
    """Test suite for HTTP response headers"""

    def test_hello_endpoint_content_type(self, client):
        """Test that /api/hello returns correct content-type header"""
        response = client.get("/api/hello")
        
        assert response.headers["content-type"] == "application/json"

    def test_health_endpoint_content_type(self, client):
        """Test that /health returns correct content-type header"""
        response = client.get("/health")
        
        assert response.headers["content-type"] == "application/json"


class TestEdgeCases:
    """Test suite for edge cases and boundary conditions"""

    def test_hello_endpoint_with_query_params(self, client):
        """Test /api/hello with query parameters (should be ignored)"""
        response = client.get("/api/hello?param=value")
        
        # Should still work normally, query params ignored
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Hello World from Backend!"

    def test_health_endpoint_with_query_params(self, client):
        """Test /health with query parameters (should be ignored)"""
        response = client.get("/health?test=true")
        
        # Should still work normally, query params ignored
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    def test_concurrent_requests_to_hello(self, client):
        """Test multiple concurrent requests to /api/hello"""
        responses = []
        
        # Make 10 concurrent-like requests
        for _ in range(10):
            response = client.get("/api/hello")
            responses.append(response)
        
        # All should succeed
        for response in responses:
            assert response.status_code == 200
            data = response.json()
            assert "message" in data
            assert "timestamp" in data

    def test_concurrent_requests_to_health(self, client):
        """Test multiple concurrent requests to /health"""
        responses = []
        
        # Make 10 concurrent-like requests
        for _ in range(10):
            response = client.get("/health")
            responses.append(response)
        
        # All should succeed
        for response in responses:
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
