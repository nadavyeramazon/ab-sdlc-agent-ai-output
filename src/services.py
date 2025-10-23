"""Business logic services module.

Contains core business logic for the Hello World service.
"""

from typing import Optional
from .config import settings

class HelloWorldService:
    """Service for generating hello world messages."""

    def __init__(self):
        """Initialize the HelloWorldService."""
        self._message = settings.DEFAULT_MESSAGE

    def get_message(self) -> str:
        """Get the hello world message.

        Returns:
            str: Hello world message

        Raises:
            ValueError: If message generation fails
        """
        if not self._message:
            raise ValueError("Message not initialized")
        return self._message
