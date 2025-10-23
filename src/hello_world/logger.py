"""Logging configuration and utilities for the hello_world application."""

from enum import Enum
import logging
import os
from pathlib import Path
from typing import Optional

from hello_world.exceptions import LoggingSetupError

class LogLevel(Enum):
    """Enumeration of available log levels."""
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

def setup_logging(log_dir: str = 'logs',
                 log_level: LogLevel = LogLevel.INFO) -> None:
    """Configure logging for the application.

    Args:
        log_dir: Directory where log files will be stored.
        log_level: Minimum log level to record.

    Raises:
        LoggingSetupError: If there are permission issues creating the log directory
                          or log file.
    """
    try:
        # Create logs directory if it doesn't exist
        Path(log_dir).mkdir(parents=True, exist_ok=True)

        # Configure logging format and handlers
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # File handler
        log_file = Path(log_dir) / 'hello_world.log'
        file_handler = logging.FileHandler(
            str(log_file), encoding='utf-8')
        file_handler.setFormatter(formatter)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # Root logger configuration
        root_logger = logging.getLogger()
        root_logger.setLevel(log_level.value)
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)

    except PermissionError as e:
        raise LoggingSetupError(
            f"Permission denied when setting up logging: {e}") from e
    except Exception as e:
        raise LoggingSetupError(f"Failed to setup logging: {e}") from e
