"""Integration tests for the FastAPI application."""

import pytest
from fastapi.testclient import TestClient
from src.app import create_app

@pytest.fixture
def client():
    """Create test client fixture."""
    app = create_app()
    return TestClient(app)

def test_hello_endpoint(client):
    """Test the /hello endpoint returns correct response."""
    response = client.get("/api/v1/hello")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Hello, World!"
