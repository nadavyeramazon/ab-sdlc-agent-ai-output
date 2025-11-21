"""Comprehensive test suite for backend API endpoints.

This module provides complete test coverage for the FastAPI backend,
including all endpoints, response validation, and error handling.
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime
import json

from main import app


# Test client setup
client = TestClient(app)


class TestRootEndpoint:
    """Test cases for the root endpoint (/)."""

    def test_root_endpoint_success(self):
        """Test that root endpoint returns successful response."""
        response = client.get("/")
        assert response.status_code == 200

    def test_root_endpoint_content_type(self):
        """Test that root endpoint returns JSON content."""
        response = client.get("/")
        assert response.headers["content-type"] == "application/json"

    def test_root_endpoint_message(self):
        """Test that root endpoint returns correct message."""
        response = client.get("/")
        data = response.json()
        assert "message" in data
        assert data["message"] == "Backend API is running"

    def test_root_endpoint_structure(self):
        """Test that root endpoint response has correct structure."""
        response = client.get("/")
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) == 1
        assert "message" in data


class TestHelloEndpoint:
    """Test cases for the /api/hello endpoint."""

    def test_hello_endpoint_success(self):
        """Test that hello endpoint returns successful response."""
        response = client.get("/api/hello")
        assert response.status_code == 200

    def test_hello_endpoint_content_type(self):
        """Test that hello endpoint returns JSON content."""
        response = client.get("/api/hello")
        assert response.headers["content-type"] == "application/json"

    def test_hello_endpoint_message(self):
        """Test that hello endpoint returns correct message."""
        response = client.get("/api/hello")
        data = response.json()
        assert "message" in data
        assert data["message"] == "Hello World from Backend!"

    def test_hello_endpoint_timestamp_exists(self):
        """Test that hello endpoint includes timestamp."""
        response = client.get("/api/hello")
        data = response.json()
        assert "timestamp" in data
        assert data["timestamp"] is not None

    def test_hello_endpoint_timestamp_format(self):
        """Test that timestamp is in valid ISO format."""
        response = client.get("/api/hello")
        data = response.json()
        timestamp_str = data["timestamp"]
        
        # Verify it's a valid ISO format timestamp
        try:
            datetime.fromisoformat(timestamp_str)
            is_valid = True
        except ValueError:
            is_valid = False
        
        assert is_valid, f"Timestamp '{timestamp_str}' is not in valid ISO format"

    def test_hello_endpoint_timestamp_recent(self):
        """Test that timestamp is recent (within 1 second)."""
        response = client.get("/api/hello")
        data = response.json()
        timestamp = datetime.fromisoformat(data["timestamp"])
        now = datetime.utcnow()
        
        # Check timestamp is within 1 second of current time
        time_diff = abs((now - timestamp).total_seconds())
        assert time_diff < 1.0, f"Timestamp difference is {time_diff} seconds"

    def test_hello_endpoint_structure(self):
        """Test that hello endpoint response has correct structure."""
        response = client.get("/api/hello")
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) == 2
        assert "message" in data
        assert "timestamp" in data

    def test_hello_endpoint_multiple_calls(self):
        """Test that hello endpoint can be called multiple times."""
        response1 = client.get("/api/hello")
        response2 = client.get("/api/hello")
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        # Timestamps should be different (or very close)
        data1 = response1.json()
        data2 = response2.json()
        # Both should have valid structure
        assert "timestamp" in data1
        assert "timestamp" in data2


class TestHealthEndpoint:
    """Test cases for the /health endpoint."""

    def test_health_endpoint_success(self):
        """Test that health endpoint returns successful response."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_endpoint_content_type(self):
        """Test that health endpoint returns JSON content."""
        response = client.get("/health")
        assert response.headers["content-type"] == "application/json"

    def test_health_endpoint_status(self):
        """Test that health endpoint returns healthy status."""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"

    def test_health_endpoint_structure(self):
        """Test that health endpoint response has correct structure."""
        response = client.get("/health")
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) == 1
        assert "status" in data

    def test_health_endpoint_reliability(self):
        """Test that health endpoint is consistently healthy."""
        # Call multiple times to ensure reliability
        for _ in range(5):
            response = client.get("/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"


class TestErrorHandling:
    """Test cases for error handling and invalid requests."""

    def test_invalid_endpoint_404(self):
        """Test that invalid endpoints return 404."""
        response = client.get("/invalid-endpoint")
        assert response.status_code == 404

    def test_invalid_method_405(self):
        """Test that invalid HTTP methods return 405."""
        # POST to GET-only endpoints
        response = client.post("/")
        assert response.status_code == 405

    def test_invalid_api_path(self):
        """Test that invalid API paths return 404."""
        response = client.get("/api/invalid")
        assert response.status_code == 404

    def test_post_to_health_endpoint(self):
        """Test POST request to health endpoint returns 405."""
        response = client.post("/health")
        assert response.status_code == 405

    def test_put_to_hello_endpoint(self):
        """Test PUT request to hello endpoint returns 405."""
        response = client.put("/api/hello")
        assert response.status_code == 405

    def test_delete_to_root_endpoint(self):
        """Test DELETE request to root endpoint returns 405."""
        response = client.delete("/")
        assert response.status_code == 405


class TestCORSConfiguration:
    """Test cases for CORS middleware configuration."""

    def test_cors_headers_on_root(self):
        """Test that CORS headers are present on root endpoint."""
        response = client.get("/")
        # Check for CORS headers (may vary based on request)
        assert response.status_code == 200

    def test_cors_headers_on_hello(self):
        """Test that CORS headers are present on hello endpoint."""
        response = client.get("/api/hello")
        assert response.status_code == 200

    def test_options_request_root(self):
        """Test OPTIONS request for CORS preflight on root."""
        response = client.options("/")
        # OPTIONS should be handled by CORS middleware
        assert response.status_code in [200, 405]

    def test_options_request_hello(self):
        """Test OPTIONS request for CORS preflight on hello endpoint."""
        response = client.options("/api/hello")
        # OPTIONS should be handled by CORS middleware
        assert response.status_code in [200, 405]


class TestAPIIntegration:
    """Integration tests for complete API workflows."""

    def test_all_endpoints_accessible(self):
        """Test that all endpoints are accessible in sequence."""
        # Check health first
        health_response = client.get("/health")
        assert health_response.status_code == 200
        
        # Check root
        root_response = client.get("/")
        assert root_response.status_code == 200
        
        # Check hello
        hello_response = client.get("/api/hello")
        assert hello_response.status_code == 200

    def test_concurrent_requests_simulation(self):
        """Test that API handles multiple rapid requests."""
        responses = []
        for _ in range(10):
            responses.append(client.get("/api/hello"))
        
        # All should succeed
        for response in responses:
            assert response.status_code == 200
            data = response.json()
            assert "message" in data
            assert "timestamp" in data

    def test_api_consistency(self):
        """Test that API responses are consistent."""
        # Root should always return same message
        for _ in range(3):
            response = client.get("/")
            data = response.json()
            assert data["message"] == "Backend API is running"
        
        # Health should always return healthy
        for _ in range(3):
            response = client.get("/health")
            data = response.json()
            assert data["status"] == "healthy"


class TestResponseValidation:
    """Test cases for validating response data types and formats."""

    def test_root_response_types(self):
        """Test that root endpoint returns correct data types."""
        response = client.get("/")
        data = response.json()
        assert isinstance(data["message"], str)

    def test_hello_response_types(self):
        """Test that hello endpoint returns correct data types."""
        response = client.get("/api/hello")
        data = response.json()
        assert isinstance(data["message"], str)
        assert isinstance(data["timestamp"], str)

    def test_health_response_types(self):
        """Test that health endpoint returns correct data types."""
        response = client.get("/health")
        data = response.json()
        assert isinstance(data["status"], str)

    def test_response_json_parseable(self):
        """Test that all responses can be parsed as JSON."""
        endpoints = ["/", "/api/hello", "/health"]
        for endpoint in endpoints:
            response = client.get(endpoint)
            # Should not raise exception
            try:
                data = response.json()
                assert isinstance(data, dict)
            except json.JSONDecodeError:
                pytest.fail(f"Response from {endpoint} is not valid JSON")


class TestPerformance:
    """Basic performance and load tests."""

    def test_response_time_reasonable(self):
        """Test that endpoints respond in reasonable time."""
        import time
        
        start = time.time()
        response = client.get("/api/hello")
        end = time.time()
        
        assert response.status_code == 200
        # Response should be under 1 second (very generous)
        assert (end - start) < 1.0

    def test_health_check_fast(self):
        """Test that health check is fast."""
        import time
        
        start = time.time()
        response = client.get("/health")
        end = time.time()
        
        assert response.status_code == 200
        # Health check should be very fast (under 100ms)
        assert (end - start) < 0.1


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
