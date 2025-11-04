import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "ab-sdlc-agent-ai-backend"
    assert "version" in data


def test_health():
    """Test health check endpoint"""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "ab-sdlc-agent-ai-backend"
    assert "version" in data
    assert "environment" in data


def test_status():
    """Test status endpoint"""
    response = client.get("/api/status")
    assert response.status_code == 200
    data = response.json()
    assert data["online"] is True
    assert "message" in data


def test_cors_headers():
    """Test CORS headers are present"""
    response = client.options(
        "/api/health",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET"
        }
    )
    assert response.status_code == 200
