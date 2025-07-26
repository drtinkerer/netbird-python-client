"""
Route models for NetBird API.
"""

from typing import List, Optional

from pydantic import Field

from .common import BaseModel, NetworkType, ResourceId


class RouteCreate(BaseModel):
    """Model for creating a route.
    
    Attributes:
        description: Route description
        network_id: Network identifier
        enabled: Whether route is enabled
        peer: Peer ID for the route
        peer_groups: Peer group IDs for the route
        network: Network address
        network_type: Network type (ipv4, ipv6, domain)
        domains: Domain list for domain routes
        metric: Route metric
        masquerade: Whether masquerading is enabled
        groups: Group IDs that can access this route
        keep_route: Whether to keep route on disconnect
        access_control_groups: Access control group IDs
    """
    
    description: Optional[str] = Field(None, description="Route description")
    network_id: str = Field(..., description="Network identifier")
    enabled: bool = Field(True, description="Route enabled status")
    peer: Optional[ResourceId] = Field(None, description="Peer ID for route")
    peer_groups: Optional[List[ResourceId]] = Field(None, description="Peer group IDs")
    network: Optional[str] = Field(None, description="Network address")
    network_type: NetworkType = Field(..., description="Network type")
    domains: Optional[List[str]] = Field(None, description="Domain list")
    metric: int = Field(9999, description="Route metric")
    masquerade: bool = Field(False, description="Masquerading enabled")
    groups: Optional[List[ResourceId]] = Field(None, description="Group IDs with access")
    keep_route: bool = Field(False, description="Keep route on disconnect")
    access_control_groups: Optional[List[ResourceId]] = Field(None, description="Access control group IDs")


class RouteUpdate(BaseModel):
    """Model for updating a route.
    
    Attributes:
        description: Route description
        enabled: Whether route is enabled
        peer: Peer ID for the route
        peer_groups: Peer group IDs for the route
        network: Network address
        domains: Domain list for domain routes
        metric: Route metric
        masquerade: Whether masquerading is enabled
        groups: Group IDs that can access this route
        keep_route: Whether to keep route on disconnect
        access_control_groups: Access control group IDs
    """
    
    description: Optional[str] = Field(None, description="Route description")
    enabled: Optional[bool] = Field(None, description="Route enabled status")
    peer: Optional[ResourceId] = Field(None, description="Peer ID for route")
    peer_groups: Optional[List[ResourceId]] = Field(None, description="Peer group IDs")
    network: Optional[str] = Field(None, description="Network address")
    domains: Optional[List[str]] = Field(None, description="Domain list")
    metric: Optional[int] = Field(None, description="Route metric")
    masquerade: Optional[bool] = Field(None, description="Masquerading enabled")
    groups: Optional[List[ResourceId]] = Field(None, description="Group IDs with access")
    keep_route: Optional[bool] = Field(None, description="Keep route on disconnect")
    access_control_groups: Optional[List[ResourceId]] = Field(None, description="Access control group IDs")


class Route(BaseModel):
    """NetBird route model.
    
    Attributes:
        id: Unique route identifier
        description: Route description
        network_id: Network identifier
        enabled: Whether route is enabled
        peer: Peer ID for the route
        peer_groups: Peer group IDs for the route
        network: Network address
        network_type: Network type
        domains: Domain list for domain routes
        metric: Route metric
        masquerade: Whether masquerading is enabled
        groups: Group IDs that can access this route
        keep_route: Whether to keep route on disconnect
        access_control_groups: Access control group IDs
    """
    
    id: ResourceId = Field(..., description="Unique route identifier")
    description: Optional[str] = Field(None, description="Route description")
    network_id: str = Field(..., description="Network identifier")
    enabled: bool = Field(..., description="Route enabled status")
    peer: Optional[ResourceId] = Field(None, description="Peer ID for route")
    peer_groups: Optional[List[ResourceId]] = Field(None, description="Peer group IDs")
    network: Optional[str] = Field(None, description="Network address")
    network_type: NetworkType = Field(..., description="Network type")
    domains: Optional[List[str]] = Field(None, description="Domain list")
    metric: int = Field(..., description="Route metric")
    masquerade: bool = Field(..., description="Masquerading enabled")
    groups: Optional[List[ResourceId]] = Field(None, description="Group IDs with access")
    keep_route: bool = Field(..., description="Keep route on disconnect")
    access_control_groups: Optional[List[ResourceId]] = Field(None, description="Access control group IDs")
