"""
Logging Configuration Module

This module provides a standardized logging setup for the Hello World application.
It configures logging with proper formatting and handling.

Author: AI Agent
Version: 1.0
"""

import logging
import sys
from typing import Optional

def setup_logger(name: str, level: Optional[int] = None) -> logging.Logger:
    """Set up a logger with standardized configuration.
    
    Args:
        name (str): Logger name, typically __name__ of the calling module
        level (Optional[int]): Logging level, defaults to INFO if not specified
        
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:  # Avoid duplicate handlers
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    logger.setLevel(level or logging.INFO)
    return logger