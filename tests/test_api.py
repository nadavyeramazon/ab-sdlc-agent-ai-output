"""Test module for API endpoints."""

from fastapi.testclient import TestClient
import pytest
from src.main import app

client = TestClient(app)

def test_hello_world():
    """Test the hello world endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'Hello, World!'}

def test_health_check():
    """Test the health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {'status': 'healthy', 'version': '1.0.0'}

def test_nonexistent_endpoint():
    """Test accessing a non-existent endpoint"""
    response = client.get('/nonexistent')
    assert response.status_code == 404