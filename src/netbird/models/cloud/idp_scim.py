"""
IDP/SCIM integration models for NetBird API.
"""

from typing import List, Optional

from pydantic import Field

from ..common import BaseModel, ResourceId


class SCIMIntegrationCreate(BaseModel):
    """Model for creating a SCIM IDP integration."""

    prefix: str = Field(..., description="Connection prefix for SCIM provider")
    provider: str = Field(..., description="SCIM identity provider name")
    group_prefixes: Optional[List[str]] = Field(None, description="Group sync patterns")
    user_group_prefixes: Optional[List[str]] = Field(
        None, description="User group sync patterns"
    )


class SCIMIntegrationUpdate(BaseModel):
    """Model for updating a SCIM IDP integration."""

    enabled: Optional[bool] = Field(None, description="Integration enabled status")
    group_prefixes: Optional[List[str]] = Field(None, description="Group sync patterns")
    user_group_prefixes: Optional[List[str]] = Field(
        None, description="User group sync patterns"
    )


class SCIMIntegration(BaseModel):
    """NetBird SCIM IDP integration model."""

    id: ResourceId = Field(..., description="Unique integration identifier")
    prefix: Optional[str] = Field(None, description="Connection prefix")
    provider: Optional[str] = Field(None, description="SCIM provider name")
    enabled: Optional[bool] = Field(None, description="Integration enabled status")
    group_prefixes: Optional[List[str]] = Field(None, description="Group sync patterns")
    user_group_prefixes: Optional[List[str]] = Field(
        None, description="User group sync patterns"
    )
