"""
Pytest configuration and fixtures.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(scope="module")
def test_client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture(scope="function")
def clean_tasks_db():
    """Clean the tasks database before and after each test."""
    from app.api.v1.endpoints.tasks import tasks_db
    tasks_db.clear()
    yield
    tasks_db.clear()
