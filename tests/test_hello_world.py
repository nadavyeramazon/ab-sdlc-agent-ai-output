"""Test suite for the hello_world application."""

import logging
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from hello_world.config import Config
from hello_world.exceptions import LoggingSetupError
from hello_world.logger import LogLevel, setup_logging
from hello_world.main import generate_greeting, main, parse_args

class TestHelloWorld(unittest.TestCase):
    """Test cases for the hello_world application."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        for handler in logging.getLogger().handlers[:]: 
            logging.getLogger().removeHandler(handler)

    def test_generate_greeting_default(self):
        """Test greeting generation with default parameter."""
        self.assertEqual(generate_greeting(), "Hello, World!")

    def test_generate_greeting_custom(self):
        """Test greeting generation with custom name."""
        self.assertEqual(generate_greeting("Alice"), "Hello, Alice!")

    def test_generate_greeting_non_ascii(self):
        """Test greeting generation with non-ASCII characters."""
        self.assertEqual(generate_greeting("José"), "Hello, José!")
        self.assertEqual(generate_greeting("中文"), "Hello, 中文!")
        self.assertEqual(generate_greeting("🌍"), "Hello, 🌍!")

    @patch('argparse.ArgumentParser.parse_args')
    def test_parse_args_default(self, mock_args):
        """Test argument parsing with default values."""
        mock_args.return_value = parse_args()
        args = parse_args()
        self.assertEqual(args.name, "World")
        self.assertIsNone(args.config)

    def test_logging_setup_success(self):
        """Test successful logging setup."""
        log_dir = Path(self.temp_dir) / 'logs'
        setup_logging(str(log_dir), LogLevel.DEBUG)
        self.assertTrue(log_dir.exists())
        self.assertTrue((log_dir / 'hello_world.log').exists())

    @patch('pathlib.Path.mkdir')
    def test_logging_setup_permission_error(self, mock_mkdir):
        """Test logging setup with permission error."""
        mock_mkdir.side_effect = PermissionError("Permission denied")
        with self.assertRaises(LoggingSetupError):
            setup_logging("logs")

    @patch('hello_world.main.print')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_success(self, mock_args, mock_print):
        """Test successful execution of main function."""
        mock_args.return_value = parse_args()
        exit_code = main()
        self.assertEqual(exit_code, 0)
        mock_print.assert_called_once_with("Hello, World!")

    @patch('argparse.ArgumentParser.parse_args')
    def test_main_error(self, mock_args):
        """Test main function error handling."""
        mock_args.side_effect = Exception("Test error")
        exit_code = main()
        self.assertEqual(exit_code, 1)

if __name__ == '__main__':
    unittest.main()
