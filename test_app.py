import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_hello_endpoint():
    response = client.get("/api/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_hello_endpoint_content_type():
    response = client.get("/api/hello")
    assert response.headers["content-type"] == "application/json"


def test_cors_headers():
    response = client.options("/api/hello")
    assert response.status_code == 200
