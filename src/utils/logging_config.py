import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any

def setup_logging(log_level: int = logging.INFO) -> logging.Logger:
    """Setup application logging with both console and file handlers.

    Args:
        log_level: The logging level to use. Defaults to INFO.

    Returns:
        logging.Logger: Configured logger instance.
    """
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Create formatters
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler
    file_handler = RotatingFileHandler(
        log_dir / "hello_world.log",
        maxBytes=10485760,  # 10MB
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a specific module.

    Args:
        name: Name of the module requesting the logger.

    Returns:
        logging.Logger: Logger instance for the module.
    """
    return logging.getLogger(name)
