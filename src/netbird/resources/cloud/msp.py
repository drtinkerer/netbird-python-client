"""
MSP resource handler for NetBird API.
"""

from typing import Any, Dict, List

from ...models.cloud.msp import MSPTenantCreate, MSPTenantUpdate
from ..base import BaseResource


class MSPResource(BaseResource):
    """Handler for NetBird MSP API endpoints."""

    def list_tenants(self) -> List[Dict[str, Any]]:
        """List all MSP tenants."""
        data = self.client.get("integrations/msp/tenants")
        return self._parse_list_response(data)

    def create_tenant(self, tenant_data: MSPTenantCreate) -> Dict[str, Any]:
        """Create an MSP tenant."""
        data = self.client.post(
            "integrations/msp/tenants",
            data=tenant_data.model_dump(exclude_unset=True),
        )
        return self._parse_response(data)

    def get_tenant(self, tenant_id: str) -> Dict[str, Any]:
        """Retrieve a specific MSP tenant."""
        data = self.client.get(f"integrations/msp/tenants/{tenant_id}")
        return self._parse_response(data)

    def update_tenant(
        self, tenant_id: str, tenant_data: MSPTenantUpdate
    ) -> Dict[str, Any]:
        """Update an MSP tenant."""
        data = self.client.put(
            f"integrations/msp/tenants/{tenant_id}",
            data=tenant_data.model_dump(exclude_unset=True),
        )
        return self._parse_response(data)

    def unlink_tenant(self, tenant_id: str, owner: str) -> Dict[str, Any]:
        """Unlink an MSP tenant."""
        data = self.client.post(
            f"integrations/msp/tenants/{tenant_id}/unlink",
            data={"owner": owner},
        )
        return self._parse_response(data)

    def verify_domain(self, tenant_id: str) -> Dict[str, Any]:
        """Verify domain DNS challenge for a tenant."""
        data = self.client.post(f"integrations/msp/tenants/{tenant_id}/dns")
        return self._parse_response(data)

    def create_subscription(self, tenant_id: str, price_id: str) -> Dict[str, Any]:
        """Create a subscription for a tenant."""
        data = self.client.post(
            f"integrations/msp/tenants/{tenant_id}/subscription",
            data={"priceID": price_id},
        )
        return self._parse_response(data)

    def invite_tenant(self, tenant_id: str) -> Dict[str, Any]:
        """Invite an existing account as tenant."""
        data = self.client.post(f"integrations/msp/tenants/{tenant_id}/invite")
        return self._parse_response(data)

    def respond_to_invite(self, tenant_id: str, value: str) -> Dict[str, Any]:
        """Respond to a tenant invitation (accept/decline)."""
        data = self.client.put(
            f"integrations/msp/tenants/{tenant_id}/invite",
            data={"value": value},
        )
        return self._parse_response(data)
