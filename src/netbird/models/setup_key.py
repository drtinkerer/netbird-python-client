"""
Setup key models for NetBird API.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import Field

from .common import BaseModel, ResourceId, SetupKeyType


class SetupKeyCreate(BaseModel):
    """Model for creating a setup key.
    
    Attributes:
        name: Setup key name
        type: Key type (reusable or one-off)
        expires_in: Expiration time in seconds
        auto_groups: Group IDs to auto-assign
        usage_limit: Maximum number of uses
        ephemeral: Whether peers using this key are ephemeral
        allow_extra_dns_labels: Allow extra DNS labels
    """
    
    name: str = Field(..., description="Setup key name")
    type: SetupKeyType = Field(..., description="Key type")
    expires_in: int = Field(..., description="Expiration time in seconds")
    auto_groups: Optional[List[ResourceId]] = Field(None, description="Auto-assigned group IDs")
    usage_limit: Optional[int] = Field(None, description="Usage limit")
    ephemeral: bool = Field(False, description="Ephemeral peers flag")
    allow_extra_dns_labels: bool = Field(False, description="Allow extra DNS labels")


class SetupKeyUpdate(BaseModel):
    """Model for updating a setup key.
    
    Attributes:
        revoked: Whether the key is revoked
        auto_groups: Group IDs to auto-assign
    """
    
    revoked: Optional[bool] = Field(None, description="Revoked status")
    auto_groups: Optional[List[ResourceId]] = Field(None, description="Auto-assigned group IDs")


class SetupKey(BaseModel):
    """NetBird setup key model.
    
    Attributes:
        id: Unique setup key identifier
        key: The actual setup key value
        name: Setup key name
        expires: Expiration timestamp
        type: Key type
        valid: Whether the key is valid
        revoked: Whether the key is revoked
        used_times: Number of times the key has been used
        last_used: When the key was last used
        state: Key state
        auto_groups: Auto-assigned group IDs
        updated_at: Last update timestamp
        usage_limit: Usage limit
        ephemeral: Whether peers are ephemeral
        allow_extra_dns_labels: Whether extra DNS labels are allowed
    """
    
    id: ResourceId = Field(..., description="Unique setup key identifier")
    key: str = Field(..., description="Setup key value")
    name: str = Field(..., description="Setup key name")
    expires: Optional[str] = Field(None, description="Expiration timestamp")
    type: SetupKeyType = Field(..., description="Key type")
    valid: bool = Field(..., description="Key validity")
    revoked: bool = Field(..., description="Revoked status")
    used_times: int = Field(..., description="Usage count")
    last_used: Optional[str] = Field(None, description="Last used timestamp")
    state: str = Field(..., description="Key state")
    auto_groups: Optional[List[ResourceId]] = Field(None, description="Auto-assigned group IDs")
    updated_at: Optional[str] = Field(None, description="Last update timestamp")
    usage_limit: Optional[int] = Field(None, description="Usage limit")
    ephemeral: bool = Field(False, description="Ephemeral peers flag")
    allow_extra_dns_labels: Optional[bool] = Field(None, description="Allow extra DNS labels")
