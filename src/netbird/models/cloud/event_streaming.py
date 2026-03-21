"""
Event streaming models for NetBird API.
"""

from typing import Any, Dict, Optional

from pydantic import Field

from ..common import BaseModel, ResourceId


class EventStreamingCreate(BaseModel):
    """Model for creating an event streaming integration."""

    platform: str = Field(..., description="Streaming platform (datadog, s3, firehose)")
    config: Dict[str, Any] = Field(..., description="Platform-specific configuration")
    enabled: bool = Field(..., description="Integration enabled status")


class EventStreamingUpdate(BaseModel):
    """Model for updating an event streaming integration."""

    config: Optional[Dict[str, Any]] = Field(None, description="Configuration")
    enabled: Optional[bool] = Field(None, description="Integration enabled status")


class EventStreamingIntegration(BaseModel):
    """NetBird event streaming integration model."""

    id: ResourceId = Field(..., description="Unique integration identifier")
    platform: Optional[str] = Field(None, description="Streaming platform")
    config: Optional[Dict[str, Any]] = Field(None, description="Configuration")
    enabled: Optional[bool] = Field(None, description="Integration enabled status")
