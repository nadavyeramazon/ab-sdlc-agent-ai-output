"""Core Hello World functionality module.

This module contains the core greeting functionality for the
Hello World application.

Example:
    >>> from hello_world import greet
    >>> greet('Alice')
    'Hello, Alice!'
"""

from typing import Optional
import logging


def greet(name: Optional[str] = 'World') -> str:
    """Generate a greeting message for the given name.

    Args:
        name: The name to include in the greeting.
              Defaults to 'World' if not provided.

    Returns:
        str: A formatted greeting message.

    Raises:
        ValueError: If name is empty or contains only whitespace.
        TypeError: If name is not a string.
    """
    logger = logging.getLogger(__name__)
    
    if not isinstance(name, str):
        error_msg = f'Name must be a string, got {type(name).__name__}'
        logger.error(error_msg)
        raise TypeError(error_msg)
        
    if not name.strip():
        error_msg = 'Name cannot be empty or whitespace'
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    logger.debug(f'Generating greeting for name: {name}')
    greeting = f'Hello, {name.strip()}!'
    logger.debug(f'Generated greeting: {greeting}')
    
    return greeting
