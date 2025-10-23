"""Unit tests for service layer."""

import pytest
from src.services import HelloWorldService

def test_hello_service_returns_message():
    """Test HelloWorldService returns correct message."""
    service = HelloWorldService()
    message = service.get_message()
    assert message == "Hello, World!"

def test_hello_service_with_empty_message():
    """Test HelloWorldService handles empty message case."""
    service = HelloWorldService()
    service._message = ""
    with pytest.raises(ValueError):
        service.get_message()
