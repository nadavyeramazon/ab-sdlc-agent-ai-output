"""Logging configuration module.

This module provides logging configuration for the Hello World application,
including both console and rotating file handlers.

Example:
    >>> from utils.logging_config import setup_logging
    >>> logger = setup_logging()
    >>> logger.info('Application started')
"""

import logging
import logging.handlers
import os
from pathlib import Path
from typing import Optional


def setup_logging(
    log_level: int = logging.INFO,
    log_format: Optional[str] = None,
    log_file: Optional[str] = None
) -> logging.Logger:
    """Configure application logging with console and file handlers.

    Args:
        log_level: The logging level to use. Defaults to logging.INFO.
        log_format: Custom log format string. If None, uses default format.
        log_file: Custom log file path. If None, uses default path.

    Returns:
        logging.Logger: Configured logger instance.

    Raises:
        OSError: If log directory creation fails or file is not writable.
    """
    if log_format is None:
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    formatter = logging.Formatter(log_format)
    
    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Clear any existing handlers
    logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler with rotation
    if log_file is None:
        log_dir = Path('logs')
        log_file = log_dir / 'hello_world.log'

    try:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        file_handler = logging.handlers.RotatingFileHandler(
            filename=log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
    except OSError as e:
        logger.error(f'Failed to configure file logging: {e}')
        raise

    logger.debug('Logging configured successfully')
    return logger
