from typing import Optional, Dict, Any
import pytest
from pathlib import Path
import tempfile
import json
import logging
from concurrent.futures import TimeoutError

from hello_world.main import validate_message, load_config, display_message, main
from hello_world.config import Config
from hello_world.exceptions import HelloWorldError, ConfigurationError
from hello_world.logger import setup_logger

# Test message validation
def test_validate_message_default() -> None:
    assert validate_message(None) == "Hello, World!"

def test_validate_message_custom() -> None:
    assert validate_message("Custom message") == "Custom message"

def test_validate_message_empty() -> None:
    with pytest.raises(HelloWorldError, match="Message cannot be empty"):
        validate_message("")
    with pytest.raises(HelloWorldError, match="Message cannot be empty"):
        validate_message("   ")

def test_validate_message_type_error() -> None:
    with pytest.raises(HelloWorldError, match="Invalid message type"):
        validate_message(123)  # type: ignore

def test_validate_message_too_long() -> None:
    with pytest.raises(HelloWorldError, match="exceeds maximum length"):
        validate_message("a" * 1001)

# Test configuration
@pytest.fixture
def config_file(tmp_path: Path) -> Path:
    config = {
        "default_message": "Test message",
        "timeout": 3,
        "log_level": "DEBUG"
    }
    path = tmp_path / "config.json"
    with path.open('w', encoding='utf-8') as f:
        json.dump(config, f)
    return path

def test_load_config_valid(config_file: Path) -> None:
    config = load_config(str(config_file))
    assert config["default_message"] == "Test message"
    assert config["timeout"] == 3

def test_load_config_missing_file() -> None:
    with pytest.raises(ConfigurationError, match="Config file not found"):
        load_config("/nonexistent/path.json")

def test_load_config_invalid_json(tmp_path: Path) -> None:
    path = tmp_path / "invalid.json"
    path.write_text("{invalid json")
    with pytest.raises(ConfigurationError, match="Invalid JSON"):
        load_config(str(path))

def test_config_validation() -> None:
    with pytest.raises(ConfigurationError, match="Missing required configuration"):
        Config({}).validate()

    with pytest.raises(ConfigurationError, match="must be a non-empty string"):
        Config({"default_message": ""}).validate()

    with pytest.raises(ConfigurationError, match="timeout must be a positive"):
        Config({"default_message": "test", "timeout": 0}).validate()

# Test message display
def test_display_message(capsys: pytest.CaptureFixture) -> None:
    message = "Test display"
    display_message(message)
    captured = capsys.readouterr()
    assert captured.out.strip() == message

def test_display_message_timeout() -> None:
    def slow_print() -> None:
        import time
        time.sleep(2)
        print("Too late")

    with pytest.raises(HelloWorldError, match="timed out"):
        with tempfile.TemporaryFile('w') as f:
            # Redirect stdout to avoid actual printing
            import sys
            old_stdout = sys.stdout
            sys.stdout = f
            try:
                display_message(slow_print(), timeout=1)  # type: ignore
            finally:
                sys.stdout = old_stdout

# Test logger setup
def test_logger_setup(tmp_path: Path) -> None:
    log_file = tmp_path / "test.log"
    logger = setup_logger("test", level="DEBUG", log_file=str(log_file))
    assert isinstance(logger, logging.Logger)
    assert logger.level == logging.DEBUG
    assert len(logger.handlers) == 2  # Console and file handlers
    assert log_file.exists()

def test_logger_invalid_level() -> None:
    logger = setup_logger("test", level="INVALID")
    assert logger.level == logging.INFO  # Falls back to default

# Test main function error handling
def test_main_with_invalid_config(monkeypatch: pytest.MonkeyPatch) -> None:
    class MockArgs:
        config = "/nonexistent/config.json"
        message = None

    monkeypatch.setattr("argparse.ArgumentParser.parse_args", lambda _: MockArgs())
    assert main() == 1  # Should return error code 1

# Test concurrent access
def test_concurrent_display(capsys: pytest.CaptureFixture) -> None:
    from concurrent.futures import ThreadPoolExecutor
    messages = [f"Message {i}" for i in range(5)]
    
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(display_message, msg) for msg in messages]
        for future in futures:
            future.result()
    
    captured = capsys.readouterr()
    for msg in messages:
        assert msg in captured.out
