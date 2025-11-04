import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_hello_endpoint():
    """Test the /api/hello endpoint"""
    response = client.get("/api/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_health_endpoint():
    """Test the /health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_cors_headers():
    """Test CORS headers are present"""
    response = client.get("/api/hello")
    assert "access-control-allow-origin" in response.headers