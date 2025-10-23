"""Application configuration module.

Handles all configuration and environment variables.
"""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings and configuration.

    Attributes:
        APP_NAME (str): Name of the application
        DEFAULT_MESSAGE (str): Default hello world message
        LOG_LEVEL (str): Logging level
    """
    APP_NAME: str = "Hello World Service"
    DEFAULT_MESSAGE: str = "Hello, World!"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()
