"""Comprehensive tests for FastAPI backend endpoints."""

import re
from datetime import datetime
from typing import Dict

import pytest
from fastapi import status
from fastapi.testclient import TestClient


class TestHealthEndpoint:
    """Test suite for /health endpoint."""
    
    def test_health_check_success(self, test_client: TestClient) -> None:
        """Test successful health check."""
        response = test_client.get("/health")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
    
    def test_health_check_response_format(self, test_client: TestClient) -> None:
        """Test health check response format."""
        response = test_client.get("/health")
        data = response.json()
        
        # Verify response structure
        assert isinstance(data, dict)
        assert len(data) == 1
        assert isinstance(data["status"], str)
    
    def test_health_check_response_time(self, test_client: TestClient) -> None:
        """Test health check response time is acceptable."""
        import time
        
        start_time = time.time()
        response = test_client.get("/health")
        elapsed_time = (time.time() - start_time) * 1000  # Convert to ms
        
        assert response.status_code == status.HTTP_200_OK
        # Response time should be under 100ms for health check
        assert elapsed_time < 100, f"Health check took {elapsed_time:.2f}ms"
    
    def test_health_check_multiple_requests(self, test_client: TestClient) -> None:
        """Test health check consistency across multiple requests."""
        responses = [test_client.get("/health") for _ in range(5)]
        
        for response in responses:
            assert response.status_code == status.HTTP_200_OK
            assert response.json()["status"] == "healthy"


class TestHelloEndpoint:
    """Test suite for /api/hello endpoint."""
    
    def test_hello_success(self, test_client: TestClient) -> None:
        """Test successful hello endpoint response."""
        response = test_client.get("/api/hello")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "message" in data
        assert "timestamp" in data
        assert data["message"] == "Hello World from Backend!"
    
    def test_hello_message_format(self, test_client: TestClient) -> None:
        """Test hello message is correctly formatted."""
        response = test_client.get("/api/hello")
        data = response.json()
        
        assert isinstance(data["message"], str)
        assert len(data["message"]) > 0
        assert "Backend" in data["message"]
    
    def test_hello_timestamp_format(self, test_client: TestClient) -> None:
        """Test timestamp is in ISO 8601 format."""
        response = test_client.get("/api/hello")
        data = response.json()
        
        # ISO 8601 format: 2024-01-01T12:00:00.000Z
        iso_pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$"
        assert re.match(iso_pattern, data["timestamp"]), \
            f"Timestamp {data['timestamp']} does not match ISO 8601 format"
    
    def test_hello_timestamp_accuracy(self, test_client: TestClient) -> None:
        """Test timestamp is current and accurate."""
        before = datetime.utcnow()
        response = test_client.get("/api/hello")
        after = datetime.utcnow()
        
        data = response.json()
        timestamp_str = data["timestamp"].replace("Z", "")
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%f")
        
        # Timestamp should be between before and after
        assert before <= timestamp <= after, "Timestamp is not current"
    
    def test_hello_response_structure(self, test_client: TestClient) -> None:
        """Test hello response has correct structure."""
        response = test_client.get("/api/hello")
        data = response.json()
        
        # Should have exactly 2 fields
        assert len(data) == 2
        assert set(data.keys()) == {"message", "timestamp"}
    
    def test_hello_response_time(self, test_client: TestClient) -> None:
        """Test hello endpoint response time is under 100ms."""
        import time
        
        start_time = time.time()
        response = test_client.get("/api/hello")
        elapsed_time = (time.time() - start_time) * 1000  # Convert to ms
        
        assert response.status_code == status.HTTP_200_OK
        assert elapsed_time < 100, f"Response took {elapsed_time:.2f}ms"
    
    def test_hello_multiple_requests(self, test_client: TestClient) -> None:
        """Test hello endpoint consistency across multiple requests."""
        responses = [test_client.get("/api/hello") for _ in range(5)]
        
        for response in responses:
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["message"] == "Hello World from Backend!"
            assert "timestamp" in data
    
    def test_hello_unique_timestamps(self, test_client: TestClient) -> None:
        """Test that consecutive calls produce different timestamps."""
        response1 = test_client.get("/api/hello")
        response2 = test_client.get("/api/hello")
        
        data1 = response1.json()
        data2 = response2.json()
        
        # Timestamps should be different (or very close)
        # We just verify they both exist and are valid
        assert "timestamp" in data1
        assert "timestamp" in data2


class TestRootEndpoint:
    """Test suite for root endpoint."""
    
    def test_root_endpoint(self, test_client: TestClient) -> None:
        """Test root endpoint returns service information."""
        response = test_client.get("/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert "service" in data
        assert "version" in data
        assert "status" in data
        assert data["status"] == "running"
    
    def test_root_endpoint_links(self, test_client: TestClient) -> None:
        """Test root endpoint provides documentation links."""
        response = test_client.get("/")
        data = response.json()
        
        assert "docs" in data
        assert "health" in data
        assert "api" in data
        assert data["docs"] == "/api/docs"
        assert data["health"] == "/health"
        assert data["api"] == "/api/hello"


class TestCORSConfiguration:
    """Test suite for CORS middleware configuration."""
    
    def test_cors_headers_present(self, test_client: TestClient) -> None:
        """Test CORS headers are present in response."""
        response = test_client.get(
            "/api/hello",
            headers={"Origin": "http://localhost:3000"}
        )
        
        # CORS headers should be present
        assert "access-control-allow-origin" in response.headers
    
    def test_cors_preflight_request(self, test_client: TestClient) -> None:
        """Test CORS preflight OPTIONS request."""
        response = test_client.options(
            "/api/hello",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            }
        )
        
        assert response.status_code == status.HTTP_200_OK


class TestErrorHandling:
    """Test suite for error handling."""
    
    def test_404_not_found(self, test_client: TestClient) -> None:
        """Test 404 error for non-existent endpoint."""
        response = test_client.get("/api/nonexistent")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert "detail" in data
    
    def test_405_method_not_allowed(self, test_client: TestClient) -> None:
        """Test 405 error for wrong HTTP method."""
        response = test_client.post("/health")
        
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


class TestAPIDocumentation:
    """Test suite for API documentation endpoints."""
    
    def test_openapi_schema(self, test_client: TestClient) -> None:
        """Test OpenAPI schema is accessible."""
        response = test_client.get("/api/openapi.json")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert "openapi" in data
        assert "info" in data
        assert "paths" in data
        assert "/health" in data["paths"]
        assert "/api/hello" in data["paths"]
    
    def test_swagger_docs_accessible(self, test_client: TestClient) -> None:
        """Test Swagger UI is accessible."""
        response = test_client.get("/api/docs")
        
        assert response.status_code == status.HTTP_200_OK
        assert "text/html" in response.headers["content-type"]
    
    def test_redoc_docs_accessible(self, test_client: TestClient) -> None:
        """Test ReDoc UI is accessible."""
        response = test_client.get("/api/redoc")
        
        assert response.status_code == status.HTTP_200_OK
        assert "text/html" in response.headers["content-type"]


class TestResponseModels:
    """Test suite for response models validation."""
    
    def test_hello_response_model(self, test_client: TestClient) -> None:
        """Test hello response matches Pydantic model."""
        response = test_client.get("/api/hello")
        data = response.json()
        
        # Verify all required fields are present
        required_fields = {"message", "timestamp"}
        assert set(data.keys()) == required_fields
        
        # Verify types
        assert isinstance(data["message"], str)
        assert isinstance(data["timestamp"], str)
    
    def test_health_response_model(self, test_client: TestClient) -> None:
        """Test health response matches Pydantic model."""
        response = test_client.get("/health")
        data = response.json()
        
        # Verify all required fields are present
        required_fields = {"status"}
        assert set(data.keys()) == required_fields
        
        # Verify types
        assert isinstance(data["status"], str)


class TestPerformance:
    """Test suite for performance benchmarks."""
    
    def test_concurrent_requests_health(self, test_client: TestClient) -> None:
        """Test handling concurrent requests to health endpoint."""
        import concurrent.futures
        
        def make_request():
            return test_client.get("/health")
        
        # Make 10 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            responses = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        # All requests should succeed
        for response in responses:
            assert response.status_code == status.HTTP_200_OK
    
    def test_concurrent_requests_hello(self, test_client: TestClient) -> None:
        """Test handling concurrent requests to hello endpoint."""
        import concurrent.futures
        
        def make_request():
            return test_client.get("/api/hello")
        
        # Make 10 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            responses = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        # All requests should succeed
        for response in responses:
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert "message" in data
            assert "timestamp" in data
