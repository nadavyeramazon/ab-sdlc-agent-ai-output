"""Custom exceptions for the Hello World application."""

class HelloWorldError(Exception):
    """Base exception class for Hello World application."""
    pass


class NetworkTimeoutError(HelloWorldError):
    """Raised when a network operation times out."""
    pass


class ConfigurationError(HelloWorldError):
    """Raised when there is an issue with configuration."""
    pass


class ValidationError(HelloWorldError):
    """Raised when input validation fails."""
    pass