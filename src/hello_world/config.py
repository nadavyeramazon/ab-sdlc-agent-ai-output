"""Configuration management for the Hello World application.

Provides centralized configuration handling with environment variable support.
"""

import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class AppConfig:
    """Application configuration settings.

    Attributes:
        log_level: Logging level (default: INFO)
        log_dir: Directory for log files (default: logs)
        max_name_length: Maximum allowed length for name input
    """
    log_level: str = 'INFO'
    log_dir: str = 'logs'
    max_name_length: int = 100

    @classmethod
    def from_env(cls) -> 'AppConfig':
        """Create configuration from environment variables.

        Returns:
            AppConfig: Configuration instance with values from environment.
        """
        return cls(
            log_level=os.getenv('HELLO_WORLD_LOG_LEVEL', 'INFO'),
            log_dir=os.getenv('HELLO_WORLD_LOG_DIR', 'logs'),
            max_name_length=int(os.getenv('HELLO_WORLD_MAX_NAME_LENGTH', '100'))
        )

_config_instance: Optional[AppConfig] = None

def get_config() -> AppConfig:
    """Get the application configuration singleton.

    Returns:
        AppConfig: The application configuration instance.
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = AppConfig.from_env()
    return _config_instance
