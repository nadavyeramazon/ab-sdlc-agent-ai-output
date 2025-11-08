from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}

def test_greet_user():
    name = "Alice"
    response = client.get(f"/greet/{name}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Hello, {name}!"}
