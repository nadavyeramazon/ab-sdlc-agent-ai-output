"""Pytest configuration and fixtures for backend tests."""

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture(scope="module")
def test_client() -> TestClient:
    """Create a test client for the FastAPI application.
    
    Yields:
        TestClient instance for making test requests
    """
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def test_app():
    """Provide the FastAPI application instance.
    
    Returns:
        FastAPI application instance
    """
    return app
