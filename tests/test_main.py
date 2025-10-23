from typing import Generator
import pytest
from fastapi.testclient import TestClient
from src.main import app, __version__

@pytest.fixture
def client() -> Generator:
    """Create a test client fixture.
    
    Returns:
        Generator: A TestClient instance for testing the API
    """
    with TestClient(app) as test_client:
        yield test_client

def test_hello_world(client: TestClient) -> None:
    """Test the hello world endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}
    assert "X-API-Version" in response.headers
    assert response.headers["X-API-Version"] == __version__

def test_health_check(client: TestClient) -> None:
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_rate_limiting(client: TestClient) -> None:
    """Test rate limiting functionality."""
    # Make 6 requests (exceeding the 5/minute limit)
    for _ in range(5):
        response = client.get("/")
        assert response.status_code == 200
    
    # The 6th request should be rate limited
    response = client.get("/")
    assert response.status_code == 429

def test_cors_headers(client: TestClient) -> None:
    """Test CORS headers are properly set."""
    response = client.options(
        "/",
        headers={"Origin": "http://example.com", "Access-Control-Request-Method": "GET"}
    )
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
    assert response.headers["access-control-allow-origin"] == "*"

def test_invalid_route(client: TestClient) -> None:
    """Test handling of invalid routes."""
    response = client.get("/invalid")
    assert response.status_code == 404
