from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert "<h1>Hello, World!</h1>" in response.text

def test_api_hello():
    response = client.get("/api/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}