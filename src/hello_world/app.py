"""Main application module for Hello World service.

This module provides the core functionality for the Hello World service,
implementing a simple greeting function with proper error handling and type hints.
"""

from typing import Dict, Optional


def get_greeting(name: Optional[str] = None) -> Dict[str, str]:
    """Generate a greeting message.

    Args:
        name (Optional[str]): Name of the person to greet. Defaults to None.

    Returns:
        Dict[str, str]: Dictionary containing the greeting message.

    Raises:
        ValueError: If the provided name is empty or contains invalid characters.
    """
    if name is not None:
        if not isinstance(name, str):
            raise TypeError('Name must be a string')
        if not name.strip():
            raise ValueError('Name cannot be empty')
        if not all(c.isalnum() or c.isspace() for c in name):
            raise ValueError('Name contains invalid characters')
        message = f'Hello, {name.strip()}!'
    else:
        message = 'Hello, World!'

    return {'message': message}
