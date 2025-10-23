"""Business logic for the Hello World service."""
import uuid
import logging
from typing import Dict

from .exceptions import ServiceError
from .schemas import HelloRequest, HelloResponse

logger = logging.getLogger(__name__)

class HelloWorldService:
    """Service class for generating greetings."""
    
    def __init__(self):
        """Initialize the service."""
        self._request_counter = 0
    
    def get_greeting(self, request: HelloRequest) -> HelloResponse:
        """Generate a greeting response.
        
        Args:
            request: Validated request model
            
        Returns:
            HelloResponse: Greeting response
            
        Raises:
            ServiceError: If greeting generation fails
        """
        try:
            self._request_counter += 1
            logger.debug(f'Generating greeting for {request.name}')
            
            # Generate unique request ID
            request_id = str(uuid.uuid4())
            
            # Create greeting message
            message = f'Hello, {request.name}!'
            
            logger.info(
                f'Generated greeting - RequestID: {request_id} '
                f'Counter: {self._request_counter}'
            )
            
            return HelloResponse(
                message=message,
                request_id=request_id
            )
            
        except Exception as e:
            logger.error(f'Failed to generate greeting: {str(e)}')
            raise ServiceError('Failed to generate greeting') from e
    
    def get_stats(self) -> Dict:
        """Get service statistics.
        
        Returns:
            Dict with service stats
        """
        return {
            'total_requests': self._request_counter
        }