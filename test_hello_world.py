#!/usr/bin/env python3
"""
Unit tests for the Hello World Application

This module contains unit tests to verify the functionality
of the hello_world module.
"""

import unittest
from io import StringIO
import sys
import hello_world


class TestHelloWorld(unittest.TestCase):
    """
    Test cases for the Hello World application.
    """

    def test_print_hello_world_output(self):
        """
        Test that print_hello_world() outputs the correct message.
        """
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        # Call the function
        hello_world.print_hello_world()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Verify output
        self.assertEqual(captured_output.getvalue().strip(), "Hello, World!")

    def test_main_returns_success_code(self):
        """
        Test that main() returns success exit code (0).
        """
        # Capture stdout to avoid cluttering test output
        captured_output = StringIO()
        sys.stdout = captured_output
        
        # Call main and verify return code
        exit_code = hello_world.main()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Verify exit code is 0 (success)
        self.assertEqual(exit_code, 0)

    def test_main_produces_output(self):
        """
        Test that main() produces output.
        """
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        # Call main
        hello_world.main()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Verify that output was produced
        self.assertTrue(len(captured_output.getvalue()) > 0)
        self.assertIn("Hello", captured_output.getvalue())


if __name__ == "__main__":
    unittest.main()