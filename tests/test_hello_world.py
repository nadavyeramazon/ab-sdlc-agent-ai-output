"""Test suite for the Hello World application.

Provides comprehensive testing of all functionality.
"""

import os
import pytest
from unittest.mock import patch
from hello_world.main import create_greeting, validate_name, main, parse_args
from hello_world.logger import HelloWorldLogger
from hello_world.config import AppConfig, get_config

# Test input validation
def test_validate_name_valid():
    """Test that valid names pass validation."""
    assert validate_name('John') is True
    assert validate_name('Mary Jane') is True

def test_validate_name_empty():
    """Test that empty names are rejected."""
    with pytest.raises(ValueError, match='Name cannot be empty'):
        validate_name('')

def test_validate_name_whitespace():
    """Test that whitespace-only names are rejected."""
    with pytest.raises(ValueError, match='Name cannot be only whitespace'):
        validate_name('   ')

def test_validate_name_too_long():
    """Test that overly long names are rejected."""
    config = get_config()
    long_name = 'a' * (config.max_name_length + 1)
    with pytest.raises(ValueError, match='Name length exceeds maximum'):
        validate_name(long_name)

def test_validate_name_invalid_chars():
    """Test that names with invalid characters are rejected."""
    with pytest.raises(ValueError, match='Name contains invalid characters'):
        validate_name('John\x00Doe')

# Test greeting creation
def test_create_greeting_success():
    """Test successful greeting creation."""
    assert create_greeting('World') == 'Hello, World!'
    assert create_greeting('John Doe') == 'Hello, John Doe!'

def test_create_greeting_validation_error():
    """Test greeting creation with invalid input."""
    with pytest.raises(ValueError):
        create_greeting('')

# Test argument parsing
def test_parse_args_valid():
    """Test parsing of valid command line arguments."""
    args = parse_args(['--name', 'World'])
    assert args.name == 'World'

def test_parse_args_missing_name():
    """Test parsing with missing required argument."""
    with pytest.raises(SystemExit):
        parse_args([])

# Test main function
def test_main_success():
    """Test successful execution of main function."""
    with patch('builtins.print') as mock_print:
        exit_code = main(['--name', 'World'])
        assert exit_code == 0
        mock_print.assert_called_once_with('Hello, World!')

def test_main_validation_error():
    """Test main function with invalid input."""
    with patch('builtins.print') as mock_print:
        exit_code = main(['--name', ''])
        assert exit_code == 1
        mock_print.assert_called_once()

# Test logger
def test_logger_singleton():
    """Test that logger follows singleton pattern."""
    logger1 = HelloWorldLogger()
    logger2 = HelloWorldLogger()
    assert logger1 is logger2

def test_logger_rotation(tmp_path):
    """Test log file rotation."""
    # Set up temporary log directory
    log_dir = tmp_path / 'logs'
    log_dir.mkdir()
    
    with patch.dict(os.environ, {'HELLO_WORLD_LOG_DIR': str(log_dir)}):
        logger = HelloWorldLogger()
        
        # Generate enough logs to trigger rotation
        large_message = 'x' * 1024 * 512  # 512KB
        for _ in range(3):  # Should create multiple log files
            logger.info(large_message)
        
        # Check that multiple log files exist
        log_files = list(log_dir.glob('hello_world.log*'))
        assert len(log_files) > 1

# Test configuration
def test_config_from_env():
    """Test configuration loading from environment variables."""
    with patch.dict(os.environ, {
        'HELLO_WORLD_LOG_LEVEL': 'DEBUG',
        'HELLO_WORLD_LOG_DIR': '/custom/logs',
        'HELLO_WORLD_MAX_NAME_LENGTH': '50'
    }):
        config = AppConfig.from_env()
        assert config.log_level == 'DEBUG'
        assert config.log_dir == '/custom/logs'
        assert config.max_name_length == 50

def test_config_singleton():
    """Test that configuration follows singleton pattern."""
    config1 = get_config()
    config2 = get_config()
    assert config1 is config2
