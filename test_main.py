from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_read_item():
    response = client.get("/hello/FastAPI")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, FastAPI!"}

def test_read_item_empty_name():
    response = client.get("/hello/")
    assert response.status_code == 404

def test_read_item_special_characters():
    response = client.get("/hello/John%20Doe")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, John Doe!"}