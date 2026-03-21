"""
DNS zone and record models for NetBird API.
"""

from typing import List, Optional

from pydantic import Field

from .common import BaseModel, ResourceId


class DNSZoneCreate(BaseModel):
    """Model for creating a DNS zone."""

    name: str = Field(..., description="Zone name identifier")
    domain: str = Field(..., description="Zone domain (FQDN)")
    enabled: Optional[bool] = Field(None, description="Zone status")
    enable_search_domain: bool = Field(
        ..., description="Enable zone as search domain"
    )
    distribution_groups: List[str] = Field(
        ..., description="Group IDs for peer resolution"
    )


class DNSZoneUpdate(BaseModel):
    """Model for updating a DNS zone."""

    name: Optional[str] = Field(None, description="Zone name identifier")
    domain: Optional[str] = Field(None, description="Zone domain (FQDN)")
    enabled: Optional[bool] = Field(None, description="Zone status")
    enable_search_domain: Optional[bool] = Field(
        None, description="Enable zone as search domain"
    )
    distribution_groups: Optional[List[str]] = Field(
        None, description="Group IDs for peer resolution"
    )


class DNSZone(BaseModel):
    """NetBird DNS zone model."""

    id: ResourceId = Field(..., description="Unique zone identifier")
    name: str = Field(..., description="Zone name identifier")
    domain: str = Field(..., description="Zone domain")
    enabled: Optional[bool] = Field(None, description="Zone status")
    enable_search_domain: Optional[bool] = Field(
        None, description="Search domain status"
    )
    distribution_groups: Optional[List[str]] = Field(
        None, description="Distribution group IDs"
    )


class DNSRecordCreate(BaseModel):
    """Model for creating a DNS record."""

    name: str = Field(..., description="FQDN for DNS record")
    type: str = Field(..., description="DNS record type")
    content: str = Field(..., description="IP or domain value")
    ttl: int = Field(..., description="Time to live in seconds")


class DNSRecordUpdate(BaseModel):
    """Model for updating a DNS record."""

    name: Optional[str] = Field(None, description="FQDN for DNS record")
    type: Optional[str] = Field(None, description="DNS record type")
    content: Optional[str] = Field(None, description="IP or domain value")
    ttl: Optional[int] = Field(None, description="Time to live in seconds")


class DNSRecord(BaseModel):
    """NetBird DNS record model."""

    id: ResourceId = Field(..., description="Unique record identifier")
    name: str = Field(..., description="FQDN for DNS record")
    type: str = Field(..., description="DNS record type")
    content: str = Field(..., description="IP or domain value")
    ttl: int = Field(..., description="Time to live in seconds")
