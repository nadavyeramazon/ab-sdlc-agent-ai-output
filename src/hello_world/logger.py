from typing import Optional
import logging
import sys
from pathlib import Path

from .exceptions import HelloWorldError

def setup_logger(name: str, level: str = 'INFO', log_file: Optional[str] = None) -> logging.Logger:
    """Set up and configure logger.

    Args:
        name: Logger name
        level: Logging level (default: INFO)
        log_file: Optional path to log file

    Returns:
        logging.Logger: Configured logger instance

    Raises:
        HelloWorldError: If logger setup fails
    """
    try:
        logger = logging.getLogger(name)
        
        # Prevent duplicate handlers
        if logger.handlers:
            return logger
            
        # Set level
        level_map = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        logger.setLevel(level_map.get(level.upper(), logging.INFO))

        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        simple_formatter = logging.Formatter('%(levelname)s: %(message)s')

        # Console handler (always present)
        console = logging.StreamHandler(sys.stderr)
        console.setFormatter(simple_formatter)
        logger.addHandler(console)

        # File handler (if configured)
        if log_file:
            try:
                path = Path(log_file)
                if not path.parent.exists():
                    path.parent.mkdir(parents=True, exist_ok=True)
                    
                file_handler = logging.FileHandler(log_file, encoding='utf-8')
                file_handler.setFormatter(detailed_formatter)
                logger.addHandler(file_handler)
            except Exception as e:
                raise HelloWorldError(f"Failed to setup log file: {str(e)}")

        return logger

    except Exception as e:
        raise HelloWorldError(f"Failed to setup logger: {str(e)}")
