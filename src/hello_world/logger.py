"""Logging configuration for Hello World application."""

import logging
from logging.handlers import RotatingFileHandler
from typing import Optional

from .config import Config

def setup_logging(config: Config) -> None:
    """Configure application logging.
    
    Args:
        config: Application configuration instance.
    """
    logger = logging.getLogger("hello_world")
    logger.setLevel(config.log_level)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler with rotation
    if config.log_file:
        file_handler = RotatingFileHandler(
            config.log_file,
            maxBytes=config.log_max_bytes,
            backupCount=config.log_backup_count,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)