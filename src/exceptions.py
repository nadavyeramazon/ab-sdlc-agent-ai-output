"""Custom exceptions for the Hello World service."""

class HelloWorldError(Exception):
    """Base exception for Hello World service."""
    pass

class ConfigurationError(HelloWorldError):
    """Raised when there's an issue with service configuration."""
    pass

class ValidationError(HelloWorldError):
    """Raised when request validation fails."""
    pass

class ServiceError(HelloWorldError):
    """Raised when the service encounters an operational error."""
    pass