from fastapi.testclient import TestClient
from main import app

client = TestClient(app=app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "<h1>Hello, World!</h1>" in response.text

def test_hello_api():
    response = client.get("/api/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}