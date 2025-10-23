"""Test suite for Hello World application."""
import logging
import os
import tempfile
from pathlib import Path
from unittest import TestCase, mock

from hello_world.config import AppConfig, LogConfig
from hello_world.logger import setup_logger
from hello_world.main import main, parse_args


class TestHelloWorld(TestCase):
    """Test cases for Hello World application."""
    
    def setUp(self) -> None:
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.log_file = os.path.join(self.temp_dir, 'test.log')
    
    def test_parse_args_minimal(self) -> None:
        """Test parsing minimal command line arguments."""
        app_config, log_config = parse_args(['Hello, World!'])
        self.assertEqual(app_config.message, 'Hello, World!')
        self.assertIsNone(log_config)
    
    def test_parse_args_with_logging(self) -> None:
        """Test parsing arguments with logging configuration."""
        app_config, log_config = parse_args([
            'Hello, World!',
            '--log-file', self.log_file,
            '--log-max-bytes', '2048',
            '--log-backup-count', '5',
            '--log-level', 'DEBUG'
        ])
        
        self.assertEqual(app_config.message, 'Hello, World!')
        self.assertIsNotNone(log_config)
        assert log_config is not None  # for type checking
        self.assertEqual(log_config.log_file, self.log_file)
        self.assertEqual(log_config.max_bytes, 2048)
        self.assertEqual(log_config.backup_count, 5)
        self.assertEqual(log_config.log_level, 'DEBUG')
    
    def test_empty_message(self) -> None:
        """Test handling of empty message."""
        with self.assertRaises(SystemExit):
            parse_args([""])
            
        with self.assertRaises(SystemExit):
            parse_args(["  "])
    
    def test_invalid_log_config(self) -> None:
        """Test handling of invalid logging configuration."""
        # Negative max_bytes
        with self.assertRaises(SystemExit):
            parse_args([
                'test',
                '--log-file', self.log_file,
                '--log-max-bytes', '-1'
            ])
        
        # Negative backup_count
        with self.assertRaises(SystemExit):
            parse_args([
                'test',
                '--log-file', self.log_file,
                '--log-backup-count', '-1'
            ])
        
        # Invalid log level
        with self.assertRaises(SystemExit):
            parse_args([
                'test',
                '--log-file', self.log_file,
                '--log-level', 'INVALID'
            ])
    
    def test_logger_setup_stderr(self) -> None:
        """Test logger setup without configuration (stderr)."""
        logger = setup_logger()
        self.assertEqual(len(logger.handlers), 1)
        self.assertIsInstance(logger.handlers[0], logging.StreamHandler)
    
    def test_logger_setup_file(self) -> None:
        """Test logger setup with file configuration."""
        config = LogConfig(
            log_file=self.log_file,
            max_bytes=1024,
            backup_count=3
        )
        logger = setup_logger(config)
        
        self.assertEqual(len(logger.handlers), 1)
        handler = logger.handlers[0]
        self.assertIsInstance(handler, logging.handlers.RotatingFileHandler)
        self.assertEqual(handler.baseFilename, self.log_file)
        self.assertEqual(handler.maxBytes, 1024)
        self.assertEqual(handler.backupCount, 3)
    
    def test_logger_setup_unwritable(self) -> None:
        """Test logger setup with unwritable directory."""
        with mock.patch('os.access', return_value=False):
            with self.assertRaises(OSError) as ctx:
                setup_logger(LogConfig(
                    log_file=self.log_file,
                    max_bytes=1024,
                    backup_count=3
                ))
            self.assertIn('not writable', str(ctx.exception))
    
    def test_logger_rotation_failure(self) -> None:
        """Test handling of log rotation failures."""
        config = LogConfig(
            log_file=self.log_file,
            max_bytes=1024,
            backup_count=3
        )
        
        with mock.patch('logging.handlers.RotatingFileHandler.doRollover',
                       side_effect=Exception('Rotation failed')):
            with self.assertRaises(ValueError) as ctx:
                setup_logger(config)
            self.assertIn('Failed to rotate', str(ctx.exception))
    
    def test_main_success(self) -> None:
        """Test successful execution of main function."""
        with mock.patch('builtins.print') as mock_print:
            exit_code = main(['Hello, World!'])
            
        self.assertEqual(exit_code, 0)
        mock_print.assert_called_once_with('Hello, World!')
    
    def test_main_with_logging(self) -> None:
        """Test main function with logging enabled."""
        exit_code = main([
            'Hello, World!',
            '--log-file', self.log_file
        ])
        
        self.assertEqual(exit_code, 0)
        self.assertTrue(os.path.exists(self.log_file))
        with open(self.log_file, 'r', encoding='utf-8') as f:
            log_content = f.read()
        self.assertIn('Hello, World!', log_content)
    
    def test_main_error(self) -> None:
        """Test main function error handling."""
        with mock.patch('hello_world.main.parse_args',
                       side_effect=Exception('Test error')):
            exit_code = main(['test'])
            
        self.assertEqual(exit_code, 1)
    
    def tearDown(self) -> None:
        """Clean up test environment."""
        # Clean up log files
        if os.path.exists(self.temp_dir):
            for file in Path(self.temp_dir).glob('*'):
                file.unlink()
            Path(self.temp_dir).rmdir()
