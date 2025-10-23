import json
from typing import Optional, Dict, Any
from .exceptions import ConfigError
from .logger import get_logger

logger = get_logger(__name__)


class Config:
    DEFAULT_CONFIG = {
        'debug': False,
        'encoding': 'utf-8',
        'max_name_length': 100
    }
    
    def __init__(self, config_path: Optional[str] = None) -> None:
        self._config = self.DEFAULT_CONFIG.copy()
        
        if config_path:
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    custom_config = json.load(f)
                self._validate_config(custom_config)
                self._config.update(custom_config)
                logger.info('Loaded configuration from: %s', config_path)
            except (IOError, json.JSONDecodeError) as e:
                error_msg = f'Failed to load config from {config_path}: {str(e)}'
                logger.error(error_msg)
                raise ConfigError(error_msg)
        
        for key, value in self._config.items():
            setattr(self, key, value)
            
    def _validate_config(self, config: Dict[str, Any]) -> None:
        if not isinstance(config, dict):
            raise ConfigError('Configuration must be a dictionary')
            
        if 'debug' in config and not isinstance(config['debug'], bool):
            raise ConfigError('debug must be a boolean value')
            
        if 'encoding' in config:
            if not isinstance(config['encoding'], str):
                raise ConfigError('encoding must be a string')
            try:
                'test'.encode(config['encoding'])
            except LookupError:
                raise ConfigError(f'Invalid encoding: {config["encoding"]}')
                
        if 'max_name_length' in config:
            if not isinstance(config['max_name_length'], int):
                raise ConfigError('max_name_length must be an integer')
            if config['max_name_length'] <= 0:
                raise ConfigError('max_name_length must be positive')
                
    def as_dict(self) -> Dict[str, Any]:
        return self._config.copy()