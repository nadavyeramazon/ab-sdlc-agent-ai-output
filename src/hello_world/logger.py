"""Logging configuration for the Hello World application.

This module sets up logging with appropriate handlers, formatters,
and configuration options.
"""

import logging
import sys
from typing import Optional
from .exceptions import LoggingError

def setup_logging(
    level: str = "INFO",
    format_string: Optional[str] = None,
    output_file: Optional[str] = None
) -> None:
    """Configure logging for the application.
    
    Sets up logging with console and optionally file output, with customizable
    format and level.
    
    Args:
        level: The logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        format_string: Custom format string for log messages.
        output_file: Optional file path for logging to a file.
        
    Raises:
        LoggingError: If logging setup fails or parameters are invalid.
    """
    try:
        # Validate logging level
        numeric_level = getattr(logging, level.upper(), None)
        if not isinstance(numeric_level, int):
            raise LoggingError(f"Invalid log level: {level}")

        # Default format if none provided
        if not format_string:
            format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(numeric_level)

        # Create and configure console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(numeric_level)
        formatter = logging.Formatter(format_string)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

        # Add file handler if output file specified
        if output_file:
            try:
                file_handler = logging.FileHandler(output_file, encoding='utf-8')
                file_handler.setLevel(numeric_level)
                file_handler.setFormatter(formatter)
                root_logger.addHandler(file_handler)
            except Exception as e:
                raise LoggingError(f"Failed to setup file logging: {str(e)}", output_file) from e

        # Log successful setup
        logger = logging.getLogger(__name__)
        logger.debug("Logging configured successfully")
        logger.debug("Level: %s", level)
        logger.debug("Format: %s", format_string)
        if output_file:
            logger.debug("Output file: %s", output_file)

    except Exception as e:
        raise LoggingError(f"Failed to setup logging: {str(e)}") from e
