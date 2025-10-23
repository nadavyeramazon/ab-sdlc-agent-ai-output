#!/usr/bin/env python3

from typing import Optional, NoReturn, Dict, Any
import sys
import argparse
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from pathlib import Path

from .config import Config
from .logger import setup_logger
from .exceptions import HelloWorldError, ConfigurationError

log = setup_logger(__name__)

def parse_args() -> argparse.Namespace:
    """Parse command line arguments.

    Returns:
        argparse.Namespace: Parsed command line arguments.
    """
    parser = argparse.ArgumentParser(
        description='Hello World Application',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
    parser.add_argument('--config', type=str, help='Path to config file')
    parser.add_argument('--message', type=str, help='Custom message to display')
    return parser.parse_args()

def validate_message(message: Optional[str]) -> str:
    """Validate and sanitize the input message.

    Args:
        message: Optional input message to validate

    Returns:
        str: Validated message

    Raises:
        HelloWorldError: If message validation fails
    """
    if message is None:
        return "Hello, World!"
    
    if not isinstance(message, str):
        raise HelloWorldError(f"Invalid message type: {type(message)}. Expected string.")
    
    message = message.strip()
    if not message:
        raise HelloWorldError("Message cannot be empty or whitespace only")
        
    if len(message) > 1000:
        raise HelloWorldError("Message exceeds maximum length of 1000 characters")
        
    return message

def load_config(config_path: Optional[str]) -> Dict[str, Any]:
    """Load and validate configuration.

    Args:
        config_path: Optional path to config file

    Returns:
        Dict[str, Any]: Configuration dictionary

    Raises:
        ConfigurationError: If config loading or validation fails
    """
    try:
        if config_path:
            path = Path(config_path)
            if not path.exists():
                raise ConfigurationError(f"Config file not found: {config_path}")
            config = Config.from_file(path)
        else:
            config = Config.default()
        
        return config.validate()
    except Exception as e:
        raise ConfigurationError(f"Failed to load configuration: {str(e)}")

def display_message(message: str, timeout: int = 5) -> None:
    """Display the message with timeout protection.

    Args:
        message: Message to display
        timeout: Timeout in seconds

    Raises:
        HelloWorldError: If display operation times out or fails
    """
    def _display() -> None:
        try:
            print(message, flush=True)
        except IOError as e:
            raise HelloWorldError(f"Failed to display message: {str(e)}")

    with ThreadPoolExecutor() as executor:
        try:
            future = executor.submit(_display)
            future.result(timeout=timeout)
        except TimeoutError:
            raise HelloWorldError(f"Display operation timed out after {timeout} seconds")
        except Exception as e:
            raise HelloWorldError(f"Unexpected error during display: {str(e)}")

def main() -> int:
    """Main entry point for the application.

    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    try:
        args = parse_args()
        config = load_config(args.config)
        message = validate_message(args.message or config.get('default_message'))
        display_message(message, config.get('timeout', 5))
        return 0

    except (HelloWorldError, ConfigurationError) as e:
        log.error(str(e))
        return 1
    except Exception as e:
        log.exception(f"Unexpected error: {str(e)}")
        return 2

def run() -> NoReturn:
    """Run the application and exit with appropriate status code."""
    sys.exit(main())

if __name__ == '__main__':
    run()
