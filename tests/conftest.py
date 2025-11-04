import pytest
import os

# Set test environment variables
os.environ["DEBUG"] = "true"
os.environ["ALLOWED_ORIGINS"] = "http://localhost:3000,http://localhost:8000"
