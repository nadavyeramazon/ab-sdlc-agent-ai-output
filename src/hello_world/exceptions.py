"""Custom exceptions for the Hello World application."""

class ConfigError(Exception):
    """Raised when there is an error in the configuration.
    
    Args:
        message: A descriptive error message.
        config_key: The configuration key that caused the error.
    """
    def __init__(self, message: str, config_key: str = None):
        self.config_key = config_key
        super().__init__(f"Configuration error: {message} (key: {config_key if config_key else 'unknown'})")

class ValidationError(Exception):
    """Raised when input validation fails.
    
    Args:
        message: A descriptive error message.
        field: The field that failed validation.
    """
    def __init__(self, message: str, field: str = None):
        self.field = field
        super().__init__(f"Validation error: {message} (field: {field if field else 'unknown'})")

class LoggingError(Exception):
    """Raised when there is an error with logging configuration or operations.
    
    Args:
        message: A descriptive error message.
        log_config: The logging configuration that caused the error.
    """
    def __init__(self, message: str, log_config: str = None):
        self.log_config = log_config
        super().__init__(f"Logging error: {message} (config: {log_config if log_config else 'unknown'})")
