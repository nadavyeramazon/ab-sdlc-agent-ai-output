"""Unit tests for service layer."""
import pytest
from src.schemas import HelloRequest
from src.services import HelloWorldService
from src.exceptions import ServiceError

def test_greeting_generation(service: HelloWorldService):
    """Test basic greeting generation."""
    request = HelloRequest(name='Test')
    response = service.get_greeting(request)
    assert response.message == 'Hello, Test!'
    assert response.request_id is not None

def test_greeting_with_default_name(service: HelloWorldService):
    """Test greeting with default name."""
    request = HelloRequest()
    response = service.get_greeting(request)
    assert response.message == 'Hello, World!'
    assert response.request_id is not None

def test_request_counter(service: HelloWorldService):
    """Test request counter increments."""
    initial_stats = service.get_stats()
    assert initial_stats['total_requests'] == 0
    
    service.get_greeting(HelloRequest())
    updated_stats = service.get_stats()
    assert updated_stats['total_requests'] == 1

@pytest.mark.parametrize('name', [
    'Alice',
    'Bob',
    'Charlie123',
    'Test-User'
])
def test_greeting_with_various_names(service: HelloWorldService, name: str):
    """Test greeting generation with various valid names."""
    request = HelloRequest(name=name)
    response = service.get_greeting(request)
    assert response.message == f'Hello, {name}!'
    assert response.request_id is not None

def test_unique_request_ids(service: HelloWorldService):
    """Test that request IDs are unique."""
    request = HelloRequest()
    response1 = service.get_greeting(request)
    response2 = service.get_greeting(request)
    assert response1.request_id != response2.request_id