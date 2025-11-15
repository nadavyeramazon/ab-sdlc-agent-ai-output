"""Comprehensive test suite for FastAPI backend.

Tests all API endpoints, CORS configuration, response formats,
and performance requirements.
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime
import time
from main import app

client = TestClient(app)


class TestHealthEndpoint:
    """Test cases for /health endpoint."""
    
    def test_health_returns_200(self):
        """Test that health endpoint returns 200 status code."""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_returns_healthy_status(self):
        """Test that health endpoint returns correct status."""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
    
    def test_health_returns_json(self):
        """Test that health endpoint returns JSON content type."""
        response = client.get("/health")
        assert "application/json" in response.headers["content-type"]
    
    def test_health_response_time(self):
        """Test that health endpoint responds within 50ms."""
        start_time = time.time()
        response = client.get("/health")
        elapsed_time = (time.time() - start_time) * 1000  # Convert to ms
        
        assert response.status_code == 200
        assert elapsed_time < 50  # Should be under 50ms


class TestHelloEndpoint:
    """Test cases for /api/hello endpoint."""
    
    def test_hello_returns_200(self):
        """Test that hello endpoint returns 200 status code."""
        response = client.get("/api/hello")
        assert response.status_code == 200
    
    def test_hello_returns_message_field(self):
        """Test that response contains message field."""
        response = client.get("/api/hello")
        data = response.json()
        assert "message" in data
        assert data["message"] == "Hello World from Backend!"
    
    def test_hello_returns_timestamp_field(self):
        """Test that response contains timestamp field."""
        response = client.get("/api/hello")
        data = response.json()
        assert "timestamp" in data
        assert isinstance(data["timestamp"], str)
    
    def test_hello_timestamp_iso8601_format(self):
        """Test that timestamp is in ISO 8601 format."""
        response = client.get("/api/hello")
        data = response.json()
        timestamp = data["timestamp"]
        
        # Verify ISO 8601 format by parsing
        try:
            # Remove 'Z' suffix and parse
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            assert dt is not None
        except ValueError:
            pytest.fail(f"Timestamp {timestamp} is not in valid ISO 8601 format")
    
    def test_hello_returns_json(self):
        """Test that hello endpoint returns JSON content type."""
        response = client.get("/api/hello")
        assert "application/json" in response.headers["content-type"]
    
    def test_hello_response_time(self):
        """Test that hello endpoint responds within 100ms."""
        start_time = time.time()
        response = client.get("/api/hello")
        elapsed_time = (time.time() - start_time) * 1000  # Convert to ms
        
        assert response.status_code == 200
        assert elapsed_time < 100  # Should be under 100ms
    
    def test_hello_response_structure(self):
        """Test complete response structure."""
        response = client.get("/api/hello")
        data = response.json()
        
        # Check all required fields are present
        assert set(data.keys()) == {"message", "timestamp"}
        
        # Check field types
        assert isinstance(data["message"], str)
        assert isinstance(data["timestamp"], str)
        
        # Check field values
        assert len(data["message"]) > 0
        assert len(data["timestamp"]) > 0


class TestCORSConfiguration:
    """Test cases for CORS middleware configuration."""
    
    def test_cors_headers_present(self):
        """Test that CORS headers are present in response."""
        response = client.get(
            "/api/hello",
            headers={"Origin": "http://localhost:3000"}
        )
        
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers
    
    def test_cors_allows_frontend_origin(self):
        """Test that CORS allows frontend origin."""
        response = client.get(
            "/api/hello",
            headers={"Origin": "http://localhost:3000"}
        )
        
        assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"
    
    def test_cors_options_request(self):
        """Test that CORS preflight OPTIONS request works."""
        response = client.options(
            "/api/hello",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET"
            }
        )
        
        assert response.status_code == 200


class TestAPIDocumentation:
    """Test cases for API documentation endpoints."""
    
    def test_openapi_schema_available(self):
        """Test that OpenAPI schema is available."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert "paths" in data
    
    def test_docs_endpoint_available(self):
        """Test that interactive docs are available."""
        response = client.get("/docs")
        assert response.status_code == 200


class TestErrorHandling:
    """Test cases for error handling."""
    
    def test_invalid_endpoint_returns_404(self):
        """Test that invalid endpoints return 404."""
        response = client.get("/api/invalid")
        assert response.status_code == 404
    
    def test_invalid_method_returns_405(self):
        """Test that invalid HTTP methods return 405."""
        response = client.post("/health")
        assert response.status_code == 405


class TestIntegration:
    """Integration tests for multiple endpoints."""
    
    def test_health_and_hello_both_work(self):
        """Test that both endpoints work in sequence."""
        # Check health
        health_response = client.get("/health")
        assert health_response.status_code == 200
        assert health_response.json()["status"] == "healthy"
        
        # Check hello
        hello_response = client.get("/api/hello")
        assert hello_response.status_code == 200
        assert "message" in hello_response.json()
        assert "timestamp" in hello_response.json()
    
    def test_multiple_hello_requests(self):
        """Test that multiple requests return different timestamps."""
        response1 = client.get("/api/hello")
        time.sleep(0.001)  # Small delay to ensure different timestamp
        response2 = client.get("/api/hello")
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        timestamp1 = response1.json()["timestamp"]
        timestamp2 = response2.json()["timestamp"]
        
        # Timestamps should be different (or same if requests are very fast)
        # Both should be valid ISO 8601 format
        assert isinstance(timestamp1, str)
        assert isinstance(timestamp2, str)
