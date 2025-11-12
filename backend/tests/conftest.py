"""Pytest configuration and fixtures for backend tests."""

import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture(scope="session")
def test_client():
    """Create a test client for the FastAPI app that persists across the test session."""
    with TestClient(app) as client:
        yield client


@pytest.fixture
def sample_names():
    """Provide sample names for testing."""
    return [
        "Alice",
        "Bob",
        "Charlie",
        "Diana",
        "José",
        "Maria",
        "John Doe",
        "Anna-Maria",
        "李小明",  # Chinese name
        "محمد",    # Arabic name
    ]


@pytest.fixture
def invalid_names():
    """Provide invalid names for testing."""
    return [
        "",           # Empty string
        "   ",        # Whitespace only
        "\t\n",       # Tabs and newlines
        "a" * 101,    # Too long (101 characters)
        "b" * 150,    # Way too long
    ]


@pytest.fixture
def valid_edge_case_names():
    """Provide edge case valid names for testing."""
    return [
        "A",          # Single character
        "a" * 100,    # Maximum length (100 characters)
        "X Æ A-12",   # Special characters
        "O'Connor",   # Apostrophe
        "Jean-Luc",   # Hyphen
        "Van Der Berg", # Multiple spaces
    ]