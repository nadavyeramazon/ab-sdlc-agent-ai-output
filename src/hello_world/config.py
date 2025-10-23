"""Configuration management for the Hello World application.

This module handles all configuration-related functionality including loading,
validation, and access to configuration settings.
"""

import os
import json
from typing import Dict, Any, Optional
import logging
from .exceptions import ConfigError

logger = logging.getLogger(__name__)

class Config:
    """Configuration manager for the Hello World application.
    
    This class handles loading and validating configuration settings from
    environment variables and/or configuration files.
    
    Attributes:
        DEFAULT_GREETING (str): The default greeting message if none is specified.
        ENV_PREFIX (str): Prefix for environment variables.
        config (Dict[str, Any]): The loaded configuration settings.
    """

    DEFAULT_GREETING = "Hello, World!"
    ENV_PREFIX = "HELLO_WORLD_"

    def __init__(self) -> None:
        """Initialize the configuration manager with default settings."""
        self.config: Dict[str, Any] = {
            "greeting": self.DEFAULT_GREETING,
            "log_level": "INFO",
            "log_format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "output_encoding": "utf-8"
        }
        logger.debug("Initialized configuration with defaults: %s", self.config)

    def load_from_env(self) -> None:
        """Load configuration from environment variables.
        
        Environment variables should be prefixed with HELLO_WORLD_.
        For example: HELLO_WORLD_GREETING="Hi!"
        
        Raises:
            ConfigError: If environment variable has invalid format or value.
        """
        logger.debug("Loading configuration from environment variables")
        for env_var in os.environ:
            if env_var.startswith(self.ENV_PREFIX):
                key = env_var[len(self.ENV_PREFIX):].lower()
                value = os.environ[env_var]
                try:
                    self._validate_config_value(key, value)
                    self.config[key] = value
                    logger.debug("Loaded config from env: %s = %s", key, value)
                except ValueError as e:
                    raise ConfigError(str(e), key) from e

    def load_from_file(self, file_path: str) -> None:
        """Load configuration from a JSON file.
        
        Args:
            file_path: Path to the JSON configuration file.
            
        Raises:
            ConfigError: If file cannot be read or has invalid format.
        """
        logger.debug("Loading configuration from file: %s", file_path)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                file_config = json.load(f)
                for key, value in file_config.items():
                    self._validate_config_value(key, value)
                    self.config[key] = value
                logger.debug("Loaded configuration from file: %s", self.config)
        except (json.JSONDecodeError, IOError) as e:
            raise ConfigError(f"Failed to load config file: {str(e)}", file_path) from e

    def _validate_config_value(self, key: str, value: Any) -> None:
        """Validate a configuration value.
        
        Args:
            key: The configuration key.
            value: The value to validate.
            
        Raises:
            ValueError: If the value is invalid for the given key.
        """
        if key == "log_level":
            valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
            if value.upper() not in valid_levels:
                raise ValueError(f"Invalid log level. Must be one of: {valid_levels}")
        elif key == "output_encoding":
            if value.lower() not in ["utf-8", "ascii"]:
                raise ValueError("Output encoding must be 'utf-8' or 'ascii'")
        elif key == "greeting":
            if not isinstance(value, str) or len(value.strip()) == 0:
                raise ValueError("Greeting must be a non-empty string")

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value.
        
        Args:
            key: The configuration key to retrieve.
            default: Default value if key doesn't exist.
            
        Returns:
            The configuration value or default if not found.
        """
        return self.config.get(key, default)
