"""
Event models for NetBird API.
"""

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import Field, IPvAnyAddress

from .common import (
    BaseModel,
    ConnectionType,
    Protocol,
    ResourceId,
    TrafficDirection,
)


class AuditEvent(BaseModel):
    """Audit event model.

    Attributes:
        timestamp: Event timestamp
        activity: Activity description
        activity_code: Activity code
        id: Event ID
        initiator_id: ID of the initiator
        initiator_email: Email of the initiator
        initiator_name: Name of the initiator
        target_id: ID of the target
        meta: Additional event metadata
    """

    timestamp: str = Field(..., description="Event timestamp")
    activity: str = Field(..., description="Activity description")
    activity_code: Optional[str] = Field(None, description="Activity code")
    id: Optional[str] = Field(None, description="Event ID")
    initiator_id: ResourceId = Field(..., description="Initiator ID")
    initiator_email: Optional[str] = Field(None, description="Initiator email")
    initiator_name: Optional[str] = Field(None, description="Initiator name")
    target_id: Optional[ResourceId] = Field(None, description="Target ID")
    meta: Optional[Dict[str, Any]] = Field(None, description="Event metadata")


class NetworkTrafficEvent(BaseModel):
    """Network traffic event model.

    Attributes:
        timestamp: Event timestamp
        source_ip: Source IP address
        destination_ip: Destination IP address
        source_port: Source port
        destination_port: Destination port
        protocol: Network protocol
        bytes_sent: Number of bytes sent
        bytes_received: Number of bytes received
        user_id: Associated user ID
        peer_id: Associated peer ID
        reporter_id: Reporter peer ID
        policy_id: Applied policy ID
        direction: Traffic direction
        connection_type: Connection type (relay/p2p)
        allowed: Whether traffic was allowed
    """

    timestamp: datetime = Field(..., description="Event timestamp")
    source_ip: IPvAnyAddress = Field(..., description="Source IP address")
    destination_ip: IPvAnyAddress = Field(
        ..., description="Destination IP address"
    )
    source_port: int = Field(..., description="Source port")
    destination_port: int = Field(..., description="Destination port")
    protocol: Protocol = Field(..., description="Network protocol")
    bytes_sent: int = Field(..., description="Bytes sent")
    bytes_received: int = Field(..., description="Bytes received")
    user_id: Optional[ResourceId] = Field(
        None, description="Associated user ID"
    )
    peer_id: ResourceId = Field(..., description="Associated peer ID")
    reporter_id: ResourceId = Field(..., description="Reporter peer ID")
    policy_id: Optional[ResourceId] = Field(
        None, description="Applied policy ID"
    )
    direction: TrafficDirection = Field(..., description="Traffic direction")
    connection_type: ConnectionType = Field(..., description="Connection type")
    allowed: bool = Field(..., description="Traffic allowed status")
