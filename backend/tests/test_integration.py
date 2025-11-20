"""Integration tests for complete request/response cycles."""

import pytest
from datetime import datetime
import json


class TestFullRequestResponseCycle:
    """Test complete request/response cycles."""
    
    @pytest.mark.integration
    def test_complete_hello_endpoint_flow(self, client):
        """Test complete flow for /api/hello endpoint."""
        # Make request
        response = client.get("/api/hello")
        
        # Verify status
        assert response.status_code == 200
        
        # Verify headers
        assert response.headers["content-type"] == "application/json"
        assert "content-length" in response.headers
        
        # Verify response body
        data = response.json()
        assert data["message"] == "Hello World from Backend!"
        assert "timestamp" in data
        
        # Verify timestamp is valid and recent
        timestamp = datetime.fromisoformat(data["timestamp"])
        assert isinstance(timestamp, datetime)
        
        # Verify timestamp is recent (within last 5 seconds)
        now = datetime.utcnow()
        time_diff = abs((now - timestamp).total_seconds())
        assert time_diff < 5, f"Timestamp is not recent: {time_diff} seconds old"
    
    @pytest.mark.integration
    def test_complete_health_endpoint_flow(self, client):
        """Test complete flow for /health endpoint."""
        # Make request
        response = client.get("/health")
        
        # Verify status
        assert response.status_code == 200
        
        # Verify headers
        assert response.headers["content-type"] == "application/json"
        
        # Verify response body
        data = response.json()
        assert data == {"status": "healthy"}
    
    @pytest.mark.integration
    def test_sequential_requests_to_both_endpoints(self, client):
        """Test sequential requests to different endpoints."""
        # Request 1: Health check
        response1 = client.get("/health")
        assert response1.status_code == 200
        assert response1.json()["status"] == "healthy"
        
        # Request 2: Hello endpoint
        response2 = client.get("/api/hello")
        assert response2.status_code == 200
        assert "message" in response2.json()
        
        # Request 3: Health check again
        response3 = client.get("/health")
        assert response3.status_code == 200
        assert response3.json()["status"] == "healthy"
        
        # Request 4: Hello endpoint again
        response4 = client.get("/api/hello")
        assert response4.status_code == 200
        assert "timestamp" in response4.json()
    
    @pytest.mark.integration
    def test_rapid_sequential_requests(self, client):
        """Test rapid sequential requests to same endpoint."""
        responses = []
        
        # Make 20 rapid requests
        for _ in range(20):
            response = client.get("/api/hello")
            responses.append(response)
        
        # All should succeed
        for response in responses:
            assert response.status_code == 200
            assert "message" in response.json()
            assert "timestamp" in response.json()
    
    @pytest.mark.integration
    def test_error_handling_for_invalid_endpoint(self, client):
        """Test error handling for non-existent endpoint."""
        response = client.get("/api/nonexistent")
        
        # Should return 404
        assert response.status_code == 404
        
        # Response should be JSON (FastAPI default error format)
        assert "application/json" in response.headers["content-type"]
        
        # Should have error detail
        data = response.json()
        assert "detail" in data
    
    @pytest.mark.integration
    def test_method_not_allowed_error_handling(self, client):
        """Test error handling for wrong HTTP method."""
        response = client.post("/api/hello")
        
        # Should return 405 Method Not Allowed
        assert response.status_code == 405
        
        # Response should be JSON
        assert "application/json" in response.headers["content-type"]
        
        # Should have error detail
        data = response.json()
        assert "detail" in data


class TestAPIDocumentation:
    """Test that API documentation endpoints are available."""
    
    @pytest.mark.integration
    def test_openapi_json_available(self, client):
        """Test that OpenAPI JSON schema is available."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        # Should be valid JSON
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert "paths" in data
    
    @pytest.mark.integration
    def test_docs_endpoint_available(self, client):
        """Test that Swagger UI docs endpoint is available."""
        response = client.get("/docs")
        assert response.status_code == 200
        
        # Should return HTML
        assert "text/html" in response.headers["content-type"]
    
    @pytest.mark.integration
    def test_redoc_endpoint_available(self, client):
        """Test that ReDoc endpoint is available."""
        response = client.get("/redoc")
        assert response.status_code == 200
        
        # Should return HTML
        assert "text/html" in response.headers["content-type"]
    
    @pytest.mark.integration
    def test_openapi_schema_includes_hello_endpoint(self, client):
        """Test that OpenAPI schema documents /api/hello endpoint."""
        response = client.get("/openapi.json")
        schema = response.json()
        
        # Check that /api/hello is documented
        assert "/api/hello" in schema["paths"]
        assert "get" in schema["paths"]["/api/hello"]
    
    @pytest.mark.integration
    def test_openapi_schema_includes_health_endpoint(self, client):
        """Test that OpenAPI schema documents /health endpoint."""
        response = client.get("/openapi.json")
        schema = response.json()
        
        # Check that /health is documented
        assert "/health" in schema["paths"]
        assert "get" in schema["paths"]["/health"]


class TestApplicationConfiguration:
    """Test application configuration and setup."""
    
    @pytest.mark.integration
    def test_application_title(self, test_app):
        """Test that application has correct title."""
        assert test_app.title == "Demo FastAPI Backend"
    
    @pytest.mark.integration
    def test_cors_middleware_configured(self, test_app):
        """Test that CORS middleware is properly configured."""
        # Check that CORS middleware is in the middleware stack
        middleware_classes = [m.cls.__name__ for m in test_app.user_middleware]
        assert "CORSMiddleware" in middleware_classes
    
    @pytest.mark.integration
    def test_application_has_routes(self, test_app):
        """Test that application has expected routes."""
        routes = [route.path for route in test_app.routes]
        
        # Should have our endpoints
        assert "/api/hello" in routes
        assert "/health" in routes
    
    @pytest.mark.integration
    def test_all_routes_have_get_method(self, test_app):
        """Test that all our custom routes support GET method."""
        for route in test_app.routes:
            if route.path in ["/api/hello", "/health"]:
                assert "GET" in route.methods


class TestResponseConsistency:
    """Test response consistency across multiple requests."""
    
    @pytest.mark.integration
    def test_health_response_is_consistent(self, client):
        """Test that /health returns identical responses."""
        responses = [client.get("/health") for _ in range(10)]
        
        # All responses should be identical
        first_response = responses[0].json()
        for response in responses[1:]:
            assert response.json() == first_response
    
    @pytest.mark.integration
    def test_hello_message_is_consistent(self, client):
        """Test that /api/hello message is consistent."""
        responses = [client.get("/api/hello") for _ in range(10)]
        
        # Message should be identical
        first_message = responses[0].json()["message"]
        for response in responses[1:]:
            assert response.json()["message"] == first_message
    
    @pytest.mark.integration
    def test_response_encoding_is_utf8(self, client):
        """Test that responses use UTF-8 encoding."""
        response = client.get("/api/hello")
        
        # Check encoding in content-type header
        content_type = response.headers["content-type"]
        # UTF-8 is typically default for application/json
        assert "application/json" in content_type
    
    @pytest.mark.integration
    def test_response_can_be_parsed_as_json(self, client):
        """Test that all endpoint responses can be parsed as JSON."""
        endpoints = ["/api/hello", "/health"]
        
        for endpoint in endpoints:
            response = client.get(endpoint)
            
            # Should successfully parse as JSON
            try:
                data = response.json()
                assert isinstance(data, dict)
            except json.JSONDecodeError:
                pytest.fail(f"Response from {endpoint} is not valid JSON")
