"""Unit tests for configuration management."""
import os
import pytest
from src.config import Settings, ConfigurationError

def test_valid_settings():
    """Test valid configuration settings."""
    settings = Settings(
        app_name='Test App',
        debug_mode=True,
        log_level='INFO',
        api_prefix='/api'
    )
    settings.validate()  # Should not raise

def test_invalid_log_level():
    """Test configuration with invalid log level."""
    settings = Settings(
        app_name='Test App',
        debug_mode=True,
        log_level='INVALID',
        api_prefix='/api'
    )
    with pytest.raises(ConfigurationError):
        settings.validate()

def test_empty_app_name():
    """Test configuration with empty app name."""
    settings = Settings(
        app_name='',
        debug_mode=True,
        log_level='INFO',
        api_prefix='/api'
    )
    with pytest.raises(ConfigurationError):
        settings.validate()

def test_invalid_api_prefix():
    """Test configuration with invalid API prefix."""
    settings = Settings(
        app_name='Test App',
        debug_mode=True,
        log_level='INFO',
        api_prefix='api'  # Missing leading slash
    )
    with pytest.raises(ConfigurationError):
        settings.validate()