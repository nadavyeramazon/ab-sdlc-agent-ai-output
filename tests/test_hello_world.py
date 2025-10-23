import json
import logging
import os
import signal
import sys
import time
from io import StringIO
from typing import Generator

import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.hello_world import generate_greeting, main, parse_args, signal_handler

@pytest.fixture
def capture_output() -> Generator[tuple[StringIO, StringIO], None, None]:
    """Capture stdout and stderr for testing."""
    stdout = StringIO()
    stderr = StringIO()
    old_stdout, old_stderr = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = stdout, stderr
    yield stdout, stderr
    sys.stdout, sys.stderr = old_stdout, old_stderr

@pytest.fixture
def capture_logs() -> Generator[StringIO, None, None]:
    """Capture JSON logs for testing."""
    log_stream = StringIO()
    handler = logging.StreamHandler(log_stream)
    handler.setFormatter(
        logging.Formatter('{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}')
    )
    logging.getLogger().addHandler(handler)
    yield log_stream
    logging.getLogger().removeHandler(handler)

def test_generate_greeting():
    """Test greeting message generation."""
    assert generate_greeting("World") == "Hello, World!"
    assert generate_greeting("Test") == "Hello, Test!"
    assert generate_greeting("") == "Hello, !"
    assert generate_greeting("🌍") == "Hello, 🌍!"

def test_parse_args():
    """Test command line argument parsing."""
    # Test default values
    sys.argv = ["hello_world.py"]
    args = parse_args()
    assert args.name == "World"
    assert not args.verbose
    
    # Test custom name
    sys.argv = ["hello_world.py", "-n", "Test"]
    args = parse_args()
    assert args.name == "Test"
    
    # Test verbose flag
    sys.argv = ["hello_world.py", "-v"]
    args = parse_args()
    assert args.verbose

def test_main_success(capture_output, capture_logs):
    """Test successful execution of main function."""
    stdout, stderr = capture_output
    sys.argv = ["hello_world.py", "-n", "Test"]
    
    exit_code = main()
    
    assert exit_code == 0
    assert stdout.getvalue().strip() == "Hello, Test!"
    assert "error" not in capture_logs.getvalue().lower()

def test_performance():
    """Test execution time requirements."""
    start_time = time.perf_counter()
    main()
    execution_time = (time.perf_counter() - start_time) * 1000
    
    assert execution_time < 100, f"Execution took {execution_time:.2f}ms, should be <100ms"

def test_signal_handling():
    """Test signal handler functionality."""
    # Simulate SIGINT
    signal_handler(signal.SIGINT, None)
    assert "shutdown" in capture_logs.getvalue().lower()

@pytest.mark.skipif(sys.platform == "win32", reason="Signal handling differs on Windows")
def test_signal_registration():
    """Test signal handler registration (Unix-like systems only)."""
    old_handler = signal.getsignal(signal.SIGINT)
    setup_signal_handlers()
    assert signal.getsignal(signal.SIGINT) == signal_handler
    signal.signal(signal.SIGINT, old_handler)  # Restore original handler

def test_unicode_support(capture_output):
    """Test handling of Unicode characters."""
    stdout, stderr = capture_output
    sys.argv = ["hello_world.py", "-n", "🌍"]
    
    exit_code = main()
    
    assert exit_code == 0
    assert stdout.getvalue().strip() == "Hello, 🌍!"

def test_memory_usage():
    """Test memory usage requirements."""
    import psutil
    process = psutil.Process()
    memory_before = process.memory_info().rss
    
    main()
    
    memory_after = process.memory_info().rss
    memory_used = (memory_after - memory_before) / (1024 * 1024)  # Convert to MB
    
    assert memory_used < 20, f"Memory usage {memory_used:.2f}MB exceeds 20MB limit"

def test_verbose_logging(capture_logs):
    """Test verbose logging output."""
    sys.argv = ["hello_world.py", "-v"]
    main()
    
    log_output = capture_logs.getvalue()
    assert "debug" in log_output.lower()
    assert "execution_time_ms" in log_output

def test_error_handling(capture_logs):
    """Test error handling and logging."""
    def simulate_error():
        raise Exception("Test error")
    
    # Monkey patch to simulate error
    original_parse = parse_args
    parse_args = simulate_error
    
    exit_code = main()
    
    assert exit_code == 1
    assert "error" in capture_logs.getvalue().lower()
    assert "test error" in capture_logs.getvalue().lower()
    
    # Restore original function
    parse_args = original_parse