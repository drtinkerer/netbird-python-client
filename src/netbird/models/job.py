"""
Job models for NetBird API.
"""

from typing import Any, Dict, Optional

from pydantic import Field

from .common import BaseModel, ResourceId


class JobCreate(BaseModel):
    """Model for creating a job."""

    workload: Dict[str, Any] = Field(..., description="Job workload specification")


class Job(BaseModel):
    """NetBird job model."""

    id: ResourceId = Field(..., description="Unique job identifier")
    workload: Optional[Dict[str, Any]] = Field(None, description="Job workload")
    status: Optional[str] = Field(None, description="Job status")
