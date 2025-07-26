"""
Token models for NetBird API.
"""

from datetime import datetime
from typing import Optional

from pydantic import Field, validator

from .common import BaseModel, ResourceId


class TokenCreate(BaseModel):
    """Model for creating a new token.
    
    Attributes:
        name: Token name
        expires_in: Token expiration in days (1-365)
    """
    
    name: str = Field(..., description="Token name")
    expires_in: int = Field(..., description="Token expiration in days", ge=1, le=365)


class Token(BaseModel):
    """NetBird token model.
    
    Attributes:
        id: Unique token identifier
        name: Token name
        creation_date: When the token was created
        expiration_date: When the token expires
        created_by: User ID who created the token
        last_used: When the token was last used
    """
    
    id: ResourceId = Field(..., description="Unique token identifier")
    name: str = Field(..., description="Token name")
    creation_date: datetime = Field(..., description="Token creation date")
    expiration_date: datetime = Field(..., description="Token expiration date")
    created_by: ResourceId = Field(..., description="Creator user ID")
    last_used: Optional[datetime] = Field(None, description="Last used timestamp")
