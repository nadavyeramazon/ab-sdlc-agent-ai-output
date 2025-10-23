"""Main module for the hello_world application.

This module provides the core functionality for the hello_world application,
including command-line interface and greeting generation.
"""

import argparse
import logging
from typing import Optional, Tuple

from hello_world.config import Config
from hello_world.logger import LogLevel, setup_logging

def parse_args() -> argparse.Namespace:
    """Parse command line arguments.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description='A friendly Hello World application')
    parser.add_argument('--name',
                       type=str,
                       help='Name to greet',
                       default='World')
    parser.add_argument('--config',
                       type=str,
                       help='Path to config file',
                       default=None)
    return parser.parse_args()

def generate_greeting(name: str = 'World') -> str:
    """Generate a greeting message.

    Args:
        name: Name to include in the greeting.

    Returns:
        str: A formatted greeting message.
    """
    logging.debug('Generating greeting for name: %s', name)
    greeting = f"Hello, {name}!"
    logging.debug('Generated greeting: %s', greeting)
    return greeting

def main() -> int:
    """Main entry point for the hello_world application.

    This function sets up logging, processes command-line arguments,
    generates a greeting, and handles any errors that occur.

    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    try:
        args = parse_args()
        config = Config.from_file(args.config) if args.config else Config()
        
        # Setup logging with configured level
        setup_logging(log_level=LogLevel[config.log_level.upper()])
        
        # Generate and display greeting
        greeting = generate_greeting(args.name)
        print(greeting)
        
        logging.debug('Application completed successfully')
        return 0
        
    except Exception as e:
        logging.error('Application error: %s', str(e))
        return 1

if __name__ == '__main__':
    exit(main())
