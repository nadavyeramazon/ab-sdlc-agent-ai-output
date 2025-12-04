"""
Configuration management for the Task Manager application.

This module provides centralized configuration using Pydantic BaseSettings,
loading values from environment variables with type validation.
"""

import os
from typing import List

from pydantic import BaseModel, Field


class Settings(BaseModel):
    """
    Application settings loaded from environment variables.

    All settings are loaded from environment variables or .env file.
    Type validation is performed automatically by Pydantic.
    """

    # Database configuration
    db_host: str = Field(default="localhost")
    db_port: int = Field(default=3306)
    db_user: str = Field(default="taskuser")
    db_password: str = Field(default="taskpassword")
    db_name: str = Field(default="taskmanager")

    # Test database configuration
    test_db_name: str = Field(default="taskmanager_test")

    # Application environment
    env: str = Field(default="development")

    # CORS configuration
    cors_origins: List[str] = Field(default=["http://localhost:3000"])

    @classmethod
    def load_from_env(cls) -> "Settings":
        """
        Load settings from environment variables.

        Reads from .env file if present, then overrides with environment variables.
        """
        # Try to load .env file if it exists
        env_file = os.path.join(os.path.dirname(__file__), "..", ".env")
        if os.path.exists(env_file):
            from dotenv import load_dotenv
            load_dotenv(env_file)

        # Parse CORS origins from comma-separated string
        cors_origins_str = os.getenv("CORS_ORIGINS", "http://localhost:3000")
        cors_origins = [origin.strip() for origin in cors_origins_str.split(",")]

        return cls(
            db_host=os.getenv("DB_HOST", "localhost"),
            db_port=int(os.getenv("DB_PORT", "3306")),
            db_user=os.getenv("DB_USER", "taskuser"),
            db_password=os.getenv("DB_PASSWORD", "taskpassword"),
            db_name=os.getenv("DB_NAME", "taskmanager"),
            test_db_name=os.getenv("TEST_DB_NAME", "taskmanager_test"),
            env=os.getenv("ENV", "development"),
            cors_origins=cors_origins,
        )


# Create a singleton settings instance
settings = Settings.load_from_env()
