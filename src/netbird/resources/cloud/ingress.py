"""
Ingress resource handler for NetBird API.
"""

from typing import Any, Dict, List

from ...models.cloud.ingress import (
    IngressPeerCreate,
    IngressPeerUpdate,
    PortAllocationCreate,
    PortAllocationUpdate,
)
from ..base import BaseResource


class IngressResource(BaseResource):
    """Handler for NetBird ingress ports API endpoints."""

    # Port allocations (scoped under peers)

    def list_ports(self, peer_id: str) -> List[Dict[str, Any]]:
        """List all port allocations for a peer."""
        data = self.client.get(f"peers/{peer_id}/ingress/ports")
        return self._parse_list_response(data)

    def create_port(
        self, peer_id: str, port_data: PortAllocationCreate
    ) -> Dict[str, Any]:
        """Create a port allocation for a peer."""
        data = self.client.post(
            f"peers/{peer_id}/ingress/ports",
            data=port_data.model_dump(exclude_unset=True),
        )
        return self._parse_response(data)

    def get_port(self, peer_id: str, allocation_id: str) -> Dict[str, Any]:
        """Retrieve a specific port allocation."""
        data = self.client.get(f"peers/{peer_id}/ingress/ports/{allocation_id}")
        return self._parse_response(data)

    def update_port(
        self, peer_id: str, allocation_id: str, port_data: PortAllocationUpdate
    ) -> Dict[str, Any]:
        """Update a port allocation."""
        data = self.client.put(
            f"peers/{peer_id}/ingress/ports/{allocation_id}",
            data=port_data.model_dump(exclude_unset=True),
        )
        return self._parse_response(data)

    def delete_port(self, peer_id: str, allocation_id: str) -> None:
        """Delete a port allocation."""
        self.client.delete(f"peers/{peer_id}/ingress/ports/{allocation_id}")

    # Ingress peers

    def list_peers(self) -> List[Dict[str, Any]]:
        """List all ingress peers."""
        data = self.client.get("ingress/peers")
        return self._parse_list_response(data)

    def create_peer(self, peer_data: IngressPeerCreate) -> Dict[str, Any]:
        """Create an ingress peer."""
        data = self.client.post(
            "ingress/peers", data=peer_data.model_dump(exclude_unset=True)
        )
        return self._parse_response(data)

    def get_peer(self, ingress_peer_id: str) -> Dict[str, Any]:
        """Retrieve a specific ingress peer."""
        data = self.client.get(f"ingress/peers/{ingress_peer_id}")
        return self._parse_response(data)

    def update_peer(
        self, ingress_peer_id: str, peer_data: IngressPeerUpdate
    ) -> Dict[str, Any]:
        """Update an ingress peer."""
        data = self.client.put(
            f"ingress/peers/{ingress_peer_id}",
            data=peer_data.model_dump(exclude_unset=True),
        )
        return self._parse_response(data)

    def delete_peer(self, ingress_peer_id: str) -> None:
        """Delete an ingress peer."""
        self.client.delete(f"ingress/peers/{ingress_peer_id}")
