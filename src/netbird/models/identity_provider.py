"""
Identity provider models for NetBird API.
"""

from typing import Optional

from pydantic import Field

from .common import BaseModel, ResourceId


class IdentityProviderCreate(BaseModel):
    """Model for creating an identity provider."""

    type: str = Field(..., description="Type of identity provider")
    name: str = Field(..., description="Human-readable name")
    issuer: str = Field(..., description="OIDC issuer URL")
    client_id: str = Field(..., description="OAuth2 client ID")
    client_secret: str = Field(..., description="OAuth2 client secret")


class IdentityProviderUpdate(BaseModel):
    """Model for updating an identity provider."""

    type: Optional[str] = Field(None, description="Type of identity provider")
    name: Optional[str] = Field(None, description="Human-readable name")
    issuer: Optional[str] = Field(None, description="OIDC issuer URL")
    client_id: Optional[str] = Field(None, description="OAuth2 client ID")
    client_secret: Optional[str] = Field(None, description="OAuth2 client secret")


class IdentityProvider(BaseModel):
    """NetBird identity provider model."""

    id: ResourceId = Field(..., description="Unique identifier")
    type: str = Field(..., description="Type of identity provider")
    name: str = Field(..., description="Human-readable name")
    issuer: Optional[str] = Field(None, description="OIDC issuer URL")
    client_id: Optional[str] = Field(None, description="OAuth2 client ID")
