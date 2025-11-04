from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "service" in data

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_generate_success():
    response = client.post("/api/generate", json={"prompt": "test prompt"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "result" in data
    assert "test prompt" in data["result"]

def test_generate_with_context():
    response = client.post("/api/generate", json={
        "prompt": "test prompt",
        "context": "some context"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "result" in data

def test_generate_empty_prompt():
    response = client.post("/api/generate", json={"prompt": ""})
    assert response.status_code == 400

def test_generate_missing_prompt():
    response = client.post("/api/generate", json={})
    assert response.status_code == 422