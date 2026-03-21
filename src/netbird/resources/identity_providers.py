"""
Identity providers resource handler for NetBird API.
"""

from typing import Any, Dict, List

from ..models.identity_provider import IdentityProviderCreate, IdentityProviderUpdate
from .base import BaseResource


class IdentityProvidersResource(BaseResource):
    """Handler for NetBird identity providers API endpoints."""

    def list(self) -> List[Dict[str, Any]]:
        """List all identity providers.

        Returns:
            List of identity provider dictionaries
        """
        data = self.client.get("identity-providers")
        return self._parse_list_response(data)

    def create(self, provider_data: IdentityProviderCreate) -> Dict[str, Any]:
        """Create a new identity provider.

        Args:
            provider_data: Identity provider creation data

        Returns:
            Created identity provider dictionary
        """
        data = self.client.post(
            "identity-providers",
            data=provider_data.model_dump(exclude_unset=True),
        )
        return self._parse_response(data)

    def get(self, provider_id: str) -> Dict[str, Any]:
        """Retrieve a specific identity provider.

        Args:
            provider_id: Unique identity provider identifier

        Returns:
            Identity provider dictionary
        """
        data = self.client.get(f"identity-providers/{provider_id}")
        return self._parse_response(data)

    def update(
        self, provider_id: str, provider_data: IdentityProviderUpdate
    ) -> Dict[str, Any]:
        """Update an identity provider.

        Args:
            provider_id: Unique identity provider identifier
            provider_data: Identity provider update data

        Returns:
            Updated identity provider dictionary
        """
        data = self.client.put(
            f"identity-providers/{provider_id}",
            data=provider_data.model_dump(exclude_unset=True),
        )
        return self._parse_response(data)

    def delete(self, provider_id: str) -> None:
        """Delete an identity provider.

        Args:
            provider_id: Unique identity provider identifier
        """
        self.client.delete(f"identity-providers/{provider_id}")
