import json
import sys
from typing import Optional, Dict, Any, Union

from .config import Config
from .exceptions import HelloWorldError, ConfigError
from .logger import get_logger

logger = get_logger(__name__)


class HelloWorld:
    def __init__(self, config_path: Optional[str] = None) -> None:
        try:
            self.config = Config(config_path) if config_path else Config()
            logger.info('HelloWorld initialized with config: %s', self.config.as_dict())
        except Exception as e:
            logger.error('Failed to initialize HelloWorld: %s', str(e))
            raise ConfigError(f'Configuration initialization failed: {str(e)}')

    def generate_message(self, name: str) -> str:
        if not name or not name.strip():
            error_msg = 'Name cannot be empty or whitespace only'
            logger.error(error_msg)
            raise HelloWorldError(error_msg)
            
        try:
            name = name.strip()
            message = f'Hello, {name}!'
            logger.info('Generated message for name: %s', name)
            return message
        except Exception as e:
            error_msg = f'Failed to generate message: {str(e)}'
            logger.error(error_msg)
            raise HelloWorldError(error_msg)

    def process_json_input(self, json_str: str) -> Dict[str, Any]:
        if not json_str or not json_str.strip():
            error_msg = 'JSON input cannot be empty'
            logger.error(error_msg)
            raise HelloWorldError(error_msg)
            
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            error_msg = f'Invalid JSON format: {str(e)}'
            logger.error(error_msg)
            raise HelloWorldError(error_msg)
            
        if not isinstance(data, dict):
            error_msg = 'JSON must contain an object'
            logger.error(error_msg)
            raise HelloWorldError(error_msg)
            
        if 'name' not in data:
            error_msg = 'Missing required field: name'
            logger.error(error_msg)
            raise HelloWorldError(error_msg)
            
        message = self.generate_message(data['name'])
        result = {
            'message': message,
            'status': 'success',
            'input': data
        }
        
        logger.info('Successfully processed JSON input: %s', json_str)
        return result


def main() -> Union[str, int]:
    if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help']:
        print('Usage: hello_world [name]')
        print('Options:')
        print('  --help     Show this help message')
        print('  --version  Show version information')
        return 0
        
    if sys.argv[1] in ['-v', '--version']:
        print('Hello World v1.0.0')
        return 0
        
    try:
        app = HelloWorld()
        message = app.generate_message(sys.argv[1])
        print(message)
        return 0
    except Exception as e:
        print(f'Error: {str(e)}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())