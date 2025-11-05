#!/usr/bin/env python3
"""
A simple Hello World application in Python.

This module demonstrates a basic Python program that prints
a greeting message to the console.
"""

def greet(name="World"):
    """
    Greet someone with a personalized message.
    
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
    # Print the greeting
    message = greet()
    print(message)
    
    # Print some additional greetings
    names = ["Alice", "Bob", "Charlie"]
    for name in names:
        print(greet(name))
    
    # Fixed: Changed semicolon to colon
    if True:
        print("This line will cause a syntax error!")


if __name__ == "__main__":
    main()
