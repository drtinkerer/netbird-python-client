"""
Group models for NetBird API.
"""

from typing import Any, Dict, List, Optional

from pydantic import Field

from .common import BaseModel, ResourceId


class GroupCreate(BaseModel):
    """Model for creating a group.
    
    Attributes:
        name: Group name
        peers: List of peer IDs to include
        resources: List of network resources
    """
    
    name: str = Field(..., description="Group name")
    peers: Optional[List[ResourceId]] = Field(None, description="Peer IDs in group")
    resources: Optional[List[Dict[str, Any]]] = Field(None, description="Network resources")


class GroupUpdate(BaseModel):
    """Model for updating a group.
    
    Attributes:
        name: Group name
        peers: List of peer IDs to include
        resources: List of network resources
    """
    
    name: Optional[str] = Field(None, description="Group name")
    peers: Optional[List[ResourceId]] = Field(None, description="Peer IDs in group")
    resources: Optional[List[Dict[str, Any]]] = Field(None, description="Network resources")


class Group(BaseModel):
    """NetBird group model.
    
    Attributes:
        id: Unique group identifier
        name: Group name
        peers_count: Number of peers in group
        peers: List of peer objects with details
        resources: List of network resource objects
        resources_count: Number of resources in group
        issued: Creation timestamp
    """
    
    id: ResourceId = Field(..., description="Unique group identifier")
    name: str = Field(..., description="Group name")
    peers_count: int = Field(..., description="Number of peers in group")
    peers: Optional[List[Dict[str, Any]]] = Field(None, description="Peer objects with details")
    resources: Optional[List[Dict[str, Any]]] = Field(None, description="Network resource objects")
    resources_count: Optional[int] = Field(None, description="Number of resources in group")
    issued: Optional[str] = Field(None, description="Creation timestamp")
