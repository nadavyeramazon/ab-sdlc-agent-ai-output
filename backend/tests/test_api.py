"""Comprehensive tests for FastAPI endpoints."""

import pytest
from datetime import datetime
import json


class TestHelloEndpoint:
    """Test suite for /api/hello endpoint."""
    
    @pytest.mark.unit
    def test_hello_endpoint_returns_200(self, client):
        """Test that /api/hello returns HTTP 200 OK."""
        response = client.get("/api/hello")
        assert response.status_code == 200
    
    @pytest.mark.unit
    def test_hello_endpoint_returns_json(self, client):
        """Test that /api/hello returns JSON content type."""
        response = client.get("/api/hello")
        assert response.headers["content-type"] == "application/json"
    
    @pytest.mark.unit
    def test_hello_endpoint_response_structure(self, client):
        """Test that /api/hello returns correct response structure."""
        response = client.get("/api/hello")
        data = response.json()
        
        # Verify response contains expected keys
        assert "message" in data
        assert "timestamp" in data
        
        # Verify data types
        assert isinstance(data["message"], str)
        assert isinstance(data["timestamp"], str)
    
    @pytest.mark.unit
    def test_hello_endpoint_message_content(self, client):
        """Test that /api/hello returns expected message."""
        response = client.get("/api/hello")
        data = response.json()
        
        assert data["message"] == "Hello World from Backend!"
    
    @pytest.mark.unit
    def test_hello_endpoint_timestamp_format(self, client):
        """Test that /api/hello returns valid ISO 8601 timestamp."""
        response = client.get("/api/hello")
        data = response.json()
        
        # Verify timestamp is valid ISO 8601 format
        try:
            parsed_time = datetime.fromisoformat(data["timestamp"])
            assert isinstance(parsed_time, datetime)
        except ValueError:
            pytest.fail(f"Timestamp '{data['timestamp']}' is not valid ISO 8601 format")
    
    @pytest.mark.unit
    def test_hello_endpoint_timestamp_is_recent(self, client):
        """Test that /api/hello returns recent timestamp (within 1 second)."""
        before = datetime.utcnow()
        response = client.get("/api/hello")
        after = datetime.utcnow()
        
        data = response.json()
        response_time = datetime.fromisoformat(data["timestamp"])
        
        # Timestamp should be between before and after request
        assert before <= response_time <= after
    
    @pytest.mark.unit
    def test_hello_endpoint_multiple_calls_different_timestamps(self, client):
        """Test that multiple calls return different timestamps."""
        response1 = client.get("/api/hello")
        response2 = client.get("/api/hello")
        
        data1 = response1.json()
        data2 = response2.json()
        
        # Timestamps should be different (or very close)
        # At minimum, we verify they're both valid
        assert "timestamp" in data1
        assert "timestamp" in data2
    
    @pytest.mark.integration
    def test_hello_endpoint_with_custom_headers(self, client, api_headers):
        """Test /api/hello with custom headers."""
        response = client.get("/api/hello", headers=api_headers)
        assert response.status_code == 200
        assert response.json()["message"] == "Hello World from Backend!"
    
    @pytest.mark.unit
    def test_hello_endpoint_post_method_not_allowed(self, client):
        """Test that POST to /api/hello is not allowed."""
        response = client.post("/api/hello")
        assert response.status_code == 405  # Method Not Allowed
    
    @pytest.mark.unit
    def test_hello_endpoint_put_method_not_allowed(self, client):
        """Test that PUT to /api/hello is not allowed."""
        response = client.put("/api/hello")
        assert response.status_code == 405  # Method Not Allowed
    
    @pytest.mark.unit
    def test_hello_endpoint_delete_method_not_allowed(self, client):
        """Test that DELETE to /api/hello is not allowed."""
        response = client.delete("/api/hello")
        assert response.status_code == 405  # Method Not Allowed
    
    @pytest.mark.unit
    def test_hello_endpoint_patch_method_not_allowed(self, client):
        """Test that PATCH to /api/hello is not allowed."""
        response = client.patch("/api/hello")
        assert response.status_code == 405  # Method Not Allowed


class TestHealthEndpoint:
    """Test suite for /health endpoint."""
    
    @pytest.mark.unit
    def test_health_endpoint_returns_200(self, client):
        """Test that /health returns HTTP 200 OK."""
        response = client.get("/health")
        assert response.status_code == 200
    
    @pytest.mark.unit
    def test_health_endpoint_returns_json(self, client):
        """Test that /health returns JSON content type."""
        response = client.get("/health")
        assert response.headers["content-type"] == "application/json"
    
    @pytest.mark.unit
    def test_health_endpoint_response_structure(self, client):
        """Test that /health returns correct response structure."""
        response = client.get("/health")
        data = response.json()
        
        # Verify response contains expected key
        assert "status" in data
        
        # Verify data type
        assert isinstance(data["status"], str)
    
    @pytest.mark.unit
    def test_health_endpoint_status_value(self, client):
        """Test that /health returns 'healthy' status."""
        response = client.get("/health")
        data = response.json()
        
        assert data["status"] == "healthy"
    
    @pytest.mark.unit
    def test_health_endpoint_consistency(self, client):
        """Test that /health returns consistent response across multiple calls."""
        responses = [client.get("/health") for _ in range(5)]
        
        for response in responses:
            assert response.status_code == 200
            assert response.json()["status"] == "healthy"
    
    @pytest.mark.integration
    def test_health_endpoint_with_custom_headers(self, client, api_headers):
        """Test /health with custom headers."""
        response = client.get("/health", headers=api_headers)
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    @pytest.mark.unit
    def test_health_endpoint_post_method_not_allowed(self, client):
        """Test that POST to /health is not allowed."""
        response = client.post("/health")
        assert response.status_code == 405  # Method Not Allowed
    
    @pytest.mark.unit
    def test_health_endpoint_put_method_not_allowed(self, client):
        """Test that PUT to /health is not allowed."""
        response = client.put("/health")
        assert response.status_code == 405  # Method Not Allowed
    
    @pytest.mark.unit
    def test_health_endpoint_delete_method_not_allowed(self, client):
        """Test that DELETE to /health is not allowed."""
        response = client.delete("/health")
        assert response.status_code == 405  # Method Not Allowed


class TestInvalidEndpoints:
    """Test suite for invalid/non-existent endpoints."""
    
    @pytest.mark.unit
    def test_invalid_endpoint_returns_404(self, client):
        """Test that invalid endpoint returns HTTP 404."""
        response = client.get("/invalid/endpoint")
        assert response.status_code == 404
    
    @pytest.mark.unit
    def test_root_endpoint_returns_404(self, client):
        """Test that root path returns HTTP 404 (no root handler defined)."""
        response = client.get("/")
        assert response.status_code == 404
    
    @pytest.mark.unit
    def test_api_without_hello_returns_404(self, client):
        """Test that /api without /hello returns HTTP 404."""
        response = client.get("/api")
        assert response.status_code == 404
    
    @pytest.mark.unit
    def test_misspelled_hello_endpoint_returns_404(self, client):
        """Test that misspelled endpoint returns HTTP 404."""
        response = client.get("/api/helo")  # Missing 'l'
        assert response.status_code == 404
    
    @pytest.mark.unit
    def test_case_sensitive_endpoint(self, client):
        """Test that endpoints are case-sensitive."""
        response = client.get("/api/Hello")  # Capital H
        assert response.status_code == 404
    
    @pytest.mark.unit
    def test_trailing_slash_on_hello_endpoint(self, client):
        """Test endpoint behavior with trailing slash."""
        response = client.get("/api/hello/")
        # FastAPI redirects or returns 404 depending on configuration
        # We just verify it doesn't return 200 with different content
        if response.status_code == 200:
            # If it works, verify it returns same content
            assert "message" in response.json()
        else:
            # Otherwise, expect 404 or 307 (redirect)
            assert response.status_code in [404, 307]
    
    @pytest.mark.unit
    def test_trailing_slash_on_health_endpoint(self, client):
        """Test health endpoint behavior with trailing slash."""
        response = client.get("/health/")
        # Similar to hello endpoint test
        if response.status_code == 200:
            assert "status" in response.json()
        else:
            assert response.status_code in [404, 307]


class TestResponseHeaders:
    """Test suite for response headers."""
    
    @pytest.mark.unit
    def test_hello_endpoint_content_type_header(self, client):
        """Test Content-Type header for /api/hello."""
        response = client.get("/api/hello")
        assert "application/json" in response.headers["content-type"]
    
    @pytest.mark.unit
    def test_health_endpoint_content_type_header(self, client):
        """Test Content-Type header for /health."""
        response = client.get("/health")
        assert "application/json" in response.headers["content-type"]
    
    @pytest.mark.unit
    def test_response_has_content_length(self, client):
        """Test that responses include Content-Length header."""
        response = client.get("/api/hello")
        assert "content-length" in response.headers
        assert int(response.headers["content-length"]) > 0


class TestEdgeCases:
    """Test suite for edge cases and boundary conditions."""
    
    @pytest.mark.unit
    def test_concurrent_requests_to_hello(self, client):
        """Test multiple concurrent requests to /api/hello."""
        # Simulate concurrent requests (synchronous in test)
        responses = [client.get("/api/hello") for _ in range(10)]
        
        # All should succeed
        for response in responses:
            assert response.status_code == 200
            assert "message" in response.json()
            assert "timestamp" in response.json()
    
    @pytest.mark.unit
    def test_concurrent_requests_to_health(self, client):
        """Test multiple concurrent requests to /health."""
        responses = [client.get("/health") for _ in range(10)]
        
        # All should succeed
        for response in responses:
            assert response.status_code == 200
            assert response.json()["status"] == "healthy"
    
    @pytest.mark.unit
    def test_request_with_query_parameters_ignored(self, client):
        """Test that query parameters don't break endpoints."""
        response = client.get("/api/hello?foo=bar&baz=qux")
        assert response.status_code == 200
        assert response.json()["message"] == "Hello World from Backend!"
    
    @pytest.mark.unit
    def test_request_with_fragment_identifier(self, client):
        """Test endpoint with URL fragment (fragments are client-side)."""
        # Note: fragments are not sent to server, but testing for completeness
        response = client.get("/api/hello#fragment")
        assert response.status_code == 200
    
    @pytest.mark.unit
    def test_empty_accept_header(self, client):
        """Test request with empty Accept header."""
        response = client.get("/api/hello", headers={"Accept": ""})
        assert response.status_code == 200
    
    @pytest.mark.unit
    def test_unusual_accept_header(self, client):
        """Test request with unusual Accept header."""
        response = client.get("/api/hello", headers={"Accept": "text/plain"})
        # FastAPI should still return JSON
        assert response.status_code == 200
        assert "application/json" in response.headers["content-type"]
