"""
Posture check models for NetBird API.
"""

from typing import Any, Dict, Optional

from pydantic import Field

from .common import BaseModel, ResourceId


class PostureCheckCreate(BaseModel):
    """Model for creating a posture check."""

    name: str = Field(..., description="Posture check name")
    description: str = Field(..., description="Posture check description")
    checks: Optional[Dict[str, Any]] = Field(
        None,
        description="Check configurations (nb_version_check, os_version_check, "
        "geo_location_check, peer_network_range_check, process_check)",
    )


class PostureCheckUpdate(BaseModel):
    """Model for updating a posture check."""

    name: Optional[str] = Field(None, description="Posture check name")
    description: Optional[str] = Field(None, description="Posture check description")
    checks: Optional[Dict[str, Any]] = Field(None, description="Check configurations")


class PostureCheck(BaseModel):
    """NetBird posture check model."""

    id: ResourceId = Field(..., description="Unique posture check identifier")
    name: str = Field(..., description="Posture check name")
    description: Optional[str] = Field(None, description="Posture check description")
    checks: Optional[Dict[str, Any]] = Field(None, description="Check configurations")
