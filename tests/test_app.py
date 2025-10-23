"""Integration tests for the API endpoints."""
import pytest
from fastapi.testclient import TestClient
from src.config import get_settings

def test_greeting_endpoint(app_client: TestClient):
    """Test the greeting endpoint with default name."""
    response = app_client.post(f'{get_settings().api_prefix}/hello')
    assert response.status_code == 200
    data = response.json()
    assert data['message'] == 'Hello, World!'
    assert 'request_id' in data

def test_greeting_with_custom_name(app_client: TestClient):
    """Test the greeting endpoint with custom name."""
    response = app_client.post(
        f'{get_settings().api_prefix}/hello',
        json={'name': 'Alice'}
    )
    assert response.status_code == 200
    data = response.json()
    assert data['message'] == 'Hello, Alice!'
    assert 'request_id' in data

def test_greeting_with_invalid_name(app_client: TestClient):
    """Test the greeting endpoint with invalid name."""
    response = app_client.post(
        f'{get_settings().api_prefix}/hello',
        json={'name': ''}
    )
    assert response.status_code == 422

def test_stats_endpoint(app_client: TestClient):
    """Test the stats endpoint."""
    # Make a greeting request first
    app_client.post(f'{get_settings().api_prefix}/hello')
    
    # Check stats
    response = app_client.get(f'{get_settings().api_prefix}/stats')
    assert response.status_code == 200
    data = response.json()
    assert data['total_requests'] > 0

def test_cors_headers(app_client: TestClient):
    """Test CORS headers are present."""
    response = app_client.options(f'{get_settings().api_prefix}/hello')
    assert response.status_code == 200
    assert 'access-control-allow-origin' in response.headers

def test_process_time_header(app_client: TestClient):
    """Test process time header is added."""
    response = app_client.post(f'{get_settings().api_prefix}/hello')
    assert 'x-process-time' in response.headers