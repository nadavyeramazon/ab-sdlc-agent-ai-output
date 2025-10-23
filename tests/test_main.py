"""Test suite for the Hello World API."""

from fastapi.testclient import TestClient
import pytest
from unittest.mock import patch
from src.main import app
from src.config import Settings

client = TestClient(app)

def test_hello_world():
    """Test the hello world endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}
    assert "X-Request-ID" in response.headers

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_404_handler():
    """Test custom 404 error handling."""
    response = client.get("/nonexistent")
    assert response.status_code == 404
    assert response.json() == {"error": "The requested resource was not found"}

def test_rate_limiting():
    """Test rate limiting behavior."""
    # Override rate limit settings for testing
    test_settings = Settings(
        rate_limit_requests=2,
        rate_limit_window=5
    )
    
    with patch('src.main.settings', test_settings):
        # First request should succeed
        response = client.get("/")
        assert response.status_code == 200
        
        # Second request should succeed
        response = client.get("/")
        assert response.status_code == 200
        
        # Third request should be rate limited
        response = client.get("/")
        assert response.status_code == 429
        assert "Retry-After" in response.headers

def test_cors_headers():
    """Test CORS headers are properly set."""
    response = client.options("/", headers={"Origin": "http://example.com"})
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
    assert response.headers["access-control-allow-origin"] == "*"

def test_request_id():
    """Test that each request gets a unique request ID."""
    response1 = client.get("/")
    response2 = client.get("/")
    
    assert "X-Request-ID" in response1.headers
    assert "X-Request-ID" in response2.headers
    assert response1.headers["X-Request-ID"] != response2.headers["X-Request-ID"]
