"""Test suite for the Hello World application.

This module contains comprehensive tests for the application including
edge cases and error conditions.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
import tempfile
import pytest
from typing import Generator, Any

from hello_world.logger import LogConfig, setup_logger
from hello_world.main import main, create_parser

@pytest.fixture
def temp_log_file() -> Generator[Path, None, None]:
    """Create a temporary log file for testing.

    Yields:
        Path: Path to temporary log file
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        log_file = Path(temp_dir) / 'test.log'
        yield log_file

def test_logger_configuration(temp_log_file: Path) -> None:
    """Test logger configuration with valid parameters."""
    config = LogConfig(
        log_level='INFO',
        log_file=temp_log_file,
        max_bytes=1024,
        backup_count=2
    )
    logger = setup_logger('test', config)
    
    assert logger.level == logging.INFO
    assert len(logger.handlers) == 2
    assert isinstance(logger.handlers[0], logging.handlers.RotatingFileHandler)
    assert isinstance(logger.handlers[1], logging.StreamHandler)

def test_logger_invalid_level(temp_log_file: Path) -> None:
    """Test logger configuration with invalid log level."""
    config = LogConfig(
        log_level='INVALID',
        log_file=temp_log_file
    )
    with pytest.raises(ValueError, match='Invalid log level'):
        setup_logger('test', config)

def test_logger_invalid_max_bytes(temp_log_file: Path) -> None:
    """Test logger configuration with invalid max_bytes."""
    config = LogConfig(
        log_level='INFO',
        log_file=temp_log_file,
        max_bytes=-1
    )
    with pytest.raises(ValueError, match='max_bytes must be positive'):
        setup_logger('test', config)

def test_logger_rotation(temp_log_file: Path) -> None:
    """Test log file rotation."""
    config = LogConfig(
        log_level='INFO',
        log_file=temp_log_file,
        max_bytes=100,
        backup_count=2
    )
    logger = setup_logger('test', config)

    # Write enough data to trigger rotation
    long_message = 'x' * 50
    for _ in range(5):
        logger.info(long_message)

    # Check that rotation files exist
    assert temp_log_file.exists()
    assert (temp_log_file.parent / f'{temp_log_file.name}.1').exists()

def test_main_success(temp_log_file: Path, capsys: Any) -> None:
    """Test successful execution of main function."""
    argv = [
        '--log-level', 'INFO',
        '--log-file', str(temp_log_file),
        '--max-log-size', '1024'
    ]
    exit_code = main(argv)
    assert exit_code == 0

    # Check stdout
    captured = capsys.readouterr()
    assert 'Hello, World!' in captured.out

    # Check log file
    assert temp_log_file.exists()
    log_content = temp_log_file.read_text()
    assert 'Hello, World!' in log_content

def test_main_invalid_args(capsys: Any) -> None:
    """Test main function with invalid arguments."""
    argv = ['--max-log-size', '-1']
    exit_code = main(argv)
    assert exit_code == 1

    captured = capsys.readouterr()
    assert 'Error:' in captured.err

def test_create_parser() -> None:
    """Test argument parser creation and defaults."""
    parser = create_parser()
    args = parser.parse_args([])

    assert args.log_level == 'INFO'
    assert isinstance(args.log_file, str)
    assert args.max_log_size == 1024 * 1024

def test_unicode_logging(temp_log_file: Path) -> None:
    """Test logging with Unicode characters."""
    config = LogConfig(
        log_level='INFO',
        log_file=temp_log_file
    )
    logger = setup_logger('test', config)

    unicode_message = 'Hello, 世界!'
    logger.info(unicode_message)

    log_content = temp_log_file.read_text(encoding='utf-8')
    assert unicode_message in log_content

def test_log_directory_creation(temp_log_file: Path) -> None:
    """Test automatic creation of log directory."""
    nested_path = temp_log_file.parent / 'nested' / 'dirs' / 'test.log'
    config = LogConfig(
        log_level='INFO',
        log_file=nested_path
    )
    logger = setup_logger('test', config)

    assert nested_path.parent.exists()
    logger.info('Test message')
    assert nested_path.exists()
