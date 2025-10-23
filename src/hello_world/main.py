"""Main module for the Hello World application.

This module implements a simple Hello World application with logging
and command line interface.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Optional, NoReturn, Dict, Any

from .logger import LogConfig, setup_logger

def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser.

    Returns:
        argparse.ArgumentParser: Configured parser instance
    """
    parser = argparse.ArgumentParser(
        description='Simple Hello World application with logging',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        default='INFO',
        help='Set the logging level'
    )
    parser.add_argument(
        '--log-file',
        type=str,
        default=str(Path.home() / '.hello_world' / 'hello.log'),
        help='Path to the log file'
    )
    parser.add_argument(
        '--max-log-size',
        type=int,
        default=1024 * 1024,  # 1MB
        help='Maximum size of log file in bytes before rotation'
    )
    return parser

def validate_args(args: argparse.Namespace) -> None:
    """Validate command line arguments.

    Args:
        args: Parsed command line arguments

    Raises:
        ValueError: If any argument is invalid
    """
    if args.max_log_size <= 0:
        raise ValueError(f'max-log-size must be positive, got {args.max_log_size}')

def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point for the Hello World application.

    Args:
        argv: List of command line arguments (uses sys.argv if None)

    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    try:
        # Parse arguments
        parser = create_parser()
        args = parser.parse_args(argv)

        # Validate arguments
        validate_args(args)

        # Configure logging
        log_config = LogConfig(
            log_level=args.log_level,
            log_file=args.log_file,
            max_bytes=args.max_log_size
        )
        logger = setup_logger('hello_world', log_config)

        # Log hello world message
        logger.info('Hello, World!')
        print('Hello, World!')

        return 0

    except ValueError as e:
        print(f'Error: {e}', file=sys.stderr)
        return 1
    except Exception as e:
        print(f'Unexpected error: {e}', file=sys.stderr)
        return 2

if __name__ == '__main__':
    sys.exit(main())
