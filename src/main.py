#!/usr/bin/env python3

import sys
from typing import NoReturn
from hello_world import HelloWorld
from utils.logging_config import setup_logging

def main() -> NoReturn:
    """Main entry point for the Hello World application.

    Sets up logging and executes the Hello World greeting.
    Exits with code 0 on success, non-zero on error.
    """
    logger = setup_logging()
    
    try:
        hello = HelloWorld()
        result = hello.greet()
        logger.info(result)
        sys.exit(0)
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
