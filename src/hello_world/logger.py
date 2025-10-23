import logging
from logging.handlers import RotatingFileHandler
from typing import Optional

def setup_logger(name: str = __name__) -> logging.Logger:
    """Set up application logger with rotation policy.

    Args:
        name: Logger name (defaults to module name).

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler with rotation
    file_handler = RotatingFileHandler(
        filename='app.log',
        maxBytes=5*1024*1024,  # 5MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    return logger

def set_log_level(logger: logging.Logger, level: str) -> None:
    """Set the logger's level.

    Args:
        logger: Logger instance to configure.
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).

    Raises:
        ValueError: If invalid log level provided.
    """
    level_map = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }

    if level.upper() not in level_map:
        raise ValueError(f"Invalid log level: {level}. Must be one of {list(level_map.keys())}")

    logger.setLevel(level_map[level.upper()])
