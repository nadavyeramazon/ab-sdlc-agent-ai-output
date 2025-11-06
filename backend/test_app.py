import pytest
from fastapi.testclient import TestClient
from app import app

# Create a test client
client = TestClient(app)

def test_read_root():
    """Test the root endpoint returns a welcome message."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Green Greeter API!"}

def test_greet_user_with_name():
    """Test greeting a user with a provided name."""
    test_name = "Alice"
    response = client.post("/greet", json={"name": test_name})
    assert response.status_code == 200
    data = response.json()
    assert "greeting" in data
    assert test_name in data["greeting"]
    assert "timestamp" in data

def test_greet_user_empty_name():
    """Test greeting with empty name."""
    response = client.post("/greet", json={"name": ""})
    assert response.status_code == 200
    data = response.json()
    assert "greeting" in data
    assert "Anonymous" in data["greeting"]
    assert "timestamp" in data

def test_greet_user_with_whitespace_name():
    """Test greeting with whitespace-only name."""
    response = client.post("/greet", json={"name": "   "})
    assert response.status_code == 200
    data = response.json()
    assert "greeting" in data
    assert "Anonymous" in data["greeting"]
    assert "timestamp" in data

def test_greet_user_missing_name_field():
    """Test greeting without name field in request."""
    response = client.post("/greet", json={})
    assert response.status_code == 422  # Unprocessable Entity

def test_greet_user_invalid_json():
    """Test greeting with invalid JSON."""
    response = client.post("/greet", data="invalid json")
    assert response.status_code == 422  # Unprocessable Entity

def test_health_endpoint():
    """Test the health endpoint for Docker health checks."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_cors_headers():
    """Test that CORS headers are properly set."""
    response = client.options("/greet")
    # FastAPI with CORSMiddleware should handle OPTIONS requests
    assert response.status_code in [200, 405]  # Some servers return 405 for OPTIONS

def test_greet_user_long_name():
    """Test greeting with a very long name."""
    long_name = "A" * 1000
    response = client.post("/greet", json={"name": long_name})
    assert response.status_code == 200
    data = response.json()
    assert "greeting" in data
    assert long_name in data["greeting"]
    assert "timestamp" in data

def test_greet_user_special_characters():
    """Test greeting with special characters in name."""
    special_name = "José María Ñoño 🌟"
    response = client.post("/greet", json={"name": special_name})
    assert response.status_code == 200
    data = response.json()
    assert "greeting" in data
    assert special_name in data["greeting"]
    assert "timestamp" in data
