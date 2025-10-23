"""
Test Suite for Hello World Application

This module contains comprehensive tests for the Hello World application.
Target: >90% test coverage.

Author: AI Agent
Version: 1.0
"""

import unittest
import logging
from src.main import HelloWorld
from src.logger import setup_logger

class TestHelloWorld(unittest.TestCase):
    """Test cases for HelloWorld class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.hello = HelloWorld()
        # Suppress logging during tests
        logging.getLogger('src.main').setLevel(logging.ERROR)

    def test_default_greeting(self):
        """Test greeting with default name."""
        self.assertEqual(self.hello.greet(), 'Hello, World!')

    def test_custom_greeting(self):
        """Test greeting with custom name."""
        self.assertEqual(self.hello.greet('Test'), 'Hello, Test!')

    def test_custom_default_name(self):
        """Test custom default name in constructor."""
        hello = HelloWorld(default_name='Custom')
        self.assertEqual(hello.greet(), 'Hello, Custom!')

    def test_empty_name(self):
        """Test greeting with empty string name."""
        self.assertEqual(self.hello.greet(''), 'Hello, !')

class TestLogger(unittest.TestCase):
    """Test cases for logger configuration."""

    def test_logger_setup(self):
        """Test logger initialization and configuration."""
        logger = setup_logger('test')
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.level, logging.INFO)

    def test_logger_custom_level(self):
        """Test logger with custom log level."""
        logger = setup_logger('test', logging.DEBUG)
        self.assertEqual(logger.level, logging.DEBUG)

if __name__ == '__main__':
    unittest.main()