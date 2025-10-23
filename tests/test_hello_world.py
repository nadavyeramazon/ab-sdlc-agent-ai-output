import pytest
import os
from unittest.mock import patch, MagicMock
from typing import Dict, Any
from hello_world.main import main, process_message, validate_input, MAX_MESSAGE_LENGTH
from hello_world.config import load_config, validate_config
from hello_world.logger import setup_logger, set_log_level

# Test configuration
@pytest.fixture
def valid_config() -> Dict[str, Any]:
    return {
        'message_prefix': '[Test] ',
        'message_suffix': ' !',
        'logging': {
            'level': 'INFO',
            'file': 'app.log',
            'max_size': 5242880,
            'backup_count': 5
        }
    }

def test_validate_input_valid():
    """Test input validation with valid message."""
    validate_input("Hello, World!")

def test_validate_input_too_long():
    """Test input validation with message exceeding max length."""
    with pytest.raises(ValueError, match=f"Message length exceeds maximum of {MAX_MESSAGE_LENGTH} characters"):
        validate_input("x" * (MAX_MESSAGE_LENGTH + 1))

def test_validate_input_invalid_chars():
    """Test input validation with invalid characters."""
    with pytest.raises(ValueError, match="Message contains invalid characters"):
        validate_input("Hello\x00World")

def test_process_message(valid_config):
    """Test message processing with configuration."""
    result = process_message("Hello", valid_config)
    assert result == "[Test] Hello !"

def test_process_message_validation(valid_config):
    """Test message processing with invalid input."""
    with pytest.raises(ValueError):
        process_message("x" * (MAX_MESSAGE_LENGTH + 1), valid_config)

def test_config_validation(valid_config):
    """Test configuration validation."""
    validate_config(valid_config)

def test_config_validation_invalid_type():
    """Test configuration validation with invalid type."""
    with pytest.raises(ValueError, match="Configuration must be a dictionary"):
        validate_config([])

def test_config_validation_missing_log_keys():
    """Test configuration validation with missing logging keys."""
    invalid_config = {'logging': {}}
    with pytest.raises(ValueError, match="Missing required logging configuration key"):
        validate_config(invalid_config)

def test_config_validation_invalid_log_values():
    """Test configuration validation with invalid logging values."""
    invalid_config = {
        'logging': {
            'level': 'INFO',
            'file': 'app.log',
            'max_size': -1,
            'backup_count': 5
        }
    }
    with pytest.raises(ValueError, match="Log max_size must be a positive integer"):
        validate_config(invalid_config)

def test_logger_setup():
    """Test logger setup and configuration."""
    logger = setup_logger("test_logger")
    assert logger.name == "test_logger"
    assert logger.level == logging.INFO
    assert len(logger.handlers) == 2  # Console and file handlers

def test_logger_level_setting():
    """Test log level configuration."""
    logger = setup_logger("test_logger")
    set_log_level(logger, "DEBUG")
    assert logger.level == logging.DEBUG

def test_logger_invalid_level():
    """Test setting invalid log level."""
    logger = setup_logger("test_logger")
    with pytest.raises(ValueError, match="Invalid log level"):
        set_log_level(logger, "INVALID")

def test_main_success(valid_config, tmp_path):
    """Test main function success path."""
    config_file = tmp_path / "config.yaml"
    with open(config_file, 'w') as f:
        yaml.dump(valid_config, f)

    with patch('sys.argv', ['main.py', '--config', str(config_file)]):
        assert main() == 0

def test_main_file_not_found():
    """Test main function with missing config file."""
    with patch('sys.argv', ['main.py', '--config', 'nonexistent.yaml']):
        assert main() == 1

def test_main_validation_error(tmp_path):
    """Test main function with invalid configuration."""
    config_file = tmp_path / "invalid_config.yaml"
    with open(config_file, 'w') as f:
        yaml.dump([], f)

    with patch('sys.argv', ['main.py', '--config', str(config_file)]):
        assert main() == 1
