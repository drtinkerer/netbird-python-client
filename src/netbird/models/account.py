"""
Account models for NetBird API.
"""

from typing import Any, Dict, Optional

from pydantic import Field

from .common import BaseModel, ResourceId


class AccountSettings(BaseModel):
    """Account settings configuration.

    Attributes:
        peer_login_expiration: Peer login expiration settings
        peer_login_expiration_enabled: Whether peer login expiration is enabled
        peer_inactivity_expiration_enabled: Whether peer inactivity expiration
            is enabled
        user_view_restrictions: User view restriction settings
        group_propagation_enabled: Whether group propagation is enabled
        jwt_groups_enabled: Whether JWT groups are enabled
        jwt_groups_claim_name: JWT groups claim name
        dns_resolution_enabled: Whether DNS resolution is enabled
        network_traffic_logging_enabled: Whether network traffic logging is enabled
        lazy_connection_enabled: Whether lazy connection is enabled
    """

    peer_login_expiration: Optional[int] = Field(
        None, description="Peer login expiration in seconds"
    )
    peer_login_expiration_enabled: bool = Field(
        False, description="Enable peer login expiration"
    )
    peer_inactivity_expiration_enabled: bool = Field(
        False, description="Enable peer inactivity expiration"
    )
    user_view_restrictions: Optional[Dict[str, bool]] = Field(
        None, description="User view restrictions"
    )
    group_propagation_enabled: bool = Field(
        True, description="Enable group propagation"
    )
    jwt_groups_enabled: bool = Field(False, description="Enable JWT groups")
    jwt_groups_claim_name: Optional[str] = Field(
        None, description="JWT groups claim name"
    )
    dns_resolution_enabled: bool = Field(True, description="Enable DNS resolution")
    network_traffic_logging_enabled: bool = Field(
        False, description="Enable network traffic logging"
    )
    lazy_connection_enabled: bool = Field(False, description="Enable lazy connection")


class Account(BaseModel):
    """NetBird account model.

    Attributes:
        id: Unique account identifier
        domain: Account domain
        domain_category: Domain category
        created_at: Account creation timestamp
        created_by: User who created the account
        settings: Account settings
    """

    id: ResourceId = Field(..., description="Unique account identifier")
    domain: str = Field(..., description="Account domain")
    domain_category: Optional[str] = Field(None, description="Domain category")
    created_at: Optional[str] = Field(None, description="Account creation timestamp")
    created_by: Optional[str] = Field(None, description="User who created the account")
    settings: Optional[Dict[str, Any]] = Field(None, description="Account settings")
