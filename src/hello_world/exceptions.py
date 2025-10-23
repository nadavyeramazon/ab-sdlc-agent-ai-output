class HelloWorldError(Exception):
    """Base exception for Hello World application.

    Args:
        message: Error message
        code: Optional error code
    """

    def __init__(self, message: str, code: int = 1) -> None:
        super().__init__(message)
        self.code = code

class ConfigurationError(HelloWorldError):
    """Raised when configuration loading or validation fails.

    Args:
        message: Error message
        code: Optional error code (default: 2)
    """

    def __init__(self, message: str, code: int = 2) -> None:
        super().__init__(message, code)
