"""
Instance resource handler for NetBird API.
"""

from typing import Any, Dict

from .base import BaseResource


class InstanceResource(BaseResource):
    """Handler for NetBird instance API endpoints.

    Note: These endpoints do not require authentication. The APIClient
    will still send auth headers (the server ignores them).
    """

    def get_status(self) -> Dict[str, Any]:
        """Get instance status.

        Returns:
            Instance status dictionary
        """
        data = self.client.get("instance")
        return self._parse_response(data)

    def get_version(self) -> Dict[str, Any]:
        """Get version information.

        Returns:
            Version information dictionary
        """
        data = self.client.get("instance/version")
        return self._parse_response(data)

    def setup(self, email: str, password: str, name: str) -> Dict[str, Any]:
        """Setup the instance with initial admin user.

        Args:
            email: Email address for the admin user
            password: Password for the admin user (minimum 8 characters)
            name: Display name for the admin user

        Returns:
            Setup confirmation dictionary
        """
        # Note: uses /setup path, not /instance/setup
        data = self.client.post(
            "setup",
            data={"email": email, "password": password, "name": name},
        )
        return self._parse_response(data)
