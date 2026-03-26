"""
MSP models for NetBird API.
"""

from typing import Any, Dict, List, Optional

from pydantic import Field

from ..common import BaseModel, ResourceId


class MSPTenantCreate(BaseModel):
    """Model for creating an MSP tenant."""

    name: str = Field(..., description="Tenant name")
    domain: str = Field(..., description="Tenant domain")
    groups: List[Dict[str, Any]] = Field(
        ..., description="Groups with access and roles"
    )


class MSPTenantUpdate(BaseModel):
    """Model for updating an MSP tenant."""

    name: Optional[str] = Field(None, description="Tenant name")
    groups: Optional[List[Dict[str, Any]]] = Field(
        None, description="Groups with access and roles"
    )


class MSPTenant(BaseModel):
    """NetBird MSP tenant model."""

    id: ResourceId = Field(..., description="Unique tenant identifier")
    name: Optional[str] = Field(None, description="Tenant name")
    domain: Optional[str] = Field(None, description="Tenant domain")
    groups: Optional[List[Dict[str, Any]]] = Field(None, description="Groups")
    status: Optional[str] = Field(None, description="Tenant status")
