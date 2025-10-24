"""API routes module containing all endpoint definitions."""

from fastapi import APIRouter, HTTPException
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get('/')
async def hello_world() -> dict:
    """
    Hello World endpoint.
    
    Returns:
        dict: A greeting message
    """
    try:
        logger.info('Handling hello world request')
        return {'message': 'Hello, World!'}
    except Exception as e:
        logger.error(f'Error handling hello world request: {str(e)}')
        raise HTTPException(status_code=500, detail='Internal server error')

@router.get('/health')
async def health_check() -> dict:
    """
    Health check endpoint.
    
    Returns:
        dict: Service health status and version
    """
    try:
        logger.info('Handling health check request')
        return {'status': 'healthy', 'version': '1.0.0'}
    except Exception as e:
        logger.error(f'Error handling health check request: {str(e)}')
        raise HTTPException(status_code=500, detail='Internal server error')