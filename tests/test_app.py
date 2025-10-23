"""Test suite for the Hello World application.

This module contains comprehensive tests for the Hello World service,
ensuring proper functionality, error handling, and edge cases.
"""

import unittest
from hello_world.app import get_greeting


class TestHelloWorld(unittest.TestCase):
    """Test cases for Hello World application."""

    def test_default_greeting(self) -> None:
        """Test the default greeting without a name parameter."""
        result = get_greeting()
        self.assertEqual(result['message'], 'Hello, World!')

    def test_personalized_greeting(self) -> None:
        """Test greeting with a valid name."""
        result = get_greeting('John')
        self.assertEqual(result['message'], 'Hello, John!')

    def test_greeting_with_whitespace(self) -> None:
        """Test greeting with name containing whitespace."""
        result = get_greeting('  John Doe  ')
        self.assertEqual(result['message'], 'Hello, John Doe!')

    def test_empty_name(self) -> None:
        """Test handling of empty name."""
        with self.assertRaises(ValueError):
            get_greeting('')
        with self.assertRaises(ValueError):
            get_greeting('   ')

    def test_invalid_name_type(self) -> None:
        """Test handling of invalid name type."""
        with self.assertRaises(TypeError):
            get_greeting(123)  # type: ignore

    def test_invalid_characters(self) -> None:
        """Test handling of invalid characters in name."""
        with self.assertRaises(ValueError):
            get_greeting('John@Doe')


if __name__ == '__main__':
    unittest.main()
