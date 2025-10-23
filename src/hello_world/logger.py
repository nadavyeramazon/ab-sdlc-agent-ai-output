import logging
import sys
from typing import Optional

def setup_logger(level: str = 'INFO', log_format: Optional[str] = None) -> logging.Logger:
    """Configure and return a logger instance.

    Args:
        level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
            Defaults to 'INFO'.
        log_format (Optional[str]): Custom log format string. If None, uses default format.
            Defaults to None.

    Returns:
        logging.Logger: Configured logger instance.

    Raises:
        ValueError: If invalid logging level is provided.
    """
    logger = logging.getLogger('hello_world')
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # Set logging level
    try:
        logger.setLevel(level.upper())
    except (AttributeError, ValueError) as e:
        raise ValueError(f'Invalid logging level: {level}') from e

    # Create console handler
    handler = logging.StreamHandler(sys.stderr)
    
    # Set format
    if log_format is None:
        log_format = '%(asctime)s [%(levelname)s] %(message)s'
    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    logger.debug('Logger initialized with level: %s', level)
    
    return logger
