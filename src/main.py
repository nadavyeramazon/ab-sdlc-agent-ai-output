#!/usr/bin/env python3

import signal
import sys
from typing import NoReturn
from logger import get_logger

logger = get_logger(__name__)

def signal_handler(signum: int, frame) -> NoReturn:
    """Handle system signals gracefully.
    
    Args:
        signum: Signal number received
        frame: Current stack frame
    """
    logger.info(f'Received signal {signum}. Shutting down...')
    sys.exit(0)

def hello_world() -> str:
    """Generate the hello world message.
    
    Returns:
        str: The hello world message
    """
    return 'Hello, World!'

def main() -> None:
    """Main application entry point."""
    # Setup signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        message = hello_world()
        logger.info(message)
        print(message)
    except Exception as e:
        logger.error(f'Error in main execution: {str(e)}')
        sys.exit(1)

if __name__ == '__main__':
    main()