"""
Policy models for NetBird API.
"""

from typing import List, Optional, Dict, Any

from pydantic import Field

from .common import BaseModel, PolicyAction, Protocol, ResourceId


class PolicyRule(BaseModel):
    """Policy rule model.
    
    Attributes:
        id: Rule identifier
        name: Rule name
        description: Rule description
        enabled: Whether rule is enabled
        action: Policy action (accept/drop)
        protocol: Network protocol
        ports: List of ports
        sources: Source groups
        destinations: Destination groups
        bidirectional: Whether rule is bidirectional
    """
    
    id: Optional[ResourceId] = Field(None, description="Rule identifier")
    name: str = Field(..., description="Rule name")
    description: Optional[str] = Field(None, description="Rule description")
    enabled: bool = Field(True, description="Rule enabled status")
    action: PolicyAction = Field(..., description="Policy action")
    protocol: Protocol = Field(..., description="Network protocol")
    ports: Optional[List[str]] = Field(None, description="Port list")
    sources: Optional[List[Dict[str, Any]]] = Field(None, description="Source group objects")
    destinations: Optional[List[Dict[str, Any]]] = Field(None, description="Destination group objects")
    bidirectional: bool = Field(False, description="Bidirectional rule")


class PolicyCreate(BaseModel):
    """Model for creating a policy.
    
    Attributes:
        name: Policy name
        description: Policy description
        enabled: Whether policy is enabled
        source_posture_checks: Source posture check IDs
        rules: List of policy rules
    """
    
    name: str = Field(..., description="Policy name")
    description: Optional[str] = Field(None, description="Policy description")
    enabled: bool = Field(True, description="Policy enabled status")
    source_posture_checks: Optional[List[ResourceId]] = Field(None, description="Source posture check IDs")
    rules: List[PolicyRule] = Field(..., description="Policy rules")


class PolicyUpdate(BaseModel):
    """Model for updating a policy.
    
    Attributes:
        name: Policy name
        description: Policy description
        enabled: Whether policy is enabled
        source_posture_checks: Source posture check IDs
        rules: List of policy rules
    """
    
    name: Optional[str] = Field(None, description="Policy name")
    description: Optional[str] = Field(None, description="Policy description")
    enabled: Optional[bool] = Field(None, description="Policy enabled status")
    source_posture_checks: Optional[List[ResourceId]] = Field(None, description="Source posture check IDs")
    rules: Optional[List[PolicyRule]] = Field(None, description="Policy rules")


class Policy(BaseModel):
    """NetBird policy model.
    
    Attributes:
        id: Unique policy identifier
        name: Policy name
        description: Policy description
        enabled: Whether policy is enabled
        source_posture_checks: Source posture check IDs
        rules: List of policy rules
    """
    
    id: ResourceId = Field(..., description="Unique policy identifier")
    name: str = Field(..., description="Policy name")
    description: Optional[str] = Field(None, description="Policy description")
    enabled: bool = Field(..., description="Policy enabled status")
    source_posture_checks: Optional[List[ResourceId]] = Field(None, description="Source posture check IDs")
    rules: List[PolicyRule] = Field(..., description="Policy rules")
