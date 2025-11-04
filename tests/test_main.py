"""
Tests for main application endpoints and configuration.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint returns welcome message."""
    response = client.get("/")
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "docs" in data
    assert "health" in data


def test_openapi_json():
    """Test OpenAPI JSON endpoint is accessible."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    
    data = response.json()
    assert "openapi" in data
    assert "info" in data
    assert "paths" in data


def test_docs_endpoint():
    """Test Swagger UI docs endpoint is accessible."""
    response = client.get("/docs")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_redoc_endpoint():
    """Test ReDoc endpoint is accessible."""
    response = client.get("/redoc")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_api_version_prefix():
    """Test API endpoints are accessible under /api/v1 prefix."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200


def test_cors_headers():
    """Test CORS headers are present in responses."""
    response = client.get(
        "/api/v1/health",
        headers={"Origin": "http://localhost:3000"}
    )
    assert response.status_code == 200
    # CORS middleware should add appropriate headers
    assert "access-control-allow-origin" in response.headers
