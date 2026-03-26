"""
Service (reverse proxy) models for NetBird API.
"""

from typing import Any, Dict, List, Optional

from pydantic import Field

from ..common import BaseModel, ResourceId


class ServiceCreate(BaseModel):
    """Model for creating a reverse proxy service."""

    name: str = Field(..., description="Service name")
    domain: str = Field(..., description="Service domain")
    targets: List[Dict[str, Any]] = Field(..., description="Service targets")
    enabled: bool = Field(..., description="Service enabled status")
    pass_host_header: Optional[bool] = Field(None, description="Pass host header")
    rewrite_redirects: Optional[bool] = Field(None, description="Rewrite redirects")
    auth: Dict[str, Any] = Field(..., description="Authentication configuration")


class ServiceUpdate(BaseModel):
    """Model for updating a reverse proxy service."""

    name: Optional[str] = Field(None, description="Service name")
    domain: Optional[str] = Field(None, description="Service domain")
    targets: Optional[List[Dict[str, Any]]] = Field(None, description="Service targets")
    enabled: Optional[bool] = Field(None, description="Service enabled status")
    pass_host_header: Optional[bool] = Field(None, description="Pass host header")
    rewrite_redirects: Optional[bool] = Field(None, description="Rewrite redirects")
    auth: Optional[Dict[str, Any]] = Field(
        None, description="Authentication configuration"
    )


class Service(BaseModel):
    """NetBird reverse proxy service model."""

    id: ResourceId = Field(..., description="Unique service identifier")
    name: str = Field(..., description="Service name")
    domain: Optional[str] = Field(None, description="Service domain")
    targets: Optional[List[Dict[str, Any]]] = Field(None, description="Service targets")
    enabled: Optional[bool] = Field(None, description="Service enabled status")
    pass_host_header: Optional[bool] = Field(None, description="Pass host header")
    rewrite_redirects: Optional[bool] = Field(None, description="Rewrite redirects")
    auth: Optional[Dict[str, Any]] = Field(
        None, description="Authentication configuration"
    )


class ServiceDomainCreate(BaseModel):
    """Model for creating a custom domain."""

    domain: str = Field(..., description="Custom domain")
    target_cluster: str = Field(..., description="Target cluster")


class ServiceDomain(BaseModel):
    """NetBird service domain model."""

    id: ResourceId = Field(..., description="Unique domain identifier")
    domain: Optional[str] = Field(None, description="Custom domain")
    target_cluster: Optional[str] = Field(None, description="Target cluster")
