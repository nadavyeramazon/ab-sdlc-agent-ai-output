"""Pytest configuration and shared fixtures"""
import pytest
import sys
from pathlib import Path

# Add parent directory to path so tests can import main module
sys.path.insert(0, str(Path(__file__).parent.parent))
