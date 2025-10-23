#!/usr/bin/env python3

import argparse
import sys
from typing import Optional, Tuple
from .logger import setup_logger

__version__ = '1.0.0'

def parse_args() -> argparse.Namespace:
    """Parse command line arguments.

    Returns:
        argparse.Namespace: Parsed command-line arguments containing:
            - name (str, optional): Name to greet
            - version (bool): Show version information
            - log_level (str): Logging level (default: INFO)
    """
    parser = argparse.ArgumentParser(
        description='A friendly greeting program.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--name', type=str, help='Name to greet')
    parser.add_argument('--version', action='store_true', help='Show version information')
    parser.add_argument('--log-level', 
                      choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                      default='INFO',
                      help='Set the logging level')
    return parser.parse_args()

def generate_greeting(name: Optional[str] = None) -> Tuple[str, int]:
    """Generate a greeting message.

    Args:
        name (Optional[str]): Name to include in greeting. Defaults to None.

    Returns:
        Tuple[str, int]: A tuple containing:
            - str: The greeting message
            - int: Exit code (0 for success, 1 for error)

    Raises:
        ValueError: If the provided name is empty or contains invalid characters.
    """
    if name:
        # Validate name
        if not name.strip():
            raise ValueError('Name cannot be empty or whitespace')
        if not all(c.isalnum() or c.isspace() for c in name):
            raise ValueError('Name can only contain alphanumeric characters and spaces')
        return f'Hello, {name}!', 0
    return 'Hello, World!', 0

def main() -> int:
    """Main entry point for the application.

    Parses command-line arguments, sets up logging, and generates a greeting.

    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    try:
        args = parse_args()
        logger = setup_logger(args.log_level)

        if args.version:
            print(f'Hello World version {__version__}')
            return 0

        logger.debug('Generating greeting message')
        message, exit_code = generate_greeting(args.name)
        
        logger.info('Message generated successfully')
        print(message)
        return exit_code

    except ValueError as e:
        logger.error(f'Invalid input: {str(e)}')
        return 1
    except Exception as e:
        logger.critical(f'Unexpected error: {str(e)}')
        return 2

if __name__ == '__main__':
    sys.exit(main())
