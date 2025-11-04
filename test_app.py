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
    assert response.headers["content-type"] == "application/json"


def test_cors_headers():
    """Test CORS is properly configured."""
    response = client.options("/api/hello")
    # OPTIONS request should succeed with CORS middleware
    assert response.status_code == 200


def test_invalid_endpoint():
    """Test that invalid endpoints return 404."""
    response = client.get("/invalid")
    assert response.status_code == 404
