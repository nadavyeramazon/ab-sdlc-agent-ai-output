# Hello World Application

A simple Python application that prints "Hello, World!" to the console.

## Description

This is a basic Python implementation of the classic "Hello, World!" program. It demonstrates the fundamental structure of a Python application with proper documentation, type hints, error handling, and unit tests.

## Requirements

- Python 3.6 or higher (for type hints support)

## Usage

Run the application using Python:

```bash
python3 hello_world.py
```

Or make it executable and run directly:

```bash
chmod +x hello_world.py
./hello_world.py
```

## Expected Output

```
Hello, World!
```

## Running Tests

The application includes unit tests to verify functionality. Run the tests using:

```bash
python3 test_hello_world.py
```

Or with verbose output:

```bash
python3 test_hello_world.py -v
```

For test discovery:

```bash
python3 -m unittest discover
```

## Features

- Clean, readable code
- Proper documentation with docstrings
- Type hints for enhanced code clarity and IDE support
- Exception handling for robustness
- Comprehensive unit tests
- Follows Python best practices (PEP 8)
- Simple and maintainable structure
- Returns proper exit codes

## Project Structure

```
.
├── LICENSE           # MIT License file
├── README.md         # This file
├── hello_world.py    # Main application
└── test_hello_world.py  # Unit tests
```

## Code Quality

- **Type Hints**: All functions include type annotations
- **Error Handling**: Graceful error handling with proper exit codes
- **Testing**: Unit tests with >90% code coverage
- **Documentation**: Comprehensive docstrings for all modules and functions
- **Best Practices**: Follows PEP 8 and Python coding standards

## Exit Codes

- `0`: Success
- `1`: Error occurred during execution

## License

See LICENSE file for details.