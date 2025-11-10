"""Comprehensive tests for FastAPI Backend

Tests all API endpoints and validates responses.
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from main import app

client = TestClient(app)


class TestHealthEndpoint:
    """Tests for /health endpoint"""
    
    def test_health_check_returns_200(self):
        """Test that health check returns 200 status code"""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_check_returns_healthy_status(self):
        """Test that health check returns healthy status"""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
    
    def test_health_check_returns_json(self):
        """Test that health check returns JSON content type"""
        response = client.get("/health")
        assert "application/json" in response.headers["content-type"]


class TestHelloEndpoint:
    """Tests for /api/hello endpoint"""
    
    def test_hello_returns_200(self):
        """Test that hello endpoint returns 200 status code"""
        response = client.get("/api/hello")
        assert response.status_code == 200
    
    def test_hello_returns_correct_message(self):
        """Test that hello endpoint returns correct message"""
        response = client.get("/api/hello")
        data = response.json()
        assert "message" in data
        assert data["message"] == "Hello World from Backend!"
    
    def test_hello_returns_timestamp(self):
        """Test that hello endpoint returns timestamp"""
        response = client.get("/api/hello")
        data = response.json()
        assert "timestamp" in data
        assert isinstance(data["timestamp"], str)
    
    def test_hello_timestamp_is_valid_iso_format(self):
        """Test that timestamp is in valid ISO format"""
        response = client.get("/api/hello")
        data = response.json()
        timestamp = data["timestamp"]
        
        # Try to parse timestamp - will raise exception if invalid
        try:
            datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except ValueError:
            pytest.fail(f"Timestamp {timestamp} is not in valid ISO format")
    
    def test_hello_returns_json(self):
        """Test that hello endpoint returns JSON content type"""
        response = client.get("/api/hello")
        assert "application/json" in response.headers["content-type"]
    
    def test_hello_response_time(self):
        """Test that API response time is under 100ms"""
        import time
        
        start_time = time.time()
        response = client.get("/api/hello")
        end_time = time.time()
        
        response_time_ms = (end_time - start_time) * 1000
        
        assert response.status_code == 200
        assert response_time_ms < 100, f"Response time {response_time_ms}ms exceeds 100ms requirement"


class TestRootEndpoint:
    """Tests for / root endpoint"""
    
    def test_root_returns_200(self):
        """Test that root endpoint returns 200 status code"""
        response = client.get("/")
        assert response.status_code == 200
    
    def test_root_returns_welcome_message(self):
        """Test that root endpoint returns welcome message"""
        response = client.get("/")
        data = response.json()
        assert "message" in data
        assert "Welcome" in data["message"]


class TestCORSConfiguration:
    """Tests for CORS middleware configuration"""
    
    def test_cors_headers_present(self):
        """Test that CORS headers are present in response"""
        response = client.get("/api/hello")
        assert "access-control-allow-origin" in response.headers
    
    def test_cors_allows_all_origins(self):
        """Test that CORS allows all origins (for development)"""
        response = client.get("/api/hello")
        assert response.headers["access-control-allow-origin"] == "*"


class TestAPIIntegration:
    """Integration tests for API functionality"""
    
    def test_multiple_hello_requests_return_different_timestamps(self):
        """Test that multiple requests return different timestamps"""
        import time
        
        response1 = client.get("/api/hello")
        data1 = response1.json()
        
        time.sleep(0.01)  # Small delay to ensure different timestamp
        
        response2 = client.get("/api/hello")
        data2 = response2.json()
        
        assert data1["timestamp"] != data2["timestamp"]
    
    def test_all_endpoints_accessible(self):
        """Test that all required endpoints are accessible"""
        endpoints = ["/", "/health", "/api/hello"]
        
        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.status_code == 200, f"Endpoint {endpoint} returned {response.status_code}"
    
    def test_invalid_endpoint_returns_404(self):
        """Test that invalid endpoints return 404"""
        response = client.get("/invalid/endpoint")
        assert response.status_code == 404


class TestResponseStructure:
    """Tests for response structure validation"""
    
    def test_hello_response_has_required_fields(self):
        """Test that hello response has all required fields"""
        response = client.get("/api/hello")
        data = response.json()
        
        required_fields = ["message", "timestamp"]
        for field in required_fields:
            assert field in data, f"Required field '{field}' missing from response"
    
    def test_health_response_has_required_fields(self):
        """Test that health response has all required fields"""
        response = client.get("/health")
        data = response.json()
        
        assert "status" in data, "Required field 'status' missing from response"
