"""Logging configuration and utilities for the Hello World application.

This module provides a configured logger with rotation and proper formatting.
"""

from __future__ import annotations

import logging
import logging.handlers
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union, Dict, Any

@dataclass
class LogConfig:
    """Configuration for the logger.

    Attributes:
        log_level: The logging level (DEBUG, INFO, etc.)
        log_file: Path to the log file
        max_bytes: Maximum size of log file before rotation
        backup_count: Number of backup files to keep
        format: Log message format string
    """
    log_level: str
    log_file: Union[str, Path]
    max_bytes: int = 1024 * 1024  # 1MB default
    backup_count: int = 3
    format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    def validate(self) -> None:
        """Validate the configuration parameters.

        Raises:
            ValueError: If any configuration parameter is invalid
        """
        valid_levels = {'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}
        if self.log_level.upper() not in valid_levels:
            raise ValueError(f'Invalid log level: {self.log_level}. Must be one of {valid_levels}')
        
        if self.max_bytes <= 0:
            raise ValueError(f'max_bytes must be positive, got {self.max_bytes}')
            
        if self.backup_count < 0:
            raise ValueError(f'backup_count must be non-negative, got {self.backup_count}')

def setup_logger(
    name: str,
    config: LogConfig
) -> logging.Logger:
    """Set up and configure a logger instance.

    Args:
        name: The logger name
        config: Logger configuration parameters

    Returns:
        logging.Logger: Configured logger instance

    Raises:
        ValueError: If configuration parameters are invalid
        OSError: If log file directory cannot be created/accessed
    """
    # Validate configuration
    config.validate()
    
    # Ensure log directory exists
    log_path = Path(config.log_file)
    log_dir = log_path.parent
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        raise OSError(f'Failed to create log directory {log_dir}: {e}') from e

    # Configure logger
    logger = logging.getLogger(name)
    logger.setLevel(config.log_level.upper())

    # Clear any existing handlers
    logger.handlers = []

    # Create handlers
    try:
        file_handler = logging.handlers.RotatingFileHandler(
            filename=str(config.log_file),
            maxBytes=config.max_bytes,
            backupCount=config.backup_count,
            encoding='utf-8'
        )
        console_handler = logging.StreamHandler()

        # Create formatter
        formatter = logging.Formatter(config.format)

        # Set formatter for both handlers
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    except Exception as e:
        raise RuntimeError(f'Failed to configure logger: {e}') from e

    return logger
