"""
Network models for NetBird API.
"""

from typing import List, Optional

from pydantic import Field

from .common import BaseModel, ResourceId


class NetworkCreate(BaseModel):
    """Model for creating a network.
    
    Attributes:
        name: Network name
        description: Network description
    """
    
    name: str = Field(..., description="Network name")
    description: Optional[str] = Field(None, description="Network description")


class NetworkUpdate(BaseModel):
    """Model for updating a network.
    
    Attributes:
        name: Network name
        description: Network description
    """
    
    name: Optional[str] = Field(None, description="Network name")
    description: Optional[str] = Field(None, description="Network description")


class NetworkResource(BaseModel):
    """Network resource model.
    
    Attributes:
        id: Resource identifier
        name: Resource name
        description: Resource description
        address: Resource address
        enabled: Whether resource is enabled
        groups: Associated group IDs
    """
    
    id: ResourceId = Field(..., description="Resource identifier")
    name: str = Field(..., description="Resource name")
    description: Optional[str] = Field(None, description="Resource description")
    address: str = Field(..., description="Resource address")
    enabled: bool = Field(True, description="Resource enabled status")
    groups: Optional[List[ResourceId]] = Field(None, description="Associated group IDs")


class NetworkRouter(BaseModel):
    """Network router model.
    
    Attributes:
        id: Router identifier
        name: Router name
        description: Router description
        peer: Associated peer ID
        peer_groups: Associated peer group IDs
        metric: Router metric
        masquerade: Whether masquerading is enabled
        enabled: Whether router is enabled
    """
    
    id: ResourceId = Field(..., description="Router identifier")
    name: str = Field(..., description="Router name")
    description: Optional[str] = Field(None, description="Router description")
    peer: Optional[ResourceId] = Field(None, description="Associated peer ID")
    peer_groups: Optional[List[ResourceId]] = Field(None, description="Associated peer group IDs")
    metric: int = Field(9999, description="Router metric")
    masquerade: bool = Field(False, description="Masquerading enabled")
    enabled: bool = Field(True, description="Router enabled status")


class Network(BaseModel):
    """NetBird network model.
    
    Attributes:
        id: Unique network identifier
        name: Network name
        description: Network description
        routers: List of router IDs
        resources: List of resource IDs
        policies: List of associated policy IDs
        routing_peers_count: Number of routing peers
    """
    
    id: ResourceId = Field(..., description="Unique network identifier")
    name: str = Field(..., description="Network name")
    description: Optional[str] = Field(None, description="Network description")
    routers: Optional[List[str]] = Field(None, description="Router IDs")
    resources: Optional[List[str]] = Field(None, description="Resource IDs")
    policies: Optional[List[ResourceId]] = Field(None, description="Associated policy IDs")
    routing_peers_count: Optional[int] = Field(None, description="Number of routing peers")
