# High-Performance Hello World Application

A production-grade Hello World application with comprehensive logging, error handling, and performance optimization.

## Features

- Type-hinted Python implementation
- JSON structured logging
- Signal handling (SIGINT/SIGTERM)
- Performance optimization (<100ms execution)
- Cross-platform compatibility
- Comprehensive test suite
- UTF-8 encoding support

## Installation

No dependencies required for production use. Clone the repository and ensure Python 3.13+ is installed:

```bash
git clone https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend.git
cd ab-sdlc-agent-ai-backend
```

## Usage

Run the application:

```bash
python src/hello_world.py [-n NAME] [-v]
```

Options:
- `-n, --name`: Name to greet (default: "World")
- `-v, --verbose`: Enable verbose logging
- `-h, --help`: Show help message

Examples:
```bash
# Basic usage
python src/hello_world.py

# Custom name
python src/hello_world.py -n "John"

# Verbose logging
python src/hello_world.py -v

# Unicode support
python src/hello_world.py -n "🌍"
```

## Development Setup

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Unix
venv\Scripts\activate    # Windows
```

2. Install development dependencies:
```bash
# Uncomment development dependencies in requirements.txt first
pip install -r requirements.txt
```

## Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=term-missing

# Run performance tests
pytest tests/test_hello_world.py -v -k "test_performance"
```

The test suite includes:
- Unit tests
- Integration tests
- Performance tests (<100ms execution)
- Cross-platform compatibility tests
- Signal handling tests
- Logging verification
- Memory usage tests

## Contributing

1. Fork the repository
2. Create a feature branch:
```bash
git checkout -b feature/your-feature-name
```

3. Ensure all tests pass and coverage meets requirements:
- Maintain 95% or higher test coverage
- All tests must pass
- Code must follow PEP 8 style guide
- Include type hints and docstrings
- Verify performance requirements

4. Submit a pull request with:
- Clear description of changes
- Updated tests
- Documentation updates

## License

MIT
