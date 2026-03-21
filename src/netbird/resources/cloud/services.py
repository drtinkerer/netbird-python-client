"""
Services (reverse proxy) resource handler for NetBird API.
"""

from typing import Any, Dict, List

from ...models.cloud.service import ServiceCreate, ServiceDomainCreate, ServiceUpdate
from ..base import BaseResource


class ServicesResource(BaseResource):
    """Handler for NetBird reverse proxy services API endpoints."""

    def list(self) -> List[Dict[str, Any]]:
        """List all services."""
        data = self.client.get("reverse-proxies/services")
        return self._parse_list_response(data)

    def create(self, service_data: ServiceCreate) -> Dict[str, Any]:
        """Create a new service."""
        data = self.client.post(
            "reverse-proxies/services",
            data=service_data.model_dump(exclude_unset=True),
        )
        return self._parse_response(data)

    def get(self, service_id: str) -> Dict[str, Any]:
        """Retrieve a specific service."""
        data = self.client.get(f"reverse-proxies/services/{service_id}")
        return self._parse_response(data)

    def update(self, service_id: str, service_data: ServiceUpdate) -> Dict[str, Any]:
        """Update a service."""
        data = self.client.put(
            f"reverse-proxies/services/{service_id}",
            data=service_data.model_dump(exclude_unset=True),
        )
        return self._parse_response(data)

    def delete(self, service_id: str) -> None:
        """Delete a service."""
        self.client.delete(f"reverse-proxies/services/{service_id}")

    def list_clusters(self) -> List[Dict[str, Any]]:
        """List available proxy clusters."""
        data = self.client.get("reverse-proxies/clusters")
        return self._parse_list_response(data)

    def list_domains(self) -> List[Dict[str, Any]]:
        """List service domains."""
        data = self.client.get("reverse-proxies/domains")
        return self._parse_list_response(data)

    def create_domain(self, domain_data: ServiceDomainCreate) -> Dict[str, Any]:
        """Create a custom domain."""
        data = self.client.post(
            "reverse-proxies/domains",
            data=domain_data.model_dump(exclude_unset=True),
        )
        return self._parse_response(data)

    def delete_domain(self, domain_id: str) -> None:
        """Delete a custom domain."""
        self.client.delete(f"reverse-proxies/domains/{domain_id}")

    def validate_domain(self, domain_id: str) -> Dict[str, Any]:
        """Validate a custom domain."""
        data = self.client.get(f"reverse-proxies/domains/{domain_id}/validate")
        return self._parse_response(data)
