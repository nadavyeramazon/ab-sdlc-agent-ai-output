"""Logging configuration for the Hello World application.

Implements a thread-safe singleton logger with rotation functionality.
"""

import logging
import logging.handlers
import os
from typing import Optional

class HelloWorldLogger:
    _instance: Optional['HelloWorldLogger'] = None
    _logger: Optional[logging.Logger] = None

    def __new__(cls) -> 'HelloWorldLogger':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if self._logger is None:
            self._setup_logger()

    def _setup_logger(self) -> None:
        """Configure the logger with rotation and formatting."""
        self._logger = logging.getLogger('hello_world')
        self._logger.setLevel(logging.INFO)

        # Create logs directory if it doesn't exist
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # File handler with rotation
        file_handler = logging.handlers.RotatingFileHandler(
            filename=os.path.join(log_dir, 'hello_world.log'),
            maxBytes=1024 * 1024,  # 1MB
            backupCount=5,
            encoding='utf-8'
        )

        # Console handler
        console_handler = logging.StreamHandler()

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        self._logger.addHandler(file_handler)
        self._logger.addHandler(console_handler)

    @property
    def logger(self) -> logging.Logger:
        """Get the configured logger instance.

        Returns:
            logging.Logger: The configured logger instance.
        """
        return self._logger

    def info(self, message: str) -> None:
        """Log an info message.

        Args:
            message: The message to log.
        """
        self.logger.info(message)

    def error(self, message: str) -> None:
        """Log an error message.

        Args:
            message: The message to log.
        """
        self.logger.error(message)

    def debug(self, message: str) -> None:
        """Log a debug message.

        Args:
            message: The message to log.
        """
        self.logger.debug(message)

    def warning(self, message: str) -> None:
        """Log a warning message.

        Args:
            message: The message to log.
        """
        self.logger.warning(message)
