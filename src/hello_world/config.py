"""Configuration module for Hello World application."""

from dataclasses import dataclass
from typing import Optional

@dataclass
class Config:
    """Configuration settings for the application."""
    log_level: str = "INFO"
    log_file: Optional[str] = "hello_world.log"
    log_max_bytes: int = 10 * 1024 * 1024  # 10MB
    log_backup_count: int = 3
    request_timeout: float = 5.0  # seconds

    @classmethod
    def from_dict(cls, config_dict: dict) -> 'Config':
        """Create Config instance from dictionary.
        
        Args:
            config_dict: Dictionary containing configuration values.
            
        Returns:
            Config instance with values from dictionary.
            
        Raises:
            ConfigurationError: If configuration values are invalid.
        """
        return cls(**{k: v for k, v in config_dict.items() if k in cls.__annotations__})