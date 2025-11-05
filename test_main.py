import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World from Backend"}


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_root_endpoint_content_type():
    response = client.get("/")
    assert response.headers["content-type"] == "application/json"


def test_health_endpoint_content_type():
    response = client.get("/health")
    assert response.headers["content-type"] == "application/json"