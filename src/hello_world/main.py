"""Main module for the Hello World application.

Provides command line interface and core functionality.
"""

import argparse
import sys
from typing import Optional, Sequence

from hello_world.config import get_config
from hello_world.logger import HelloWorldLogger

__version__ = '1.0.0'

def validate_name(name: str) -> bool:
    """Validate the input name.

    Args:
        name: The name to validate.

    Returns:
        bool: True if name is valid, False otherwise.

    Raises:
        ValueError: If name is empty or exceeds maximum length.
    """
    config = get_config()
    
    if not name:
        raise ValueError('Name cannot be empty')
    
    if len(name) > config.max_name_length:
        raise ValueError(
            f'Name length exceeds maximum of {config.max_name_length} characters'
        )
    
    if not name.strip():  # Check for whitespace-only input
        raise ValueError('Name cannot be only whitespace')
    
    if not all(c.isprintable() for c in name):  # Check for non-printable characters
        raise ValueError('Name contains invalid characters')
    
    return True

def create_greeting(name: str) -> str:
    """Create a greeting message.

    Args:
        name: The name to include in the greeting.

    Returns:
        str: The formatted greeting message.

    Raises:
        ValueError: If name validation fails.
    """
    validate_name(name)
    return f'Hello, {name}!'

def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    """Parse command line arguments.

    Args:
        argv: List of command line arguments.

    Returns:
        argparse.Namespace: Parsed command line arguments.
    """
    parser = argparse.ArgumentParser(
        description='A simple Hello World application.'
    )
    parser.add_argument(
        '--name',
        help='Name to greet',
        type=str,
        required=True
    )
    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )
    return parser.parse_args(argv)

def main(argv: Optional[Sequence[str]] = None) -> int:
    """Main entry point for the application.

    Args:
        argv: Command line arguments.

    Returns:
        int: Exit code (0 for success, non-zero for failure).
    """
    logger = HelloWorldLogger()
    
    try:
        args = parse_args(argv)
        greeting = create_greeting(args.name)
        print(greeting)
        logger.info(f'Successfully created greeting for {args.name}')
        return 0
    except ValueError as e:
        logger.error(f'Validation error: {str(e)}')
        print(f'Error: {str(e)}', file=sys.stderr)
        return 1
    except Exception as e:
        logger.error(f'Unexpected error: {str(e)}')
        print(f'Error: An unexpected error occurred', file=sys.stderr)
        return 2

if __name__ == '__main__':
    sys.exit(main())
