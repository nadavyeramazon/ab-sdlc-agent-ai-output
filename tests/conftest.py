"""Pytest configuration and fixtures.

This module provides test fixtures and configuration for the
Hello World application test suite.
"""

import os
import tempfile
from pathlib import Path
import pytest
from src.utils.logging_config import setup_logging


@pytest.fixture
def temp_log_dir():
    """Provide a temporary directory for log files.

    Yields:
        Path: Path to temporary log directory.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def test_logger(temp_log_dir):
    """Provide a configured logger for testing.

    Args:
        temp_log_dir: Temporary directory fixture for log files.

    Returns:
        logging.Logger: Configured logger instance.
    """
    log_file = temp_log_dir / 'test.log'
    return setup_logging(log_file=str(log_file))


@pytest.fixture(autouse=True)
def cleanup_logs():
    """Clean up log files after tests.

    This fixture runs automatically after each test.
    """
    yield
    if os.path.exists('logs'):
        for file in Path('logs').glob('*.log*'):
            try:
                file.unlink()
            except OSError:
                pass  # Ignore errors during cleanup
