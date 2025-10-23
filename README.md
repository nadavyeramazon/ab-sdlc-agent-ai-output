# Hello World Application

A simple Hello World application implemented in Python with zero runtime dependencies.

## Features

- Outputs "Hello World!" to stdout
- Command-line interface with --help and --version flags
- Comprehensive error handling
- Logging with timestamp and levels
- UTF-8 encoding
- Platform-appropriate line endings
- Type hints and Google-style docstrings

## Installation

No installation required. Simply clone the repository and run the application.

## Usage

```bash
# Run the application
python -m hello_world.main

# Show version
python -m hello_world.main --version

# Show help
python -m hello_world.main --help
```

## Development

1. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Run tests:
```bash
pytest
```

3. Run linting:
```bash
pylint src tests
```

4. Run type checking:
```bash
mypy src tests
```

## Technical Specifications

- Python 3.13 compatible
- Zero runtime dependencies
- 95%+ test coverage
- PEP 8 compliant
- Performance: <100ms startup, <500ms execution
- Memory usage: <50MB peak
