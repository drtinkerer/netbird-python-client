"""
Users resource handler for NetBird API.
"""

from typing import Any, Dict, List, Optional

from ..models import UserCreate, UserInviteCreate, UserUpdate
from .base import BaseResource


class UsersResource(BaseResource):
    """Handler for NetBird users API endpoints.

    Provides methods to manage NetBird users including listing, creating,
    updating, deleting users, and managing user invitations.
    """

    def list(self) -> List[Dict[str, Any]]:
        """List all users.

        Returns:
            List of user dictionaries

        Example:
            >>> users = client.users.list()
            >>> for user in users:
            ...     print(f"{user['name']}: {user['email']}")
        """
        data = self.client.get("users")
        return self._parse_list_response(data)

    def create(self, user_data: UserCreate) -> Dict[str, Any]:
        """Create a new user.

        Args:
            user_data: User creation data

        Returns:
            Created user dictionary

        Example:
            >>> user_data = UserCreate(
            ...     email="john@example.com",
            ...     name="John Doe",
            ...     role="user"
            ... )
            >>> user = client.users.create(user_data)
        """
        data = self.client.post("users", data=user_data.model_dump(exclude_unset=True))
        return self._parse_response(data)

    def get(self, user_id: str) -> Dict[str, Any]:
        """Get a specific user by ID.

        Args:
            user_id: Unique user identifier

        Returns:
            User dictionary

        Example:
            >>> user = client.users.get("user-123")
            >>> print(f"User: {user['name']}")
        """
        data = self.client.get(f"users/{user_id}")
        return self._parse_response(data)

    def update(self, user_id: str, user_data: UserUpdate) -> Dict[str, Any]:
        """Update an existing user.

        Args:
            user_id: Unique user identifier
            user_data: User update data

        Returns:
            Updated user dictionary

        Example:
            >>> user_data = UserUpdate(name="John Smith")
            >>> user = client.users.update("user-123", user_data)
        """
        data = self.client.put(
            f"users/{user_id}", data=user_data.model_dump(exclude_unset=True)
        )
        return self._parse_response(data)

    def delete(self, user_id: str) -> None:
        """Delete a user.

        Args:
            user_id: Unique user identifier

        Example:
            >>> client.users.delete("user-123")
        """
        self.client.delete(f"users/{user_id}")

    def invite(self, user_id: str) -> None:
        """Resend user invitation.

        Args:
            user_id: Unique user identifier

        Example:
            >>> client.users.invite("user-123")
        """
        self.client.post(f"users/{user_id}/invite")

    def get_current(self) -> Dict[str, Any]:
        """Get the current authenticated user.

        Returns:
            Current user dictionary

        Example:
            >>> current_user = client.users.get_current()
            >>> print(f"Logged in as: {current_user['name']}")
        """
        data = self.client.get("users/current")
        return self._parse_response(data)

    def approve(self, user_id: str) -> Dict[str, Any]:
        """Approve a pending user.

        Args:
            user_id: Unique user identifier

        Returns:
            Approved user dictionary
        """
        data = self.client.post(f"users/{user_id}/approve")
        return self._parse_response(data)

    def reject(self, user_id: str) -> None:
        """Reject a pending user.

        Args:
            user_id: Unique user identifier
        """
        self.client.delete(f"users/{user_id}/reject")

    def change_password(
        self, user_id: str, old_password: str, new_password: str
    ) -> None:
        """Change a user's password.

        Args:
            user_id: Unique user identifier
            old_password: Current password
            new_password: New password
        """
        self.client.put(
            f"users/{user_id}/password",
            data={"old_password": old_password, "new_password": new_password},
        )

    def list_invites(self) -> List[Dict[str, Any]]:
        """List all user invites.

        Returns:
            List of invite dictionaries
        """
        data = self.client.get("users/invites")
        return self._parse_list_response(data)

    def create_invite(self, invite_data: UserInviteCreate) -> Dict[str, Any]:
        """Create a user invite.

        Args:
            invite_data: Invite creation data

        Returns:
            Created invite dictionary with token
        """
        data = self.client.post(
            "users/invites", data=invite_data.model_dump(exclude_unset=True)
        )
        return self._parse_response(data)

    def delete_invite(self, invite_id: str) -> None:
        """Delete a user invite.

        Args:
            invite_id: Unique invite identifier
        """
        self.client.delete(f"users/invites/{invite_id}")

    def regenerate_invite(
        self, invite_id: str, expires_in: Optional[int] = None
    ) -> Dict[str, Any]:
        """Regenerate a user invite token.

        Args:
            invite_id: Unique invite identifier
            expires_in: Optional new expiration in seconds

        Returns:
            Regenerated invite dictionary with new token
        """
        payload = {}
        if expires_in is not None:
            payload["expires_in"] = expires_in
        data = self.client.post(
            f"users/invites/{invite_id}/regenerate", data=payload or None
        )
        return self._parse_response(data)

    def get_invite_info(self, token: str) -> Dict[str, Any]:
        """Get public invite information by token.

        Args:
            token: Invite token

        Returns:
            Public invite details
        """
        data = self.client.get(f"users/invites/{token}")
        return self._parse_response(data)

    def accept_invite(self, token: str, password: str) -> Dict[str, Any]:
        """Accept a user invite.

        Args:
            token: Invite token
            password: Password for the new account

        Returns:
            Acceptance confirmation
        """
        data = self.client.post(
            f"users/invites/{token}/accept", data={"password": password}
        )
        return self._parse_response(data)
