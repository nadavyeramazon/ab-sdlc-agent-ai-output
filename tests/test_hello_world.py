import json
import pytest
from hello_world.main import HelloWorld
from hello_world.config import Config
from hello_world.exceptions import HelloWorldError, ConfigError


class TestHelloWorld:
    def test_valid_message_generation(self):
        app = HelloWorld()
        assert app.generate_message('World') == 'Hello, World!'
        assert app.generate_message('OpenAI') == 'Hello, OpenAI!'
        
    def test_empty_name(self):
        app = HelloWorld()
        with pytest.raises(HelloWorldError) as exc:
            app.generate_message('')
        assert 'Name cannot be empty' in str(exc.value)
        
    def test_whitespace_name(self):
        app = HelloWorld()
        with pytest.raises(HelloWorldError) as exc:
            app.generate_message('   ')
        assert 'Name cannot be empty' in str(exc.value)
        
    def test_name_stripping(self):
        app = HelloWorld()
        assert app.generate_message('  World  ') == 'Hello, World!'
        
    def test_valid_json_input(self):
        app = HelloWorld()
        input_json = '{"name": "World"}'
        result = app.process_json_input(input_json)
        assert result['message'] == 'Hello, World!'
        assert result['status'] == 'success'
        assert result['input']['name'] == 'World'
        
    def test_invalid_json_format(self):
        app = HelloWorld()
        with pytest.raises(HelloWorldError) as exc:
            app.process_json_input('{invalid json}')
        assert 'Invalid JSON format' in str(exc.value)
        
    def test_missing_name_in_json(self):
        app = HelloWorld()
        with pytest.raises(HelloWorldError) as exc:
            app.process_json_input('{"message": "test"}')
        assert 'Missing required field: name' in str(exc.value)
        
    def test_empty_json_input(self):
        app = HelloWorld()
        with pytest.raises(HelloWorldError) as exc:
            app.process_json_input('')
        assert 'JSON input cannot be empty' in str(exc.value)
        
    def test_non_object_json(self):
        app = HelloWorld()
        with pytest.raises(HelloWorldError) as exc:
            app.process_json_input('["not an object"]')
        assert 'JSON must contain an object' in str(exc.value)


class TestConfig:
    def test_default_config(self):
        config = Config()
        assert config.debug is False
        assert config.encoding == 'utf-8'
        assert config.max_name_length == 100
        
    def test_invalid_config_type(self, tmp_path):
        config_file = tmp_path / 'config.json'
        config_file.write_text('["invalid"]')
        
        with pytest.raises(ConfigError) as exc:
            Config(str(config_file))
        assert 'Configuration must be a dictionary' in str(exc.value)
        
    def test_invalid_debug_type(self, tmp_path):
        config_file = tmp_path / 'config.json'
        config_file.write_text('{"debug": "invalid"}')
        
        with pytest.raises(ConfigError) as exc:
            Config(str(config_file))
        assert 'debug must be a boolean value' in str(exc.value)
        
    def test_invalid_encoding(self, tmp_path):
        config_file = tmp_path / 'config.json'
        config_file.write_text('{"encoding": "invalid-encoding"}')
        
        with pytest.raises(ConfigError) as exc:
            Config(str(config_file))
        assert 'Invalid encoding' in str(exc.value)
        
    def test_invalid_max_name_length(self, tmp_path):
        config_file = tmp_path / 'config.json'
        
        config_file.write_text('{"max_name_length": -1}')
        with pytest.raises(ConfigError) as exc:
            Config(str(config_file))
        assert 'max_name_length must be positive' in str(exc.value)
        
        config_file.write_text('{"max_name_length": "invalid"}')
        with pytest.raises(ConfigError) as exc:
            Config(str(config_file))
        assert 'max_name_length must be an integer' in str(exc.value)