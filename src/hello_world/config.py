from typing import Dict, Any
import yaml

class Config:
    """Configuration class for the application.

    Attributes:
        message_prefix: Optional prefix for messages.
        message_suffix: Optional suffix for messages.
        log_config: Logging configuration dictionary.
    """
    def __init__(self, config_dict: Dict[str, Any]):
        self.message_prefix = config_dict.get('message_prefix', '')
        self.message_suffix = config_dict.get('message_suffix', '')
        self.log_config = config_dict.get('logging', {})

def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from YAML file.

    Args:
        config_path: Path to the YAML configuration file.

    Returns:
        Dict[str, Any]: Configuration dictionary.

    Raises:
        FileNotFoundError: If configuration file doesn't exist.
        yaml.YAMLError: If configuration file is invalid YAML.
    """
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def validate_config(config: Dict[str, Any]) -> None:
    """Validate configuration values.

    Args:
        config: Configuration dictionary to validate.

    Raises:
        ValueError: If configuration is invalid.
    """
    if not isinstance(config, dict):
        raise ValueError("Configuration must be a dictionary")

    # Validate message prefix/suffix
    prefix = config.get('message_prefix', '')
    suffix = config.get('message_suffix', '')
    if not isinstance(prefix, str) or not isinstance(suffix, str):
        raise ValueError("Message prefix and suffix must be strings")
    if len(prefix) > 100 or len(suffix) > 100:
        raise ValueError("Message prefix and suffix must not exceed 100 characters")

    # Validate logging configuration
    log_config = config.get('logging', {})
    if not isinstance(log_config, dict):
        raise ValueError("Logging configuration must be a dictionary")

    required_log_keys = ['level', 'file', 'max_size', 'backup_count']
    for key in required_log_keys:
        if key not in log_config:
            raise ValueError(f"Missing required logging configuration key: {key}")

    if not isinstance(log_config['max_size'], int) or log_config['max_size'] <= 0:
        raise ValueError("Log max_size must be a positive integer")

    if not isinstance(log_config['backup_count'], int) or log_config['backup_count'] <= 0:
        raise ValueError("Log backup_count must be a positive integer")
