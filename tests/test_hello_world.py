"""Test suite for Hello World application."""

import logging
import pytest
from unittest.mock import patch

from hello_world.config import Config
from hello_world.exceptions import NetworkTimeoutError
from hello_world.main import main, validate_external_service

def test_successful_execution(caplog, capsys):
    """Test successful execution of the application."""
    with patch('hello_world.main.validate_external_service'):
        main()
        
    captured = capsys.readouterr()
    assert captured.out.strip() == "Hello, World!"
    assert "Successfully printed greeting" in caplog.text

def test_network_timeout():
    """Test handling of network timeout."""
    config = Config()
    
    with patch('urllib.request.urlopen') as mock_urlopen:
        mock_urlopen.side_effect = TimeoutError()
        
        with pytest.raises(NetworkTimeoutError):
            validate_external_service(config.request_timeout)

def test_logging_rotation(tmp_path):
    """Test log file rotation configuration."""
    log_file = tmp_path / "test.log"
    config = Config(
        log_file=str(log_file),
        log_max_bytes=1024,
        log_backup_count=2
    )
    
    with patch('hello_world.main.validate_external_service'):
        main()
    
    assert log_file.exists()

def test_config_from_dict():
    """Test configuration creation from dictionary."""
    config_dict = {
        "log_level": "DEBUG",
        "request_timeout": 10.0
    }
    config = Config.from_dict(config_dict)
    
    assert config.log_level == "DEBUG"
    assert config.request_timeout == 10.0