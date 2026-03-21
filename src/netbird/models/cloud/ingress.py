"""
Ingress port models for NetBird API.
"""

from typing import Any, Dict, List, Optional

from pydantic import Field

from ..common import BaseModel, ResourceId


class PortAllocationCreate(BaseModel):
    """Model for creating a port allocation."""

    name: str = Field(..., description="Port allocation name")
    enabled: bool = Field(..., description="Enabled status")
    port_ranges: Optional[List[Dict[str, Any]]] = Field(None, description="Port ranges")
    direct_port: Optional[Dict[str, Any]] = Field(None, description="Direct port config")


class PortAllocationUpdate(BaseModel):
    """Model for updating a port allocation."""

    name: Optional[str] = Field(None, description="Port allocation name")
    enabled: Optional[bool] = Field(None, description="Enabled status")
    port_ranges: Optional[List[Dict[str, Any]]] = Field(None, description="Port ranges")
    direct_port: Optional[Dict[str, Any]] = Field(None, description="Direct port config")


class PortAllocation(BaseModel):
    """NetBird port allocation model."""

    id: ResourceId = Field(..., description="Unique allocation identifier")
    name: Optional[str] = Field(None, description="Port allocation name")
    enabled: Optional[bool] = Field(None, description="Enabled status")
    port_ranges: Optional[List[Dict[str, Any]]] = Field(None, description="Port ranges")
    direct_port: Optional[Dict[str, Any]] = Field(None, description="Direct port config")


class IngressPeerCreate(BaseModel):
    """Model for creating an ingress peer."""

    peer_id: str = Field(..., description="Peer identifier")
    enabled: bool = Field(..., description="Enabled status")
    fallback: bool = Field(..., description="Fallback status")


class IngressPeerUpdate(BaseModel):
    """Model for updating an ingress peer."""

    enabled: Optional[bool] = Field(None, description="Enabled status")
    fallback: Optional[bool] = Field(None, description="Fallback status")


class IngressPeer(BaseModel):
    """NetBird ingress peer model."""

    id: ResourceId = Field(..., description="Unique ingress peer identifier")
    peer_id: Optional[str] = Field(None, description="Peer identifier")
    enabled: Optional[bool] = Field(None, description="Enabled status")
    fallback: Optional[bool] = Field(None, description="Fallback status")
