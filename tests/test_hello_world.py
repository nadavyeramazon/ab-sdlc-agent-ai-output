import fastapi
from fastapi.testclient import TestClient
from hello_world import app

client = TestClient(app)

def test_read_root():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'Hello': 'World'}