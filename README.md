# Hello World Application

A sophisticated Hello World application implemented in Python 3.13 with comprehensive logging, error handling, and test coverage.

## Features

- Type-annotated Python implementation
- Comprehensive error handling
- Rotating file and console logging
- High test coverage
- Command-line interface

## Installation

```bash
pip install -e .
```

For development installation with test dependencies:

```bash
pip install -e .[dev]
```

## Usage

### Command Line

```bash
# Using the installed command
hello-world --name Alice

# Running the module directly
python -m src.main --name Bob
```

### As a Module

```python
from src.hello_world import greet

# Basic usage
result = greet('Alice')  # Returns: 'Hello, Alice!'

# Using default name
result = greet()  # Returns: 'Hello, World!'
```

## Logging

Logs are written to both console and file:
- Console: All INFO and above messages
- File: Rotating log files in `logs/hello_world.log`
  - Maximum file size: 10MB
  - Keeps last 5 backup files

### Custom Logging Configuration

```python
from src.utils.logging_config import setup_logging
import logging

# Custom configuration
logger = setup_logging(
    log_level=logging.DEBUG,
    log_format='%(asctime)s - %(levelname)s - %(message)s',
    log_file='custom/path/app.log'
)
```

## Testing

Run the test suite:

```bash
pytest
```

With coverage:

```bash
pytest --cov=src tests/
```

## Error Handling

The application handles various error cases:

```python
# TypeError for invalid input types
greet(123)  # Raises TypeError

# ValueError for empty or whitespace names
greet('')  # Raises ValueError
greet('   ')  # Raises ValueError
```

Exit codes:
- 0: Success
- 1: Invalid input or configuration error
- 2: Runtime error

## Contributing

1. Ensure all tests pass
2. Add tests for new functionality
3. Update documentation as needed
4. Follow PEP 8 style guidelines

## License

MIT License
