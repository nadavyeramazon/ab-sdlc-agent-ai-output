import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from main import app

# Create test client
client = TestClient(app)

def test_health_endpoint():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_hello_endpoint():
    """Test the hello endpoint"""
    response = client.get("/api/hello")
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "timestamp" in data
    assert data["message"] == "Hello World from Backend!"
    
    # Validate timestamp is valid ISO format
    try:
        datetime.fromisoformat(data["timestamp"])
    except ValueError:
        pytest.fail("Timestamp is not in valid ISO format")
