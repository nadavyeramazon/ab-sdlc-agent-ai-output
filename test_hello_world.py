#!/usr/bin/env python3
"""
Unit tests for the hello_world module.

This module contains comprehensive tests for the hello_world application,
including tests for the greet() function with various parameters,
main() execution, output format validation, and edge cases.
"""

import unittest
from io import StringIO
import sys
import hello_world


class TestGreetFunction(unittest.TestCase):
    """Test cases for the greet() function."""

    def test_greet_default_parameter(self):
        """Test greet() with default parameter (no arguments)."""
        result = hello_world.greet()
        self.assertEqual(result, "Hello, World!")
        self.assertIsInstance(result, str)

    def test_greet_with_custom_name(self):
        """Test greet() with a custom name."""
        result = hello_world.greet("Alice")
        self.assertEqual(result, "Hello, Alice!")

    def test_greet_with_multiple_names(self):
        """Test greet() with multiple different names."""
        names = ["Bob", "Charlie", "David"]
        expected = ["Hello, Bob!", "Hello, Charlie!", "Hello, David!"]
        
        for name, expected_result in zip(names, expected):
            with self.subTest(name=name):
                result = hello_world.greet(name)
                self.assertEqual(result, expected_result)

    def test_greet_output_format(self):
        """Test that greet() output follows the correct format."""
        result = hello_world.greet("Test")
        self.assertTrue(result.startswith("Hello, "))
        self.assertTrue(result.endswith("!"))
        self.assertIn("Test", result)

    def test_greet_with_empty_string(self):
        """Test greet() with an empty string as name."""
        result = hello_world.greet("")
        self.assertEqual(result, "Hello, !")

    def test_greet_with_special_characters(self):
        """Test greet() with names containing special characters."""
        special_names = ["O'Brien", "José", "Marie-Claire", "李明"]
        
        for name in special_names:
            with self.subTest(name=name):
                result = hello_world.greet(name)
                self.assertEqual(result, f"Hello, {name}!")
                self.assertIn(name, result)

    def test_greet_with_long_name(self):
        """Test greet() with a very long name."""
        long_name = "A" * 1000
        result = hello_world.greet(long_name)
        self.assertEqual(result, f"Hello, {long_name}!")

    def test_greet_with_numeric_string(self):
        """Test greet() with numeric strings."""
        result = hello_world.greet("123")
        self.assertEqual(result, "Hello, 123!")

    def test_greet_with_whitespace(self):
        """Test greet() with names containing whitespace."""
        result = hello_world.greet("John Doe")
        self.assertEqual(result, "Hello, John Doe!")
        
        result = hello_world.greet(" SpaceBefore")
        self.assertEqual(result, "Hello,  SpaceBefore!")


class TestMainFunction(unittest.TestCase):
    """Test cases for the main() function."""

    def test_main_execution(self):
        """Test that main() executes without errors."""
        # Capture stdout to prevent output during tests
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            hello_world.main()
        finally:
            sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        self.assertIsNotNone(output)
        self.assertGreater(len(output), 0)

    def test_main_output_contains_hello_world(self):
        """Test that main() output contains 'Hello, World!'."""
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            hello_world.main()
        finally:
            sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        self.assertIn("Hello, World!", output)

    def test_main_output_contains_alice(self):
        """Test that main() output contains greeting for Alice."""
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            hello_world.main()
        finally:
            sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        self.assertIn("Hello, Alice!", output)

    def test_main_output_contains_bob(self):
        """Test that main() output contains greeting for Bob."""
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            hello_world.main()
        finally:
            sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        self.assertIn("Hello, Bob!", output)

    def test_main_output_contains_charlie(self):
        """Test that main() output contains greeting for Charlie."""
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            hello_world.main()
        finally:
            sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        self.assertIn("Hello, Charlie!", output)

    def test_main_output_line_count(self):
        """Test that main() outputs the expected number of lines."""
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            hello_world.main()
        finally:
            sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        lines = output.strip().split('\n')
        # Should have: Hello World + Alice + Bob + Charlie + syntax error message = 5 lines
        self.assertEqual(len(lines), 5)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""

    def test_greet_return_type(self):
        """Test that greet() always returns a string."""
        test_cases = ["", "Test", "123", " ", "Special!@#"]
        
        for test_input in test_cases:
            with self.subTest(input=test_input):
                result = hello_world.greet(test_input)
                self.assertIsInstance(result, str)

    def test_greet_immutability(self):
        """Test that greet() doesn't modify the input."""
        original = "TestName"
        hello_world.greet(original)
        self.assertEqual(original, "TestName")

    def test_module_has_docstring(self):
        """Test that the module has a docstring."""
        self.assertIsNotNone(hello_world.__doc__)
        self.assertGreater(len(hello_world.__doc__), 0)

    def test_greet_function_has_docstring(self):
        """Test that greet() function has a docstring."""
        self.assertIsNotNone(hello_world.greet.__doc__)
        self.assertGreater(len(hello_world.greet.__doc__), 0)

    def test_main_function_has_docstring(self):
        """Test that main() function has a docstring."""
        self.assertIsNotNone(hello_world.main.__doc__)
        self.assertGreater(len(hello_world.main.__doc__), 0)


if __name__ == "__main__":
    unittest.main()
