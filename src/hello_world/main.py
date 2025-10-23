"""Main module for Hello World application."""
import argparse
import logging
import sys
from typing import List, Optional, Tuple

from hello_world.config import AppConfig, LogConfig
from hello_world.logger import setup_logger

__version__ = '0.1.0'


def parse_args(args: List[str]) -> Tuple[AppConfig, Optional[LogConfig]]:
    """Parse command line arguments.
    
    Args:
        args: Command line arguments
        
    Returns:
        Tuple[AppConfig, Optional[LogConfig]]: Application and logging configuration
        
    Raises:
        ValueError: If validation fails for any arguments
    """
    parser = argparse.ArgumentParser(
        description='Print a message to stdout and optionally log it.'
    )
    parser.add_argument(
        'message',
        help='Message to print (non-empty string)'
    )
    parser.add_argument(
        '--log-file',
        help='Path to log file'
    )
    parser.add_argument(
        '--log-max-bytes',
        type=int,
        default=1048576,  # 1MB
        help='Maximum size of log file before rotation (must be positive)'
    )
    parser.add_argument(
        '--log-backup-count',
        type=int,
        default=3,
        help='Number of backup files to keep (must be non-negative)'
    )
    parser.add_argument(
        '--log-level',
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Logging level'
    )
    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )
    
    parsed_args = parser.parse_args(args)
    
    log_config = None
    if parsed_args.log_file:
        try:
            log_config = LogConfig(
                log_file=parsed_args.log_file,
                max_bytes=parsed_args.log_max_bytes,
                backup_count=parsed_args.log_backup_count,
                log_level=parsed_args.log_level
            )
        except ValueError as e:
            parser.error(str(e))
    
    try:
        app_config = AppConfig(message=parsed_args.message, log_config=log_config)
    except ValueError as e:
        parser.error(str(e))
        
    return app_config, log_config


def main(argv: Optional[List[str]] = None) -> int:
    """Application entry point.
    
    Args:
        argv: Command line arguments. If None, sys.argv[1:] is used.
        
    Returns:
        int: Exit code (0 for success, non-zero for failure)
        
    Raises:
        SystemExit: On argument parsing errors
    """
    if argv is None:
        argv = sys.argv[1:]
    
    try:
        app_config, log_config = parse_args(argv)
        logger = setup_logger(log_config)
        
        print(app_config.message)
        logger.info('Message printed: %s', app_config.message)
        
        return 0
        
    except Exception as e:
        logging.error('Application error: %s', str(e))
        return 1


if __name__ == '__main__':
    sys.exit(main())
