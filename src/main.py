#!/usr/bin/env python3

"""Main entry point for the Hello World application.

This module serves as the entry point for the Hello World application.
It configures logging and handles command line arguments.

Example:
    $ python main.py --name John
    Hello, John!

    $ python main.py  # uses default name 'World'
    Hello, World!

Exits:
    0: Success
    1: Invalid input or configuration error
    2: Runtime error
"""

import argparse
import sys
from typing import Optional, NoReturn

from hello_world import greet
from utils.logging_config import setup_logging


def parse_args() -> argparse.Namespace:
    """Parse command line arguments.

    Returns:
        argparse.Namespace: Parsed command line arguments.
    """
    parser = argparse.ArgumentParser(
        description='Hello World Application',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--name',
        type=str,
        default='World',
        help='Name to greet (default: World)'
    )
    return parser.parse_args()


def main() -> Optional[NoReturn]:
    """Main function that runs the Hello World application.

    Returns:
        Optional[NoReturn]: Never returns if system exit is called.

    Raises:
        SystemExit: With code 0 on success, 1 on invalid input,
                   or 2 on runtime error.
    """
    try:
        logger = setup_logging()
        args = parse_args()
        
        if not args.name.strip():  # Check for empty or whitespace-only name
            logger.error('Name cannot be empty')
            sys.exit(1)
            
        result = greet(args.name)
        print(result)
        logger.info(f'Successfully greeted {args.name}')
        sys.exit(0)
        
    except ValueError as e:
        logger.error(f'Invalid input: {str(e)}')
        sys.exit(1)
    except Exception as e:
        logger.exception(f'Unexpected error: {str(e)}')
        sys.exit(2)


if __name__ == '__main__':
    main()
