"""Main module for the Hello World application.

This module provides the core functionality for the Hello World application,
including command-line interface and message generation.
"""

import sys
import argparse
import logging
from typing import List, Optional
from .config import Config
from .logger import setup_logging
from .exceptions import ConfigError, ValidationError, LoggingError

logger = logging.getLogger(__name__)

VERSION = "1.0.0"

def create_parser() -> argparse.ArgumentParser:
    """Create and configure the command-line argument parser.
    
    Returns:
        An ArgumentParser instance configured with all supported arguments.
    """
    parser = argparse.ArgumentParser(
        description="A sophisticated Hello World application",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {VERSION}'
    )
    parser.add_argument(
        '--config',
        help='Path to configuration file'
    )
    parser.add_argument(
        '--greeting',
        help='Custom greeting message'
    )
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Set the logging level'
    )
    return parser

def validate_args(args: argparse.Namespace) -> None:
    """Validate command-line arguments.
    
    Args:
        args: Parsed command-line arguments.
        
    Raises:
        ValidationError: If any arguments are invalid.
    """
    logger.debug("Validating command-line arguments: %s", vars(args))
    if args.greeting and not args.greeting.strip():
        raise ValidationError("Greeting cannot be empty", "greeting")

def generate_message(greeting: str) -> str:
    """Generate the formatted greeting message.
    
    Args:
        greeting: The greeting text to use.
        
    Returns:
        A formatted greeting message.
        
    Raises:
        ValidationError: If greeting is invalid.
    """
    if not greeting or not greeting.strip():
        raise ValidationError("Greeting cannot be empty", "greeting")
    
    logger.debug("Generating message with greeting: %s", greeting)
    return f"{greeting.strip()}\n"

def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point for the Hello World application.
    
    Args:
        argv: List of command-line arguments (defaults to sys.argv[1:]).
        
    Returns:
        Exit code (0 for success, non-zero for errors).
    """
    if argv is None:
        argv = sys.argv[1:]

    try:
        # Parse arguments
        parser = create_parser()
        args = parser.parse_args(argv)
        logger.debug("Parsed arguments: %s", vars(args))

        # Load configuration
        config = Config()
        if args.config:
            config.load_from_file(args.config)
        config.load_from_env()

        # Setup logging
        log_level = args.log_level or config.get("log_level", "INFO")
        setup_logging(level=log_level)

        # Validate arguments
        validate_args(args)

        # Generate and output message
        greeting = args.greeting or config.get("greeting")
        message = generate_message(greeting)
        encoding = config.get("output_encoding", "utf-8")
        sys.stdout.buffer.write(message.encode(encoding))
        logger.info("Successfully output greeting message")
        return 0

    except ConfigError as e:
        logger.error("Configuration error: %s", str(e))
        return 1
    except ValidationError as e:
        logger.error("Validation error: %s", str(e))
        return 2
    except LoggingError as e:
        logger.error("Logging error: %s", str(e))
        return 3
    except Exception as e:
        logger.error("Unexpected error: %s", str(e))
        return 4

if __name__ == "__main__":
    sys.exit(main())
