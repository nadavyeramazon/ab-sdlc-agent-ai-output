"""Configuration settings for the Hello World API."""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """API configuration settings.
    
    Attributes:
        rate_limit_requests (int): Number of requests allowed per time window
        rate_limit_window (int): Time window in seconds for rate limiting
    """
    rate_limit_requests: int = 5
    rate_limit_window: int = 60  # 1 minute
    
    class Config:
        env_prefix = 'API_'

# Create settings instance
settings = Settings()
