"""Test suite for Hello World application."""

import io
import logging
import sys
from unittest.mock import patch

import pytest

from hello_world.main import main, parse_args
from hello_world.logger import get_logger

def test_main_success(capsys):
    """Test successful execution of main function."""
    exit_code = main([])
    captured = capsys.readouterr()
    
    assert exit_code == 0
    assert captured.out == 'Hello World!\n'

def test_version_flag():
    """Test --version flag."""
    with pytest.raises(SystemExit) as exc_info:
        parse_args(['--version'])
    assert exc_info.value.code == 0

def test_help_flag():
    """Test --help flag."""
    with pytest.raises(SystemExit) as exc_info:
        parse_args(['--help'])
    assert exc_info.value.code == 0

def test_main_error_handling():
    """Test error handling in main function."""
    with patch('hello_world.main.parse_args', side_effect=Exception('Test error')):
        exit_code = main([])
        assert exit_code == 1

def test_logger_configuration():
    """Test logger configuration and output."""
    logger = get_logger('test_logger')
    
    assert logger.level == logging.INFO
    assert len(logger.handlers) == 1
    assert isinstance(logger.handlers[0], logging.StreamHandler)

def test_logger_output():
    """Test logger output format."""
    log_output = io.StringIO()
    handler = logging.StreamHandler(log_output)
    logger = get_logger('test_output')
    logger.handlers = [handler]  # Replace handlers
    
    logger.info('Test message')
    output = log_output.getvalue()
    
    assert 'test_output' in output
    assert 'INFO' in output
    assert 'Test message' in output
