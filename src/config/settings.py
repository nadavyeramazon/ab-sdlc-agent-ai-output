"""Application settings and configuration module."""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application settings class using Pydantic BaseSettings.
    """
    APP_NAME: str = 'ab-sdlc-agent-ai-backend'
    VERSION: str = '1.0.0'
    
    class Config:
        env_file = '.env'