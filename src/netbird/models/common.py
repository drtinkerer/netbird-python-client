"""
Common types and base models for NetBird API.
"""

from datetime import datetime
from enum import Enum
from typing import NewType, Any

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict


class BaseModel(PydanticBaseModel):
    """Base model for all NetBird API models."""
    
    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        use_enum_values=True,
        populate_by_name=True,
    )


# Type aliases for better type hints
ResourceId = NewType("ResourceId", str)
Timestamp = NewType("Timestamp", datetime)


class UserRole(str, Enum):
    """User role enumeration."""
    ADMIN = "admin"
    USER = "user"
    OWNER = "owner"


class UserStatus(str, Enum):
    """User status enumeration."""
    ACTIVE = "active"
    DISABLED = "disabled"
    INVITED = "invited"


class SetupKeyType(str, Enum):
    """Setup key type enumeration."""
    REUSABLE = "reusable"
    ONE_OFF = "one-off"


class NetworkType(str, Enum):
    """Network type enumeration."""
    IPV4 = "ipv4"
    IPV6 = "ipv6"
    DOMAIN = "domain"

    @classmethod
    def _missing_(cls, value: object) -> Any:
        if isinstance(value, str):
            value = value.lower()
            for member in cls:
                if member.value == value:
                    return member
        return None


class Protocol(str, Enum):
    """Network protocol enumeration."""
    TCP = "tcp"
    UDP = "udp"
    ICMP = "icmp"
    ALL = "all"

    @classmethod
    def _missing_(cls, value: object) -> Any:
        if isinstance(value, str):
            value = value.lower()
            for member in cls:
                if member.value == value:
                    return member
        return None


class PolicyAction(str, Enum):
    """Policy action enumeration."""
    ACCEPT = "accept"
    DROP = "drop"

    @classmethod
    def _missing_(cls, value: object) -> Any:
        if isinstance(value, str):
            value = value.lower()
            for member in cls:
                if member.value == value:
                    return member
        return None


class TrafficDirection(str, Enum):
    """Traffic direction enumeration."""
    SENT = "sent"
    RECEIVED = "received"


class ConnectionType(str, Enum):
    """Connection type enumeration."""
    RELAY = "relay"
    P2P = "p2p"