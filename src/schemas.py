"""Pydantic schemas for request/response models.

Defines data validation and serialization schemas.
"""

from pydantic import BaseModel

class HelloResponse(BaseModel):
    """Response model for hello endpoint.

    Attributes:
        message (str): Hello world message
    """
    message: str
