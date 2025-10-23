from typing import Optional
from utils.logging_config import get_logger

class HelloWorld:
    """A class that implements Hello World functionality.

    This class provides methods to generate hello world greetings
    with optional custom messages.

    Attributes:
        logger: Logger instance for the class.
    """

    def __init__(self) -> None:
        """Initialize the HelloWorld class with a logger."""
        self.logger = get_logger(__name__)

    def greet(self, name: Optional[str] = None) -> str:
        """Generate a hello world greeting.

        Args:
            name: Optional name to include in greeting.

        Returns:
            str: Formatted greeting message.

        Raises:
            ValueError: If name contains invalid characters.
        """
        if name:
            if not name.isalnum() and not name.replace(' ', '').isalnum():
                self.logger.error(f"Invalid name provided: {name}")
                raise ValueError("Name contains invalid characters")
            return f"Hello, {name}!"
        return "Hello, World!"
