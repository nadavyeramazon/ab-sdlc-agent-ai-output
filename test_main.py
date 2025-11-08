from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'Hello, World!'}

def test_read_root_content_type():
    response = client.get('/')
    assert response.headers['Content-Type'] == 'application/json'

def test_read_root_not_found():
    response = client.get('/non-existent-path')
    assert response.status_code == 404

def test_read_root_method_not_allowed():
    response = client.post('/')
    assert response.status_code == 405
