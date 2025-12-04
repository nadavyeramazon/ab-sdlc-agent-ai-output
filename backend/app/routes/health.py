"""
Health check route module.

This module provides health check endpoints for monitoring the application status.
"""

from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
def health_check() -> dict[str, str]:
    """
    Health check endpoint for monitoring.

    Returns:
        Dictionary with status information
    """
    return {"status": "healthy"}
