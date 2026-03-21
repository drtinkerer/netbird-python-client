"""
IDP/SCIM resource handler for NetBird API.
"""

from typing import Any, Dict, List

from ...models.cloud.idp_scim import SCIMIntegrationCreate, SCIMIntegrationUpdate
from ..base import BaseResource


class IDPScimResource(BaseResource):
    """Handler for NetBird IDP/SCIM integration API endpoints."""

    def list(self) -> List[Dict[str, Any]]:
        """List all SCIM IDP integrations."""
        data = self.client.get("integrations/scim-idp")
        return self._parse_list_response(data)

    def create(self, integration_data: SCIMIntegrationCreate) -> Dict[str, Any]:
        """Create a SCIM IDP integration."""
        data = self.client.post(
            "integrations/scim-idp",
            data=integration_data.model_dump(exclude_unset=True),
        )
        return self._parse_response(data)

    def get(self, integration_id: str) -> Dict[str, Any]:
        """Retrieve a specific SCIM IDP integration."""
        data = self.client.get(f"integrations/scim-idp/{integration_id}")
        return self._parse_response(data)

    def update(
        self, integration_id: str, integration_data: SCIMIntegrationUpdate
    ) -> Dict[str, Any]:
        """Update a SCIM IDP integration."""
        data = self.client.put(
            f"integrations/scim-idp/{integration_id}",
            data=integration_data.model_dump(exclude_unset=True),
        )
        return self._parse_response(data)

    def delete(self, integration_id: str) -> None:
        """Delete a SCIM IDP integration."""
        self.client.delete(f"integrations/scim-idp/{integration_id}")

    def regenerate_token(self, integration_id: str) -> Dict[str, Any]:
        """Regenerate SCIM token."""
        data = self.client.post(f"integrations/scim-idp/{integration_id}/token")
        return self._parse_response(data)

    def get_logs(self, integration_id: str) -> List[Dict[str, Any]]:
        """Get SCIM integration sync logs."""
        data = self.client.get(f"integrations/scim-idp/{integration_id}/logs")
        return self._parse_list_response(data)
