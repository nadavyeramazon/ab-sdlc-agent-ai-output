import pytest
import logging

@pytest.fixture(autouse=True)
def setup_test_logging():
    """Configure logging for tests.

    This fixture runs automatically for all tests and sets up a basic
    console logger to capture log output during testing.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Remove any existing handlers
    for handler in logger.handlers[:]: 
        logger.removeHandler(handler)

    # Add a console handler for tests
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    logger.addHandler(handler)
