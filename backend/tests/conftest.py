"""Pytest configuration and fixtures for backend tests."""

import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture(scope="session")
def test_app():
    """
    Provides the FastAPI application instance for testing.
    
    Scope: session - Created once per test session.
    """
    return app


@pytest.fixture(scope="function")
def client(test_app):
    """
    Provides a FastAPI TestClient for making API requests.
    
    Scope: function - Fresh client for each test function.
    
    Usage:
        def test_endpoint(client):
            response = client.get("/api/hello")
            assert response.status_code == 200
    """
    with TestClient(test_app) as test_client:
        yield test_client


@pytest.fixture(scope="function")
def mock_datetime(monkeypatch):
    """
    Provides a mock datetime for consistent timestamp testing.
    
    Usage:
        def test_with_mock_time(client, mock_datetime):
            mock_datetime("2024-01-15T10:30:45.123456")
            response = client.get("/api/hello")
            assert "2024-01-15" in response.json()["timestamp"]
    """
    from datetime import datetime
    
    def _mock_datetime(iso_string):
        class MockDateTime:
            @staticmethod
            def utcnow():
                return datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
            
            def __getattr__(self, name):
                return getattr(datetime, name)
        
        monkeypatch.setattr("main.datetime", MockDateTime())
    
    return _mock_datetime


@pytest.fixture(scope="function")
def api_headers():
    """
    Provides standard API request headers.
    
    Returns:
        dict: Standard headers for API requests
    """
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
