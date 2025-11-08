from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get('/')
    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.content}")
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert response.json() == {'message': 'Hello, World!'}, f"Expected {{'message': 'Hello, World!'}}, but got {response.json()}"