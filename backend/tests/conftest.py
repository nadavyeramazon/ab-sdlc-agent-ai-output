"""Pytest configuration and shared fixtures."""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture(scope="session")
def test_data():
    """Fixture providing test data for use across tests."""
    return {
        "valid_messages": [
            "Hello, World!",
            "Test message",
            "Special chars: !@#$%",
        ],
        "invalid_messages": [
            "",
            "   ",
            "\t\n",
        ],
    }


@pytest.fixture
def sample_message_request():
    """Fixture providing a sample message request."""
    return {"message": "Test message from fixture"}
