#!/usr/bin/env python3
"""
Simple Hello World Application

This is a basic Python application that demonstrates the classic
"Hello, World!" program with additional functionality.
"""


def greet(name="World"):
    """
    Generate a greeting message.
    
    Args:
        name (str): The name to greet. Defaults to "World".
    
    Returns:
        str: A greeting message.
    """
    return f"Hello, {name}!"


def main():
    """
    Main function to run the Hello World application.
    """
    # Print the basic hello world message
    print(greet())
    
    # Demonstrate with a custom name
    print(greet("Python Developer"))
    
    # Interactive greeting
    try:
        user_name = input("\nWhat's your name? ")
        if user_name.strip():
            print(greet(user_name))
        else:
            print(greet())
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye!")


if __name__ == "__main__":
    main()
