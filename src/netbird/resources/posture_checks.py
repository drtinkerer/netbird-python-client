"""
Posture checks resource handler for NetBird API.
"""

from typing import Any, Dict, List

from ..models.posture_check import PostureCheckCreate, PostureCheckUpdate
from .base import BaseResource


class PostureChecksResource(BaseResource):
    """Handler for NetBird posture checks API endpoints."""

    def list(self) -> List[Dict[str, Any]]:
        """List all posture checks.

        Returns:
            List of posture check dictionaries
        """
        data = self.client.get("posture-checks")
        return self._parse_list_response(data)

    def create(self, check_data: PostureCheckCreate) -> Dict[str, Any]:
        """Create a new posture check.

        Args:
            check_data: Posture check creation data

        Returns:
            Created posture check dictionary
        """
        data = self.client.post(
            "posture-checks", data=check_data.model_dump(exclude_unset=True)
        )
        return self._parse_response(data)

    def get(self, check_id: str) -> Dict[str, Any]:
        """Retrieve a specific posture check.

        Args:
            check_id: Unique posture check identifier

        Returns:
            Posture check dictionary
        """
        data = self.client.get(f"posture-checks/{check_id}")
        return self._parse_response(data)

    def update(self, check_id: str, check_data: PostureCheckUpdate) -> Dict[str, Any]:
        """Update a posture check.

        Args:
            check_id: Unique posture check identifier
            check_data: Posture check update data

        Returns:
            Updated posture check dictionary
        """
        data = self.client.put(
            f"posture-checks/{check_id}",
            data=check_data.model_dump(exclude_unset=True),
        )
        return self._parse_response(data)

    def delete(self, check_id: str) -> None:
        """Delete a posture check.

        Args:
            check_id: Unique posture check identifier
        """
        self.client.delete(f"posture-checks/{check_id}")
