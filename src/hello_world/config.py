"""Configuration module for Hello World application."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class LogConfig:
    """Configuration for logging.
    
    Args:
        log_file: Path to the log file
        max_bytes: Maximum size of log file before rotation (must be positive)
        backup_count: Number of backup files to keep (must be non-negative)
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Raises:
        ValueError: If max_bytes is not positive or backup_count is negative
    """
    log_file: str
    max_bytes: int
    backup_count: int
    log_level: str = 'INFO'

    def __post_init__(self) -> None:
        """Validate configuration parameters.
        
        Returns:
            None
            
        Raises:
            ValueError: If parameters are invalid
        """
        if not self.log_file.strip():
            raise ValueError('Log file path cannot be empty')
            
        if self.max_bytes <= 0:
            raise ValueError('max_bytes must be positive')
            
        if self.backup_count < 0:
            raise ValueError('backup_count cannot be negative')
            
        valid_levels = {'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}
        if self.log_level not in valid_levels:
            raise ValueError(f'Invalid log_level. Must be one of: {", ".join(valid_levels)}')


@dataclass
class AppConfig:
    """Application configuration.
    
    Args:
        message: Message to print (non-empty string)
        log_config: Optional logging configuration
        
    Raises:
        ValueError: If message is empty
    """
    message: str
    log_config: Optional[LogConfig] = None

    def __post_init__(self) -> None:
        """Validate configuration parameters.
        
        Returns:
            None
            
        Raises:
            ValueError: If message is empty
        """
        if not self.message.strip():
            raise ValueError('Message cannot be empty')
