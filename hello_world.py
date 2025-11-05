#!/usr/bin/env python3
"""
Simple Hello World Application

This is a basic Python application that prints "Hello, World!" to the console.
"""

import sys
from typing import NoReturn


def print_hello_world() -> None:
    """
    Print the Hello World message to stdout.
    
    This function encapsulates the core functionality of printing
    the greeting message, making it testable and reusable.
    """
    print("Hello, World!")


def main() -> int:
    """
    Main function that executes the Hello World application.
    
    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    try:
        print_hello_world()
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())