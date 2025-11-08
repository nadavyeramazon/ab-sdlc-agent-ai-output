from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/greet")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, user!"}

def test_cors_headers():
    response = client.options("/greet")
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
    assert response.headers["access-control-allow-origin"] == "*"