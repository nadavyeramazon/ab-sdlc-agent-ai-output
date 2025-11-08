from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_read_root_content_type():
    response = client.get("/")
    assert response.headers["content-type"] == "application/json"

def test_read_non_existent_route():
    response = client.get("/non-existent")
    assert response.status_code == 404

def test_method_not_allowed():
    response = client.post("/")
    assert response.status_code == 405