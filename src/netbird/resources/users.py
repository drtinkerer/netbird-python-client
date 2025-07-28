"""
Users resource handler for NetBird API.
"""

from typing import Any, Dict, List

from ..models import UserCreate, UserUpdate
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
