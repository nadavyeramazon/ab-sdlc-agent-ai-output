# AB-SDLC-Agent-AI-Backend

A simple Hello World application demonstrating Python best practices.

## Features

- PEP 8 compliant code style
- Comprehensive error handling
- Console and file logging
- 90%+ test coverage
- Type hints
- Google-style docstrings

## Installation

```bash
pip install -e .
```

For development:
```bash
pip install -e ".[dev]"
```

## Usage

Run the application:
```bash
python -m src.main
```

Or after installation:
```bash
hello-world
```

## Testing

Run tests with coverage:
```bash
pytest --cov=src tests/
```

## Logging

Logs are written to:
- Console (stdout)
- `logs/hello_world.log` (rotated, max 5 files of 10MB each)
