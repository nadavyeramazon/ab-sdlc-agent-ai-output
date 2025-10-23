import logging
import pytest
from hello_world.main import generate_greeting, parse_args, main
from hello_world.logger import setup_logger

def test_generate_greeting_default():
    """Test default greeting without a name."""
    message, exit_code = generate_greeting()
    assert message == 'Hello, World!'
    assert exit_code == 0

def test_generate_greeting_with_name():
    """Test greeting with a valid name."""
    message, exit_code = generate_greeting('John')
    assert message == 'Hello, John!'
    assert exit_code == 0

def test_generate_greeting_with_complex_name():
    """Test greeting with a complex but valid name."""
    message, exit_code = generate_greeting('John Doe 123')
    assert message == 'Hello, John Doe 123!'
    assert exit_code == 0

def test_generate_greeting_empty_name():
    """Test greeting with empty name should raise ValueError."""
    with pytest.raises(ValueError, match='Name cannot be empty or whitespace'):
        generate_greeting('')
    with pytest.raises(ValueError, match='Name cannot be empty or whitespace'):
        generate_greeting('   ')

def test_generate_greeting_invalid_chars():
    """Test greeting with invalid characters should raise ValueError."""
    with pytest.raises(ValueError, match='Name can only contain alphanumeric characters and spaces'):
        generate_greeting('John@Doe')

def test_parse_args_default(monkeypatch):
    """Test argument parsing with default values."""
    monkeypatch.setattr('sys.argv', ['script.py'])
    args = parse_args()
    assert args.name is None
    assert not args.version
    assert args.log_level == 'INFO'

def test_parse_args_with_values(monkeypatch):
    """Test argument parsing with provided values."""
    monkeypatch.setattr('sys.argv', ['script.py', '--name', 'John', '--log-level', 'DEBUG'])
    args = parse_args()
    assert args.name == 'John'
    assert args.log_level == 'DEBUG'

def test_logger_setup():
    """Test logger configuration."""
    logger = setup_logger('DEBUG')
    assert isinstance(logger, logging.Logger)
    assert logger.level == logging.DEBUG
    assert len(logger.handlers) == 1

def test_logger_invalid_level():
    """Test logger setup with invalid level."""
    with pytest.raises(ValueError, match='Invalid logging level'):
        setup_logger('INVALID_LEVEL')

def test_main_version(monkeypatch, capsys):
    """Test main function with --version flag."""
    monkeypatch.setattr('sys.argv', ['script.py', '--version'])
    exit_code = main()
    captured = capsys.readouterr()
    assert 'Hello World version' in captured.out
    assert exit_code == 0

def test_main_error_handling(monkeypatch):
    """Test main function error handling."""
    monkeypatch.setattr('sys.argv', ['script.py', '--name', '@invalid@'])
    exit_code = main()
    assert exit_code == 1
