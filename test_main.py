import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}

def test_read_item():
    response = client.get("/hello/TestUser")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, TestUser!"}

def test_read_item_empty_name():
    response = client.get("/hello/")
    assert response.status_code == 404

def test_read_item_special_characters():
    response = client.get("/hello/Test%20User%21")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, Test User!!"}

def test_method_not_allowed():
    response = client.post("/")
    assert response.status_code == 405

def test_not_found():
    response = client.get("/non_existent_endpoint")
    assert response.status_code == 404