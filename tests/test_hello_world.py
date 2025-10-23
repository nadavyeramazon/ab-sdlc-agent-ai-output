"""Test suite for the Hello World application."""

import os
import sys
import io
import tempfile
import json
import pytest
from hello_world.main import main, generate_message, create_parser
from hello_world.config import Config
from hello_world.exceptions import ConfigError, ValidationError, LoggingError

def test_version_flag(capsys):
    """Test that --version outputs correct version."""
    with pytest.raises(SystemExit) as e:
        main(['--version'])
    assert e.value.code == 0
    captured = capsys.readouterr()
    assert '1.0.0' in captured.out

def test_help_flag(capsys):
    """Test that --help outputs help message."""
    with pytest.raises(SystemExit) as e:
        main(['--help'])
    assert e.value.code == 0
    captured = capsys.readouterr()
    assert 'usage:' in captured.out
    assert '--version' in captured.out
    assert '--config' in captured.out
    assert '--greeting' in captured.out

def test_default_greeting(capsys):
    """Test default greeting output."""
    assert main([]) == 0
    captured = capsys.readouterr()
    assert captured.out == "Hello, World!\n"

def test_custom_greeting(capsys):
    """Test custom greeting via command line."""
    greeting = "Hi there!"
    assert main(['--greeting', greeting]) == 0
    captured = capsys.readouterr()
    assert captured.out == f"{greeting}\n"

def test_empty_greeting():
    """Test that empty greeting raises error."""
    assert main(['--greeting', '']) == 2

def test_config_file():
    """Test loading configuration from file."""
    config = {
        "greeting": "Greetings from config!",
        "log_level": "DEBUG"
    }
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        json.dump(config, f)
        f.flush()
        try:
            exit_code = main(['--config', f.name])
            assert exit_code == 0
        finally:
            os.unlink(f.name)

def test_invalid_config_file():
    """Test error handling for invalid config file."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("invalid json")
        f.flush()
        try:
            exit_code = main(['--config', f.name])
            assert exit_code == 1
        finally:
            os.unlink(f.name)

def test_environment_variables(monkeypatch):
    """Test loading configuration from environment variables."""
    greeting = "Hi from ENV!"
    monkeypatch.setenv("HELLO_WORLD_GREETING", greeting)
    assert main([]) == 0

def test_invalid_log_level():
    """Test error handling for invalid log level."""
    assert main(['--log-level', 'INVALID']) == 2

def test_generate_message_validation():
    """Test message generation validation."""
    with pytest.raises(ValidationError):
        generate_message("")
    with pytest.raises(ValidationError):
        generate_message(None)
    assert generate_message("Test") == "Test\n"

def test_config_validation():
    """Test configuration validation."""
    config = Config()
    
    # Test invalid log level
    with pytest.raises(ConfigError):
        config._validate_config_value("log_level", "INVALID")
    
    # Test invalid encoding
    with pytest.raises(ConfigError):
        config._validate_config_value("output_encoding", "invalid-encoding")
    
    # Test invalid greeting
    with pytest.raises(ConfigError):
        config._validate_config_value("greeting", "")

def test_argument_parser():
    """Test argument parser configuration."""
    parser = create_parser()
    args = parser.parse_args(['--greeting', 'Test'])
    assert args.greeting == 'Test'
    assert args.log_level is None
    assert args.config is None
