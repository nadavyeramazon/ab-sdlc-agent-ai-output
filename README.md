# Hello World Application

A production-grade Hello World service implementing best practices in Python.

## Features

- Type-annotated Python code
- Comprehensive test suite with 100% coverage
- PEP 8 compliant
- Production-ready error handling
- Efficient performance metrics

## Installation

```bash
pip install -e .
```

## Development Setup

```bash
pip install -e ".[dev]"
```

## Running Tests

```bash
pytest
```

## Code Quality

```bash
pylint src/hello_world tests
mypy src/hello_world tests
```

## Usage

```python
from hello_world.app import get_greeting

# Default greeting
result = get_greeting()
print(result['message'])  # Output: Hello, World!

# Personalized greeting
result = get_greeting('John')
print(result['message'])  # Output: Hello, John!
```
