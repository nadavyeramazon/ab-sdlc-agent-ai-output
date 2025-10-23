"""Logging configuration for Hello World application."""
import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

from hello_world.config import LogConfig


def setup_logger(config: Optional[LogConfig] = None) -> logging.Logger:
    """Configure and return a logger instance.
    
    Args:
        config: Optional logging configuration. If None, logs to stderr.
    
    Returns:
        logging.Logger: Configured logger instance
        
    Raises:
        OSError: If log file directory cannot be created or is not writable
        ValueError: If log rotation fails
    """
    logger = logging.getLogger('hello_world')
    logger.setLevel(logging.INFO)
    
    # Clear any existing handlers
    logger.handlers = []
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    if config is None:
        # Log to stderr if no config provided
        handler = logging.StreamHandler(sys.stderr)
    else:
        try:
            # Ensure log directory exists
            log_dir = os.path.dirname(config.log_file)
            if log_dir:
                Path(log_dir).mkdir(parents=True, exist_ok=True)
                
            # Verify directory is writable
            if not os.access(log_dir, os.W_OK):
                raise OSError(f'Log directory {log_dir} is not writable')
                
            handler = RotatingFileHandler(
                config.log_file,
                maxBytes=config.max_bytes,
                backupCount=config.backup_count,
                encoding='utf-8'
            )
            
            # Test log rotation
            try:
                handler.doRollover()
            except Exception as e:
                raise ValueError(f'Failed to rotate log file: {str(e)}') from e
                
            logger.setLevel(getattr(logging, config.log_level))
            
        except OSError as e:
            raise OSError(f'Failed to configure file logging: {str(e)}') from e
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger
