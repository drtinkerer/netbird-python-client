"""
User models for NetBird API.
"""

from typing import Any, Dict, List, Optional

from pydantic import EmailStr, Field

from .common import BaseModel, ResourceId, UserRole, UserStatus


class UserCreate(BaseModel):
    """Model for creating a new user.

    Attributes:
        email: User email address
        name: User display name
        role: User role (admin, user, owner)
        auto_groups: List of group IDs to auto-assign
        is_service_user: Whether this is a service user
        is_blocked: Whether the user is blocked
    """

    email: EmailStr = Field(..., description="User email address")
    name: Optional[str] = Field(None, description="User display name")
    role: UserRole = Field(UserRole.USER, description="User role")
    auto_groups: Optional[List[ResourceId]] = Field(
        None, description="Auto-assigned group IDs"
    )
    is_service_user: bool = Field(False, description="Service user flag")
    is_blocked: bool = Field(False, description="Blocked status")


class UserUpdate(BaseModel):
    """Model for updating an existing user.

    Attributes:
        name: User display name
        role: User role
        auto_groups: List of group IDs to auto-assign
        is_blocked: Whether the user is blocked
    """

    name: Optional[str] = Field(None, description="User display name")
    role: Optional[UserRole] = Field(None, description="User role")
    auto_groups: Optional[List[ResourceId]] = Field(
        None, description="Auto-assigned group IDs"
    )
    is_blocked: Optional[bool] = Field(None, description="Blocked status")


class User(BaseModel):
    """NetBird user model.

    Attributes:
        id: Unique user identifier
        email: User email address
        name: User display name
        role: User role
        status: User status (active, disabled, invited)
        auto_groups: List of auto-assigned group IDs
        is_service_user: Whether this is a service user
        is_blocked: Whether the user is blocked
        issued: When the user was created
        permissions: User permissions
        is_current: Whether this is the current user (from get_current endpoint)
        last_login: Last login timestamp
    """

    id: ResourceId = Field(..., description="Unique user identifier")
    email: Optional[str] = Field(None, description="User email address")
    name: Optional[str] = Field(None, description="User display name")
    role: UserRole = Field(..., description="User role")
    status: UserStatus = Field(..., description="User status")
    auto_groups: Optional[List[ResourceId]] = Field(
        None, description="Auto-assigned group IDs"
    )
    is_service_user: bool = Field(False, description="Service user flag")
    is_blocked: bool = Field(False, description="Blocked status")
    issued: Optional[str] = Field(None, description="User creation timestamp")
    permissions: Optional[Dict[str, Any]] = Field(None, description="User permissions")
    is_current: Optional[bool] = Field(
        None, description="Whether this is the current user"
    )
    last_login: Optional[str] = Field(None, description="Last login timestamp")


class UserInviteCreate(BaseModel):
    """Model for creating a user invite."""

    email: str = Field(..., description="Invitee email address")
    name: str = Field(..., description="Invitee display name")
    role: UserRole = Field(..., description="Role to assign")
    auto_groups: List[ResourceId] = Field(..., description="Auto-assigned group IDs")
    expires_in: Optional[int] = Field(None, description="Expiration in seconds")


class UserInvite(BaseModel):
    """User invite model."""

    id: ResourceId = Field(..., description="Unique invite identifier")
    email: str = Field(..., description="Invitee email address")
    name: str = Field(..., description="Invitee display name")
    role: UserRole = Field(..., description="Assigned role")
    expires_at: Optional[str] = Field(None, description="Expiration timestamp")
    token: Optional[str] = Field(None, description="Invite token")
    invited_by: Optional[str] = Field(None, description="Inviter identifier")
    valid: Optional[bool] = Field(None, description="Whether invite is still valid")
