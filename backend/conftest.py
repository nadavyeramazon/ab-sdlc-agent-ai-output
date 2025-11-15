"""Pytest configuration file for backend tests.

This file is automatically loaded by pytest and configures the test environment.
It ensures that the backend module can be properly imported in tests.
"""

import sys
from pathlib import Path

# Add the backend directory to Python path so 'main' module can be imported
backend_dir = Path(__file__).parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))
