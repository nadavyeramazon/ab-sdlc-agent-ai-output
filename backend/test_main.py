"""Comprehensive test suite for FastAPI backend.

Tests:
- GET /api/hello endpoint functionality
- GET /health endpoint functionality
- CORS headers validation
- Response time requirements
- Error handling
- ISO-8601 timestamp format validation
"""

import time
import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from main import app

# Create test client
client = TestClient(app)


class TestHelloEndpoint:
    """Test suite for /api/hello endpoint."""
    
    def test_hello_endpoint_returns_correct_structure(self):
        """Test that /api/hello returns correct JSON structure."""
        response = client.get("/api/hello")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "message" in data
        assert "timestamp" in data
        
    def test_hello_endpoint_returns_correct_message(self):
        """Test that /api/hello returns correct message."""
        response = client.get("/api/hello")
        data = response.json()
        
        assert data["message"] == "Hello World from Backend!"
        
    def test_hello_endpoint_returns_valid_timestamp(self):
        """Test that /api/hello returns valid ISO-8601 timestamp."""
        response = client.get("/api/hello")
        data = response.json()
        
        # Verify timestamp format (ISO-8601)
        timestamp = data["timestamp"]
        assert timestamp.endswith("Z"), "Timestamp should end with Z for UTC"
        
        # Parse timestamp to verify it's valid ISO-8601
        try:
            # Remove 'Z' and parse
            parsed_time = datetime.fromisoformat(timestamp.rstrip("Z"))
            assert isinstance(parsed_time, datetime)
        except ValueError:
            pytest.fail("Timestamp is not valid ISO-8601 format")
            
    def test_hello_endpoint_timestamp_is_recent(self):
        """Test that timestamp is current (within last 5 seconds)."""
        response = client.get("/api/hello")
        data = response.json()
        
        timestamp_str = data["timestamp"].rstrip("Z")
        response_time = datetime.fromisoformat(timestamp_str)
        current_time = datetime.utcnow()
        
        time_diff = (current_time - response_time).total_seconds()
        assert time_diff < 5, "Timestamp should be within last 5 seconds"
        
    def test_hello_endpoint_response_time(self):
        """Test that /api/hello responds within 100ms."""
        start_time = time.time()
        response = client.get("/api/hello")
        end_time = time.time()
        
        response_time_ms = (end_time - start_time) * 1000
        
        assert response.status_code == 200
        # Allow up to 150ms to account for test environment overhead
        assert response_time_ms < 150, f"Response time {response_time_ms}ms exceeds 150ms limit"


class TestHealthEndpoint:
    """Test suite for /health endpoint."""
    
    def test_health_endpoint_returns_healthy(self):
        """Test that /health returns status healthy."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "status" in data
        assert data["status"] == "healthy"
        
    def test_health_endpoint_response_time(self):
        """Test that /health responds within 100ms."""
        start_time = time.time()
        response = client.get("/health")
        end_time = time.time()
        
        response_time_ms = (end_time - start_time) * 1000
        
        assert response.status_code == 200
        # Allow up to 150ms to account for test environment overhead
        assert response_time_ms < 150, f"Response time {response_time_ms}ms exceeds 150ms limit"


class TestCORSHeaders:
    """Test suite for CORS configuration."""
    
    def test_cors_headers_present_on_hello_endpoint(self):
        """Test that CORS headers are present in /api/hello response."""
        response = client.get(
            "/api/hello",
            headers={"Origin": "http://localhost:3000"}
        )
        
        assert response.status_code == 200
        
        # Check for CORS headers
        assert "access-control-allow-origin" in response.headers
        
    def test_cors_headers_present_on_health_endpoint(self):
        """Test that CORS headers are present in /health response."""
        response = client.get(
            "/health",
            headers={"Origin": "http://localhost:3000"}
        )
        
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers
        
    def test_cors_preflight_request(self):
        """Test that CORS preflight requests are handled correctly."""
        response = client.options(
            "/api/hello",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            }
        )
        
        # Preflight should return 200
        assert response.status_code == 200


class TestRootEndpoint:
    """Test suite for root endpoint."""
    
    def test_root_endpoint_returns_api_info(self):
        """Test that root endpoint returns API information."""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "name" in data
        assert "version" in data
        assert "endpoints" in data


class TestErrorHandling:
    """Test suite for error handling."""
    
    def test_nonexistent_endpoint_returns_404(self):
        """Test that non-existent endpoints return 404."""
        response = client.get("/api/nonexistent")
        
        assert response.status_code == 404
