from typing import Dict, Any, Optional
import json
from pathlib import Path

from .exceptions import ConfigurationError

class Config:
    """Configuration management for the Hello World application.

    Handles loading, validation, and access to configuration settings.
    """

    REQUIRED_FIELDS = {'default_message'}
    OPTIONAL_FIELDS = {'timeout', 'log_level', 'log_file'}
    
    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize configuration.

        Args:
            config: Configuration dictionary

        Raises:
            ConfigurationError: If config is not a dictionary
        """
        if not isinstance(config, dict):
            raise ConfigurationError(f"Config must be a dictionary, got {type(config)}")
        self._config = config

    @classmethod
    def from_file(cls, path: Path) -> 'Config':
        """Load configuration from a JSON file.

        Args:
            path: Path to configuration file

        Returns:
            Config: Configuration instance

        Raises:
            ConfigurationError: If file reading or JSON parsing fails
        """
        try:
            with path.open('r', encoding='utf-8') as f:
                config = json.load(f)
            return cls(config)
        except json.JSONDecodeError as e:
            raise ConfigurationError(f"Invalid JSON in config file: {str(e)}")
        except IOError as e:
            raise ConfigurationError(f"Failed to read config file: {str(e)}")

    @classmethod
    def default(cls) -> 'Config':
        """Create default configuration.

        Returns:
            Config: Default configuration instance
        """
        return cls({
            'default_message': 'Hello, World!',
            'timeout': 5,
            'log_level': 'INFO',
            'log_file': None
        })

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value.

        Args:
            key: Configuration key
            default: Default value if key doesn't exist

        Returns:
            Any: Configuration value or default
        """
        return self._config.get(key, default)

    def validate(self) -> Dict[str, Any]:
        """Validate configuration.

        Returns:
            Dict[str, Any]: Validated configuration dictionary

        Raises:
            ConfigurationError: If validation fails
        """
        # Check required fields
        missing = self.REQUIRED_FIELDS - set(self._config.keys())
        if missing:
            raise ConfigurationError(f"Missing required configuration fields: {missing}")

        # Validate specific fields
        config = self._config.copy()
        
        # Validate default_message
        msg = config['default_message']
        if not isinstance(msg, str) or not msg.strip():
            raise ConfigurationError("default_message must be a non-empty string")

        # Validate timeout
        timeout = config.get('timeout', 5)
        if not isinstance(timeout, (int, float)) or timeout <= 0:
            raise ConfigurationError("timeout must be a positive number")

        # Validate log_level
        log_level = config.get('log_level', 'INFO')
        valid_levels = {'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}
        if log_level not in valid_levels:
            raise ConfigurationError(f"log_level must be one of: {valid_levels}")

        # Validate log_file if present
        log_file = config.get('log_file')
        if log_file is not None:
            if not isinstance(log_file, str):
                raise ConfigurationError("log_file must be a string or null")
            try:
                path = Path(log_file)
                if not path.parent.exists():
                    path.parent.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                raise ConfigurationError(f"Invalid log_file path: {str(e)}")

        return config
