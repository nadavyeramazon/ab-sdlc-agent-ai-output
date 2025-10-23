"""
Hello World Application

This module implements a simple Hello World application with configurable greeting functionality.
The application focuses on performance, maintainability, and proper logging.

Performance targets:
- Execution time: <100ms
- Memory usage: <20MB

Author: AI Agent
Version: 1.0
"""

import logging
from typing import Optional
from .logger import setup_logger

logger = setup_logger(__name__)

class HelloWorld:
    """A class that provides greeting functionality with customizable messages."""
    
    def __init__(self, default_name: str = 'World'):
        """Initialize HelloWorld with a default name.
        
        Args:
            default_name (str): Default name to use in greetings
        """
        self.default_name = default_name
        logger.info(f'HelloWorld initialized with default name: {default_name}')
    
    def greet(self, name: Optional[str] = None) -> str:
        """Generate a greeting message.
        
        Args:
            name (Optional[str]): Name to include in greeting. Uses default if None.
            
        Returns:
            str: Formatted greeting message
        """
        try:
            actual_name = name if name is not None else self.default_name
            message = f'Hello, {actual_name}!'
            logger.info(f'Generated greeting: {message}')
            return message
        except Exception as e:
            logger.error(f'Error generating greeting: {str(e)}')
            raise

if __name__ == '__main__':
    # Command line execution example
    hello = HelloWorld()
    print(hello.greet())  # Uses default 'World'
    print(hello.greet('User'))  # Custom greeting