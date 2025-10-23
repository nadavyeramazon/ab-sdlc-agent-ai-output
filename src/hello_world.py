#!/usr/bin/env python3

import argparse
import json
import logging
import signal
import sys
import time
from typing import NoReturn, Optional

# Configure JSON structured logging
logger = logging.getLogger(__name__)
log_handler = logging.StreamHandler()
log_handler.setFormatter(
    logging.Formatter('{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}')
)
logger.addHandler(log_handler)
logger.setLevel(logging.INFO)

# Global flag for graceful shutdown
shutdown_requested = False

def signal_handler(signum: int, frame) -> None:
    """Handle system signals for graceful shutdown.
    
    Args:
        signum: Signal number received
        frame: Current stack frame
    """
    global shutdown_requested
    shutdown_requested = True
    logger.info(f"Received signal {signum}, initiating graceful shutdown")

def parse_args() -> argparse.Namespace:
    """Parse and validate command line arguments.
    
    Returns:
        Parsed command line arguments
    """
    parser = argparse.ArgumentParser(
        description="High-performance Hello World application with JSON logging"
    )
    parser.add_argument(
        "-n", 
        "--name",
        type=str,
        default="World",
        help="Name to greet (default: World)"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    return parser.parse_args()

def setup_signal_handlers() -> None:
    """Configure signal handlers for graceful shutdown."""
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

def generate_greeting(name: str) -> str:
    """Generate a greeting message.
    
    Args:
        name: Name to include in greeting
        
    Returns:
        Formatted greeting message
    """
    return f"Hello, {name}!"

def main() -> int:
    """Main application entry point.
    
    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    start_time = time.perf_counter()
    
    try:
        # Parse arguments
        args = parse_args()
        
        # Configure logging level
        if args.verbose:
            logger.setLevel(logging.DEBUG)
        
        # Setup signal handlers
        setup_signal_handlers()
        
        # Generate and output greeting
        greeting = generate_greeting(args.name)
        print(greeting, flush=True)
        
        # Log performance metrics
        execution_time = (time.perf_counter() - start_time) * 1000
        logger.debug({
            "execution_time_ms": execution_time,
            "message": "Execution completed successfully"
        })
        
        # Verify performance requirement
        if execution_time > 100:
            logger.warning(f"Execution time ({execution_time:.2f}ms) exceeded 100ms threshold")
        
        return 0
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
