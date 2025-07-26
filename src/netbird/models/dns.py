"""
DNS models for NetBird API.
"""

from typing import List, Optional

from pydantic import Field, IPvAnyAddress

from .common import BaseModel, ResourceId


class DNSNameserverGroup(BaseModel):
    """DNS nameserver group model.
    
    Attributes:
        id: Unique nameserver group identifier
        name: Nameserver group name
        description: Nameserver group description
        nameservers: List of nameserver IP addresses
        enabled: Whether the nameserver group is enabled
        groups: Group IDs that use this nameserver group
        domains: Domain list for this nameserver group
        search_domains_enabled: Whether search domains are enabled
    """
    
    id: ResourceId = Field(..., description="Unique nameserver group identifier")
    name: str = Field(..., description="Nameserver group name")
    description: Optional[str] = Field(None, description="Nameserver group description")
    nameservers: List[IPvAnyAddress] = Field(..., description="Nameserver IP addresses")
    enabled: bool = Field(True, description="Nameserver group enabled status")
    groups: Optional[List[ResourceId]] = Field(None, description="Group IDs using this nameserver")
    domains: Optional[List[str]] = Field(None, description="Domain list")
    search_domains_enabled: bool = Field(False, description="Search domains enabled")


class DNSSettings(BaseModel):
    """DNS settings model.
    
    Attributes:
        disabled_management_groups: Groups with disabled DNS management
    """
    
    disabled_management_groups: Optional[List[ResourceId]] = Field(
        None, description="Groups with disabled DNS management"
    )
