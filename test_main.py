from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_generate_missing_fields():
    response = client.post("/generate", json={"repo": "test"})
    assert response.status_code == 422

def test_generate_empty_fields():
    response = client.post("/generate", json={
        "repo": "",
        "branch": "",
        "requirements": ""
    })
    assert response.status_code == 400

@patch('httpx.AsyncClient.post')
def test_generate_success(mock_post):
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "message": "Generated",
        "files_changed": ["main.py", "test.py"]
    }
    mock_response.raise_for_status = AsyncMock()
    mock_post.return_value = mock_response
    
    response = client.post("/generate", json={
        "repo": "git@github.com:test/repo.git",
        "branch": "main",
        "requirements": "Add hello world"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["files_changed"]) == 2

@patch('httpx.AsyncClient.post')
def test_generate_llm_error(mock_post):
    mock_post.side_effect = Exception("LLM failed")
    
    response = client.post("/generate", json={
        "repo": "git@github.com:test/repo.git",
        "branch": "main",
        "requirements": "Add hello world"
    })
    assert response.status_code == 500
    assert "Internal error" in response.json()["detail"]