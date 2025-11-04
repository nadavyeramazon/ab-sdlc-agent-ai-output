"""
Tests for health check endpoint.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint returns 200 and correct data."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "timestamp" in data


def test_health_check_response_structure():
    """Test health check response has correct structure."""
    response = client.get("/api/v1/health")
    data = response.json()
    
    # Check all required fields are present
    required_fields = ["status", "version", "timestamp"]
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"


def test_health_check_version():
    """Test health check returns version information."""
    response = client.get("/api/v1/health")
    data = response.json()
    
    assert isinstance(data["version"], str)
    assert len(data["version"]) > 0
