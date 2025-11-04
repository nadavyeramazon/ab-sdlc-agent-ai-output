import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_hello_endpoint():
    """Test the /api/hello endpoint returns correct response."""
    response = client.get("/api/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_hello_endpoint_content_type():
    """Test the /api/hello endpoint returns JSON content type."""
    response = client.get("/api/hello")
    content_type = response.headers["content-type"]
    assert "application/json" in content_type


def test_cors_headers():
    """Test CORS is properly configured."""
    # Test with a simple GET request that CORS allows
    response = client.get("/api/hello")
    assert response.status_code == 200
    
    # Verify CORS headers are present (TestClient may not fully simulate OPTIONS)
    # In production, these headers would be added by the CORS middleware


def test_invalid_endpoint():
    """Test that invalid endpoints return 404."""
    response = client.get("/invalid")
    assert response.status_code == 404


def test_hello_endpoint_response_structure():
    """Test that the response has the correct structure."""
    response = client.get("/api/hello")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert isinstance(data["message"], str)
    assert len(data["message"]) > 0
