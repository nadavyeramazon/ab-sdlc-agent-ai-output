from fastapi.testclient import TestClient
import pytest
from main import app

@pytest.fixture
def client():
    return TestClient(app=app)

def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert "<h1>Hello, World!</h1>" in response.text

def test_api_hello(client):
    response = client.get("/api/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}