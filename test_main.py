import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client() -> TestClient:
    """Create a test client fixture"""
    return TestClient(app)


def test_hello_endpoint(client: TestClient) -> None:
    """Test the /api/hello endpoint"""
    response = client.get("/api/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_health_check_endpoint(client: TestClient) -> None:
    """Test the /health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_hello_endpoint_returns_json(client: TestClient) -> None:
    """Test that /api/hello returns JSON content type"""
    response = client.get("/api/hello")
    assert response.headers["content-type"] == "application/json"


def test_health_endpoint_returns_json(client: TestClient) -> None:
    """Test that /health returns JSON content type"""
    response = client.get("/health")
    assert response.headers["content-type"] == "application/json"


def test_cors_headers(client: TestClient) -> None:
    """Test that CORS headers are present"""
    response = client.get("/api/hello")
    assert "access-control-allow-origin" in response.headers
