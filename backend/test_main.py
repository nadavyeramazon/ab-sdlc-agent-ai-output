"""Comprehensive tests for FastAPI backend.

Tests cover:
- API endpoint functionality
- Response format validation
- CORS configuration
- Performance requirements
- Health check endpoint
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime
import time
from main import app

client = TestClient(app)


class TestHelloEndpoint:
    """Test suite for /api/hello endpoint."""
    
    def test_hello_endpoint_returns_200(self):
        """Test that /api/hello returns 200 status code."""
        response = client.get("/api/hello")
        assert response.status_code == 200
    
    def test_hello_endpoint_returns_json(self):
        """Test that /api/hello returns JSON content type."""
        response = client.get("/api/hello")
        assert response.headers["content-type"] == "application/json"
    
    def test_hello_endpoint_response_structure(self):
        """Test that /api/hello returns correct JSON structure."""
        response = client.get("/api/hello")
        data = response.json()
        
        # Verify response has required keys
        assert "message" in data
        assert "timestamp" in data
    
    def test_hello_endpoint_message_content(self):
        """Test that /api/hello returns correct message."""
        response = client.get("/api/hello")
        data = response.json()
        
        assert data["message"] == "Hello World from Backend!"
    
    def test_hello_endpoint_timestamp_format(self):
        """Test that /api/hello returns ISO-8601 formatted timestamp."""
        response = client.get("/api/hello")
        data = response.json()
        
        # Verify timestamp is in ISO-8601 format and ends with Z
        timestamp = data["timestamp"]
        assert timestamp.endswith("Z")
        
        # Verify timestamp can be parsed as ISO-8601
        try:
            datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        except ValueError:
            pytest.fail("Timestamp is not in valid ISO-8601 format")
    
    def test_hello_endpoint_performance(self):
        """Test that /api/hello responds within 100ms."""
        start_time = time.time()
        response = client.get("/api/hello")
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000  # Convert to ms
        assert response_time < 100, f"Response time {response_time}ms exceeds 100ms limit"


class TestHealthEndpoint:
    """Test suite for /health endpoint."""
    
    def test_health_endpoint_returns_200(self):
        """Test that /health returns 200 status code."""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_endpoint_returns_json(self):
        """Test that /health returns JSON content type."""
        response = client.get("/health")
        assert response.headers["content-type"] == "application/json"
    
    def test_health_endpoint_response_structure(self):
        """Test that /health returns correct JSON structure."""
        response = client.get("/health")
        data = response.json()
        
        assert "status" in data
        assert data["status"] == "healthy"
    
    def test_health_endpoint_performance(self):
        """Test that /health responds within 100ms."""
        start_time = time.time()
        response = client.get("/health")
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000  # Convert to ms
        assert response_time < 100, f"Response time {response_time}ms exceeds 100ms limit"


class TestCORS:
    """Test suite for CORS configuration."""
    
    def test_cors_headers_present(self):
        """Test that CORS headers are present in response."""
        response = client.options(
            "/api/hello",
            headers={"Origin": "http://localhost:3000", "Access-Control-Request-Method": "GET"}
        )
        
        # CORS headers should be present
        assert "access-control-allow-origin" in response.headers
    
    def test_cors_allows_localhost_3000(self):
        """Test that CORS allows requests from http://localhost:3000."""
        response = client.get(
            "/api/hello",
            headers={"Origin": "http://localhost:3000"}
        )
        
        assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"


class TestAPIDocumentation:
    """Test suite for API documentation."""
    
    def test_openapi_docs_available(self):
        """Test that OpenAPI documentation is available at /docs."""
        response = client.get("/docs")
        assert response.status_code == 200
    
    def test_openapi_json_available(self):
        """Test that OpenAPI JSON schema is available."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        data = response.json()
        assert "openapi" in data
        assert "info" in data
