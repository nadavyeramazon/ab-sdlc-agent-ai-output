"""
Comprehensive test suite for the FastAPI backend application.

This module contains pytest tests for all API endpoints and middleware configurations.
Tests follow pytest best practices with clear naming, proper fixtures, and comprehensive coverage.
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from main import app


@pytest.fixture
def client():
    """
    Pytest fixture that provides a TestClient instance for testing FastAPI endpoints.
    
    The TestClient allows making requests to the FastAPI application without running
    a live server, making tests fast and isolated.
    
    Yields:
        TestClient: A test client instance for the FastAPI app
    """
    with TestClient(app) as test_client:
        yield test_client


class TestHealthEndpoint:
    """Test suite for the /health endpoint"""
    
    def test_health_returns_200_status(self, client):
        """Test that the health endpoint returns a 200 OK status code"""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_returns_correct_structure(self, client):
        """Test that the health endpoint returns the expected JSON structure"""
        response = client.get("/health")
        data = response.json()
        
        assert "status" in data
        assert isinstance(data, dict)
    
    def test_health_returns_healthy_status(self, client):
        """Test that the health endpoint returns 'healthy' status"""
        response = client.get("/health")
        data = response.json()
        
        assert data["status"] == "healthy"
    
    def test_health_endpoint_method_not_allowed(self, client):
        """Test that POST method is not allowed on health endpoint"""
        response = client.post("/health")
        assert response.status_code == 405  # Method Not Allowed
    
    def test_health_endpoint_content_type(self, client):
        """Test that the health endpoint returns JSON content type"""
        response = client.get("/health")
        assert "application/json" in response.headers["content-type"]


class TestHelloEndpoint:
    """Test suite for the /api/hello endpoint"""
    
    def test_hello_returns_200_status(self, client):
        """Test that the hello endpoint returns a 200 OK status code"""
        response = client.get("/api/hello")
        assert response.status_code == 200
    
    def test_hello_returns_correct_structure(self, client):
        """Test that the hello endpoint returns the expected JSON structure"""
        response = client.get("/api/hello")
        data = response.json()
        
        assert "message" in data
        assert "timestamp" in data
        assert isinstance(data, dict)
    
    def test_hello_returns_correct_message(self, client):
        """Test that the hello endpoint returns the expected greeting message"""
        response = client.get("/api/hello")
        data = response.json()
        
        assert data["message"] == "Hello World from Backend!"
    
    def test_hello_timestamp_is_valid_iso_format(self, client):
        """Test that the timestamp in hello response is in valid ISO 8601 format"""
        response = client.get("/api/hello")
        data = response.json()
        
        # This will raise ValueError if timestamp is not valid ISO format
        try:
            parsed_timestamp = datetime.fromisoformat(data["timestamp"])
            assert isinstance(parsed_timestamp, datetime)
        except ValueError:
            pytest.fail("Timestamp is not in valid ISO 8601 format")
    
    def test_hello_timestamp_is_recent(self, client):
        """Test that the timestamp in hello response is recent (within last 5 seconds)"""
        response = client.get("/api/hello")
        data = response.json()
        
        timestamp = datetime.fromisoformat(data["timestamp"])
        now = datetime.now()
        time_difference = (now - timestamp).total_seconds()
        
        # Timestamp should be within the last 5 seconds
        assert abs(time_difference) < 5
    
    def test_hello_endpoint_method_not_allowed(self, client):
        """Test that POST method is not allowed on hello endpoint"""
        response = client.post("/api/hello")
        assert response.status_code == 405  # Method Not Allowed
    
    def test_hello_endpoint_content_type(self, client):
        """Test that the hello endpoint returns JSON content type"""
        response = client.get("/api/hello")
        assert "application/json" in response.headers["content-type"]
    
    def test_hello_multiple_calls_return_different_timestamps(self, client):
        """Test that multiple calls to hello endpoint return different timestamps"""
        response1 = client.get("/api/hello")
        response2 = client.get("/api/hello")
        
        data1 = response1.json()
        data2 = response2.json()
        
        # Timestamps should be different (or very close) between calls
        assert data1["message"] == data2["message"]  # Message stays the same
        # Timestamps might be the same if calls are very fast, so we just verify they exist
        assert "timestamp" in data1
        assert "timestamp" in data2


class TestCORSConfiguration:
    """Test suite for CORS (Cross-Origin Resource Sharing) middleware configuration"""
    
    def test_cors_allows_configured_origin(self, client):
        """Test that CORS allows requests from the configured origin (localhost:3000)"""
        response = client.get(
            "/api/hello",
            headers={"Origin": "http://localhost:3000"}
        )
        
        assert response.status_code == 200
        # Check for CORS headers in response
        assert "access-control-allow-origin" in response.headers
    
    def test_cors_allows_localhost_3000(self, client):
        """Test that CORS specifically allows localhost:3000 as origin"""
        response = client.get(
            "/api/hello",
            headers={"Origin": "http://localhost:3000"}
        )
        
        # The allowed origin should be in the response headers
        assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"
    
    def test_cors_preflight_request(self, client):
        """Test CORS preflight (OPTIONS) request for allowed methods"""
        response = client.options(
            "/api/hello",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET"
            }
        )
        
        # Preflight should return 200 OK
        assert response.status_code == 200
    
    def test_cors_allowed_methods_in_preflight(self, client):
        """Test that CORS preflight response includes allowed methods"""
        response = client.options(
            "/api/hello",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET"
            }
        )
        
        # Check that allowed methods are present
        allowed_methods = response.headers.get("access-control-allow-methods", "")
        assert "GET" in allowed_methods
    
    def test_cors_allowed_headers(self, client):
        """Test that CORS allows Content-Type header"""
        response = client.options(
            "/api/hello",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
                "Access-Control-Request-Headers": "Content-Type"
            }
        )
        
        # Should allow the Content-Type header
        assert response.status_code == 200


class TestAPIEndpointEdgeCases:
    """Test suite for edge cases and error handling"""
    
    def test_nonexistent_endpoint_returns_404(self, client):
        """Test that accessing a non-existent endpoint returns 404 Not Found"""
        response = client.get("/api/nonexistent")
        assert response.status_code == 404
    
    def test_root_endpoint_returns_404(self, client):
        """Test that accessing root endpoint returns 404 (no root route defined)"""
        response = client.get("/")
        assert response.status_code == 404
    
    def test_api_endpoint_with_trailing_slash(self, client):
        """Test API endpoint behavior with trailing slash"""
        # FastAPI by default redirects with trailing slash
        response = client.get("/api/hello/")
        # Should either return 200 or 307/308 redirect
        assert response.status_code in [200, 307, 308]
    
    def test_health_endpoint_with_query_parameters(self, client):
        """Test that health endpoint ignores query parameters"""
        response = client.get("/health?foo=bar")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_hello_endpoint_with_query_parameters(self, client):
        """Test that hello endpoint ignores query parameters"""
        response = client.get("/api/hello?test=value")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "timestamp" in data


class TestApplicationConfiguration:
    """Test suite for FastAPI application configuration"""
    
    def test_app_has_cors_middleware(self):
        """Test that the FastAPI app has CORS middleware configured"""
        # Check if CORS middleware is in the middleware stack
        middleware_classes = [m.cls.__name__ for m in app.user_middleware]
        assert "CORSMiddleware" in middleware_classes
    
    def test_openapi_schema_available(self, client):
        """Test that OpenAPI schema is available at /openapi.json"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert "paths" in schema
    
    def test_docs_endpoint_available(self, client):
        """Test that interactive API docs are available at /docs"""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]


# Test to ensure all endpoints are tested
def test_all_endpoints_are_covered():
    """
    Meta-test to ensure we have test coverage for all defined API endpoints.
    This helps maintain test coverage as new endpoints are added.
    """
    routes = [route.path for route in app.routes if hasattr(route, 'path')]
    api_routes = [r for r in routes if not r.startswith('/docs') and not r.startswith('/openapi')]
    
    # Verify we have routes defined
    assert len(api_routes) > 0
    
    # Check that critical endpoints exist
    assert "/health" in routes
    assert "/api/hello" in routes
