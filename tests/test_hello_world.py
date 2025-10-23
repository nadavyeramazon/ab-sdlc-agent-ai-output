import pytest
from src.hello_world import HelloWorld

@pytest.fixture
def hello_world():
    """Fixture that provides a HelloWorld instance."""
    return HelloWorld()

def test_default_greeting(hello_world):
    """Test the default greeting without a name."""
    assert hello_world.greet() == "Hello, World!"

def test_custom_greeting(hello_world):
    """Test greeting with a custom name."""
    assert hello_world.greet("John") == "Hello, John!"

def test_greeting_with_spaces(hello_world):
    """Test greeting with a name containing spaces."""
    assert hello_world.greet("John Doe") == "Hello, John Doe!"

def test_invalid_name(hello_world):
    """Test greeting with invalid name characters."""
    with pytest.raises(ValueError):
        hello_world.greet("John@Doe#")

def test_empty_name(hello_world):
    """Test greeting with empty name should return default greeting."""
    assert hello_world.greet("") == "Hello, !"

def test_none_name(hello_world):
    """Test greeting with None should return default greeting."""
    assert hello_world.greet(None) == "Hello, World!"
