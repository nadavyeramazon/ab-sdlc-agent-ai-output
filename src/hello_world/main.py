"""Hello World application main entry point.

This module provides the core functionality for the Hello World application,
including command-line interface and main execution logic.
"""

import argparse
import sys
from typing import List, Optional

from hello_world import __version__
from hello_world.logger import get_logger

logger = get_logger(__name__)

def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command line arguments.

    Args:
        argv: List of command line arguments, defaults to sys.argv[1:]

    Returns:
        Parsed command line arguments
    """
    parser = argparse.ArgumentParser(
        description='A simple Hello World application',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )
    return parser.parse_args(argv)

def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point for the application.

    Args:
        argv: List of command line arguments

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    try:
        parse_args(argv)
        logger.info('Starting Hello World application')
        print('Hello World!')
        logger.info('Successfully printed greeting')
        return 0
    except Exception as e:
        logger.error('Application error: %s', str(e))
        return 1

if __name__ == '__main__':
    sys.exit(main())
