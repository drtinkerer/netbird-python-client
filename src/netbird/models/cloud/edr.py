"""
EDR integration models for NetBird API.
"""

from typing import Any, Dict, List, Optional

from pydantic import Field

from ..common import BaseModel


class EDRFalconConfig(BaseModel):
    """CrowdStrike Falcon EDR configuration."""

    client_id: str = Field(..., description="CrowdStrike API client ID")
    secret: str = Field(..., description="CrowdStrike API client secret")
    cloud_id: str = Field(..., description="CrowdStrike cloud identifier")
    groups: List[str] = Field(..., description="Groups this integration applies to")
    zta_score_threshold: int = Field(..., description="Minimum ZTA score (0-100)")
    enabled: Optional[bool] = Field(None, description="Integration enabled status")


class EDRHuntressConfig(BaseModel):
    """Huntress EDR configuration."""

    api_key: str = Field(..., description="Huntress API key")
    api_secret: str = Field(..., description="Huntress API secret")
    groups: List[str] = Field(..., description="Groups this integration applies to")
    last_synced_interval: int = Field(..., description="Sync interval in hours (min 24)")
    enabled: Optional[bool] = Field(None, description="Integration enabled status")
    match_attributes: Optional[Dict[str, Any]] = Field(None, description="Match attributes")


class EDRIntuneConfig(BaseModel):
    """Microsoft Intune EDR configuration."""

    client_id: str = Field(..., description="Azure application client ID")
    tenant_id: str = Field(..., description="Azure tenant ID")
    secret: str = Field(..., description="Azure application client secret")
    groups: List[str] = Field(..., description="Groups this integration applies to")
    last_synced_interval: int = Field(..., description="Sync interval in hours (min 24)")
    enabled: Optional[bool] = Field(None, description="Integration enabled status")


class EDRSentinelOneConfig(BaseModel):
    """SentinelOne EDR configuration."""

    api_token: str = Field(..., description="SentinelOne API token")
    api_url: str = Field(..., description="SentinelOne API URL")
    groups: List[str] = Field(..., description="Groups this integration applies to")
    last_synced_interval: int = Field(..., description="Sync interval in hours (min 24)")
    enabled: Optional[bool] = Field(None, description="Integration enabled status")
    match_attributes: Optional[Dict[str, Any]] = Field(None, description="Match attributes")
