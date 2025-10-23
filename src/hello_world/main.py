"""Main module for Hello World application."""

import argparse
import logging
import sys
from typing import NoReturn, Optional
import urllib.request

from .config import Config
from .exceptions import NetworkTimeoutError, ValidationError
from .logger import setup_logging

logger = logging.getLogger(__name__)

def parse_args() -> argparse.Namespace:
    """Parse command line arguments.

    Returns:
        Parsed command line arguments.
    """
    parser = argparse.ArgumentParser(description="Hello World Application")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )
    return parser.parse_args()

def validate_external_service(timeout: float) -> None:
    """Validate external service connectivity.
    
    Args:
        timeout: Request timeout in seconds.
        
    Raises:
        NetworkTimeoutError: If request times out.
    """
    try:
        urllib.request.urlopen("http://example.com", timeout=timeout)
    except urllib.error.URLError as e:
        raise NetworkTimeoutError("Failed to connect to external service") from e

def main() -> Optional[NoReturn]:
    """Main entry point for the application.

    Returns:
        None on success, or calls sys.exit() on error.
    """
    try:
        args = parse_args()
        config = Config()
        setup_logging(config)
        
        validate_external_service(config.request_timeout)
        
        print("Hello, World!")
        logger.info("Successfully printed greeting")
        return None
        
    except (NetworkTimeoutError, ValidationError) as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.exception("Unexpected error occurred")
        sys.exit(2)

if __name__ == "__main__":
    main()