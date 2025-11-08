from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Hello World"
    assert "description" in data
    assert "timestamp" in data

def test_info():
    response = client.get("/info")
    assert response.status_code == 200
    data = response.json()
    assert data["app_name"] == "Simple Hello World API"
    assert data["version"] == "1.0.0"
    assert data["framework"] == "FastAPI"
    assert data["author"] == "AI Agent"
