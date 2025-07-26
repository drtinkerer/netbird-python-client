"""
NetBird API Models

Pydantic models for all NetBird API resources.
"""

from .account import Account, AccountSettings
from .common import BaseModel, ResourceId, Timestamp
from .dns import DNSNameserverGroup, DNSSettings
from .event import AuditEvent, NetworkTrafficEvent
from .group import Group, GroupCreate, GroupUpdate
from .network import Network, NetworkCreate, NetworkResource, NetworkRouter, NetworkUpdate
from .peer import Peer, PeerUpdate
from .policy import Policy, PolicyCreate, PolicyRule, PolicyUpdate
from .route import Route, RouteCreate, RouteUpdate
from .setup_key import SetupKey, SetupKeyCreate, SetupKeyUpdate
from .token import Token, TokenCreate
from .user import User, UserCreate, UserUpdate

__all__ = [
    # Common
    "BaseModel",
    "ResourceId", 
    "Timestamp",
    
    # Account
    "Account",
    "AccountSettings",
    
    # User
    "User",
    "UserCreate",
    "UserUpdate",
    
    # Token
    "Token",
    "TokenCreate",
    
    # Peer
    "Peer",
    "PeerUpdate",
    
    # Setup Key
    "SetupKey",
    "SetupKeyCreate",
    "SetupKeyUpdate",
    
    # Group
    "Group",
    "GroupCreate",
    "GroupUpdate",
    
    # Network
    "Network",
    "NetworkCreate",
    "NetworkUpdate",
    "NetworkResource",
    "NetworkRouter",
    
    # Policy
    "Policy",
    "PolicyCreate",
    "PolicyUpdate",
    "PolicyRule",
    
    # Route
    "Route",
    "RouteCreate",
    "RouteUpdate",
    
    # DNS
    "DNSNameserverGroup",
    "DNSSettings",
    
    # Events
    "AuditEvent",
    "NetworkTrafficEvent",
]