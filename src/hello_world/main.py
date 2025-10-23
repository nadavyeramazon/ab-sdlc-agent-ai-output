#!/usr/bin/env python3

from typing import Optional, NoReturn, Dict, Any
import sys
import argparse
from .logger import setup_logger
from .config import Config, load_config, validate_config

MAX_MESSAGE_LENGTH = 1000

def validate_input(message: str) -> None:
    """Validate the input message.

    Args:
        message: The message to validate.

    Raises:
        ValueError: If message exceeds max length or contains invalid characters.
    """
    if len(message) > MAX_MESSAGE_LENGTH:
        raise ValueError(f"Message length exceeds maximum of {MAX_MESSAGE_LENGTH} characters")
    if not message.isprintable():
        raise ValueError("Message contains invalid characters")

def parse_args() -> argparse.Namespace:
    """Parse command line arguments.

    Returns:
        argparse.Namespace: Parsed command line arguments.
    """
    parser = argparse.ArgumentParser(description="Simple Hello World application")
    parser.add_argument(
        "--config", 
        type=str,
        default="config.yaml",
        help="Path to configuration file"
    )
    parser.add_argument(
        "--message",
        type=str,
        default="Hello, World!",
        help="Custom message to display"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )
    return parser.parse_args()

def process_message(message: str, config: Dict[str, Any]) -> str:
    """Process the input message according to configuration.

    Args:
        message: The input message to process.
        config: Configuration dictionary.

    Returns:
        str: The processed message.

    Raises:
        ValueError: If message validation fails.
    """
    validate_input(message)
    prefix = config.get('message_prefix', '')
    suffix = config.get('message_suffix', '')
    return f"{prefix}{message}{suffix}"

def main() -> Optional[NoReturn]:
    """Main entry point for the application.

    Returns:
        Optional[NoReturn]: Exits with status code 0 on success, 1 on error.
    """
    logger = setup_logger()
    try:
        args = parse_args()
        config = load_config(args.config)
        validate_config(config)
        
        logger.info("Processing message with configuration")
        result = process_message(args.message, config)
        print(result)
        return 0

    except FileNotFoundError as e:
        logger.error(f"Configuration file not found: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
