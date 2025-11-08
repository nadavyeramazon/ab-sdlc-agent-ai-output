from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_read_root_incorrect_method():
    response = client.post("/")
    assert response.status_code == 405  # Method Not Allowed

def test_nonexistent_route():
    response = client.get("/nonexistent")
    assert response.status_code == 404  # Not Found

def test_read_root_headers():
    response = client.get("/")
    assert response.headers["content-type"] == "application/json"

def test_read_root_performance():
    import time
    start_time = time.time()
    client.get("/")
    end_time = time.time()
    assert end_time - start_time < 0.1  # Ensure response time is less than 100ms