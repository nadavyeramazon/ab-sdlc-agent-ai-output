"""Test fixtures and configuration."""
import pytest
from fastapi.testclient import TestClient
from src.app import create_app
from src.services import HelloWorldService

@pytest.fixture
def app_client():
    """Create test client.
    
    Returns:
        TestClient: FastAPI test client
    """
    app = create_app()
    return TestClient(app)

@pytest.fixture
def service():
    """Create HelloWorldService instance.
    
    Returns:
        HelloWorldService: Service instance
    """
    return HelloWorldService()