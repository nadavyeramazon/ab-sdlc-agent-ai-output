"""Test suite for the Hello World application.

This module contains comprehensive tests for the Hello World
application's core functionality.
"""

import pytest
from src.hello_world import greet


def test_greet_with_default():
    """Test greeting with default parameter."""
    assert greet() == 'Hello, World!'


def test_greet_with_name():
    """Test greeting with a specific name."""
    assert greet('Alice') == 'Hello, Alice!'


def test_greet_with_whitespace_name():
    """Test greeting with whitespace in name."""
    assert greet('  Bob  ') == 'Hello, Bob!'


def test_greet_with_empty_string():
    """Test greeting with empty string raises ValueError."""
    with pytest.raises(ValueError):
        greet('')


def test_greet_with_whitespace_only():
    """Test greeting with whitespace-only string raises ValueError."""
    with pytest.raises(ValueError):
        greet('   ')


def test_greet_with_invalid_type():
    """Test greeting with invalid type raises TypeError."""
    with pytest.raises(TypeError):
        greet(123)


@pytest.mark.parametrize('name,expected', [
    ('World', 'Hello, World!'),
    ('Alice', 'Hello, Alice!'),
    ('  Bob  ', 'Hello, Bob!'),
    ('🌍', 'Hello, 🌍!'),  # Test Unicode support
])
def test_greet_parametrized(name, expected):
    """Parametrized test for greeting with various inputs."""
    assert greet(name) == expected
