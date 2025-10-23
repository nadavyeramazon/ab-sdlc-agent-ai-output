"""Configuration management for the Hello World service."""
import os
from typing import Optional
from dataclasses import dataclass
from functools import lru_cache

from .exceptions import ConfigurationError

@dataclass
class Settings:
    """Service configuration settings.
    
    Attributes:
        app_name: Name of the application
        debug_mode: Enable debug logging
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        api_prefix: API URL prefix
    """
    app_name: str
    debug_mode: bool
    log_level: str
    api_prefix: str

    def validate(self) -> None:
        """Validate configuration settings.
        
        Raises:
            ConfigurationError: If any settings are invalid
        """
        valid_log_levels = {'DEBUG', 'INFO', 'WARNING', 'ERROR'}
        if self.log_level not in valid_log_levels:
            raise ConfigurationError(f'Invalid log level: {self.log_level}')
        
        if not self.app_name:
            raise ConfigurationError('Application name cannot be empty')
        
        if not self.api_prefix.startswith('/'):
            raise ConfigurationError('API prefix must start with /')

@lru_cache()
def get_settings() -> Settings:
    """Get validated application settings.
    
    Returns:
        Settings: Application configuration

    Raises:
        ConfigurationError: If environment variables are invalid
    """
    settings = Settings(
        app_name=os.getenv('APP_NAME', 'Hello World Service'),
        debug_mode=os.getenv('DEBUG', 'false').lower() == 'true',
        log_level=os.getenv('LOG_LEVEL', 'INFO').upper(),
        api_prefix=os.getenv('API_PREFIX', '/api/v1')
    )
    settings.validate()
    return settings