"""
Peer models for NetBird API.
"""

from typing import Any, Dict, List, Optional

from pydantic import Field, IPvAnyAddress

from .common import BaseModel, ResourceId


class PeerUpdate(BaseModel):
    """Model for updating a peer.

    Attributes:
        name: Peer name
        ssh_enabled: Whether SSH is enabled
        login_expiration_enabled: Whether login expiration is enabled
        inactivity_expiration_enabled: Whether inactivity expiration is enabled
        approval_required: Whether approval is required (cloud-only)
    """

    name: Optional[str] = Field(None, description="Peer name")
    ssh_enabled: Optional[bool] = Field(None, description="SSH enabled flag")
    login_expiration_enabled: Optional[bool] = Field(
        None, description="Login expiration enabled"
    )
    inactivity_expiration_enabled: Optional[bool] = Field(
        None, description="Inactivity expiration enabled"
    )
    approval_required: Optional[bool] = Field(
        None, description="Approval required (cloud-only)"
    )


class Peer(BaseModel):
    """NetBird peer model.

    Attributes:
        id: Unique peer identifier
        name: Peer name
        ip: Peer IP address
        connection_ip: Connection IP address
        connected: Whether peer is connected
        last_seen: Last seen timestamp
        os: Operating system
        version: NetBird version
        groups: List of group objects with details
        user_id: Associated user ID
        hostname: Peer hostname
        ui_version: UI version
        dns_label: DNS label
        ssh_enabled: Whether SSH is enabled
        login_expiration_enabled: Whether login expiration is enabled
        login_expired: Whether login has expired
        approval_required: Whether approval is required
        accessible_peers_count: Number of accessible peers
        city_name: Geographic city name
        country_code: Geographic country code
        ephemeral: Whether peer is ephemeral
        extra_dns_labels: Additional DNS labels
        geoname_id: Geographic name ID
        inactivity_expiration_enabled: Whether inactivity expiration is enabled
        kernel_version: OS kernel version
        last_login: Last login timestamp
        serial_number: Device serial number
    """

    id: ResourceId = Field(..., description="Unique peer identifier")
    name: str = Field(..., description="Peer name")
    ip: IPvAnyAddress = Field(..., description="Peer IP address")
    connection_ip: Optional[str] = Field(None, description="Connection IP address")
    connected: bool = Field(..., description="Connection status")
    last_seen: Optional[str] = Field(None, description="Last seen timestamp")
    os: Optional[str] = Field(None, description="Operating system")
    version: Optional[str] = Field(None, description="NetBird version")
    groups: Optional[List[Dict[str, Any]]] = Field(
        None, description="Group objects with details"
    )
    user_id: Optional[ResourceId] = Field(None, description="Associated user ID")
    hostname: Optional[str] = Field(None, description="Peer hostname")
    ui_version: Optional[str] = Field(None, description="UI version")
    dns_label: Optional[str] = Field(None, description="DNS label")
    ssh_enabled: bool = Field(False, description="SSH enabled flag")
    login_expiration_enabled: bool = Field(
        False, description="Login expiration enabled"
    )
    login_expired: bool = Field(False, description="Login expired status")
    approval_required: bool = Field(False, description="Approval required flag")
    accessible_peers_count: Optional[int] = Field(
        None, description="Number of accessible peers"
    )
    city_name: Optional[str] = Field(None, description="Geographic city name")
    country_code: Optional[str] = Field(None, description="Geographic country code")
    ephemeral: Optional[bool] = Field(None, description="Whether peer is ephemeral")
    extra_dns_labels: Optional[List[str]] = Field(
        None, description="Additional DNS labels"
    )
    geoname_id: Optional[int] = Field(None, description="Geographic name ID")
    inactivity_expiration_enabled: Optional[bool] = Field(
        None, description="Inactivity expiration enabled"
    )
    kernel_version: Optional[str] = Field(None, description="OS kernel version")
    last_login: Optional[str] = Field(None, description="Last login timestamp")
    serial_number: Optional[str] = Field(None, description="Device serial number")
