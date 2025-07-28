"""
Networks resource handler for NetBird API.
"""

from typing import Any, Dict, List

from ..models import NetworkCreate, NetworkUpdate
from .base import BaseResource


class NetworksResource(BaseResource):
    """Handler for NetBird networks API endpoints.

    Provides methods to manage NetBird networks including listing,
    creating, retrieving, updating, and deleting networks, as well as
    managing network resources and routers.
    """

    def list(self) -> List[Dict[str, Any]]:
        """List all networks.

        Returns:
            List of network dictionaries

        Example:
            >>> networks = client.networks.list()
            >>> for network in networks:
            ...     print(f"Network: {network['name']}")
        """
        data = self.client.get("networks")
        return self._parse_list_response(data)

    def create(self, network_data: NetworkCreate) -> Dict[str, Any]:
        """Create a new network.

        Args:
            network_data: Network creation data

        Returns:
            Created network dictionary

        Example:
            >>> network_data = NetworkCreate(
            ...     name="Production Network",
            ...     description="Main production environment"
            ... )
            >>> network = client.networks.create(network_data)
        """
        data = self.client.post(
            "networks", data=network_data.model_dump(exclude_unset=True)
        )
        return self._parse_response(data)

    def get(self, network_id: str) -> Dict[str, Any]:
        """Retrieve a specific network.

        Args:
            network_id: Unique network identifier

        Returns:
            Network dictionary

        Example:
            >>> network = client.networks.get("network-123")
            >>> print(f"Network: {network['name']}")
        """
        data = self.client.get(f"networks/{network_id}")
        return self._parse_response(data)

    def update(self, network_id: str, network_data: NetworkUpdate) -> Dict[str, Any]:
        """Update a network.

        Args:
            network_id: Unique network identifier
            network_data: Network update data

        Returns:
            Updated network dictionary

        Example:
            >>> network_data = NetworkUpdate(
            ...     name="Updated Production Network"
            ... )
            >>> network = client.networks.update("network-123", network_data)
        """
        data = self.client.put(
            f"networks/{network_id}",
            data=network_data.model_dump(exclude_unset=True),
        )
        return self._parse_response(data)

    def delete(self, network_id: str) -> None:
        """Delete a network.

        Args:
            network_id: Unique network identifier

        Example:
            >>> client.networks.delete("network-123")
        """
        self.client.delete(f"networks/{network_id}")

    # Network Resources

    def list_resources(self, network_id: str) -> List[Dict[str, Any]]:
        """List all resources in a network.

        Args:
            network_id: Unique network identifier

        Returns:
            List of network resource dictionaries

        Example:
            >>> resources = client.networks.list_resources("network-123")
        """
        data = self.client.get(f"networks/{network_id}/resources")
        return self._parse_list_response(data)

    def create_resource(self, network_id: str, resource_data: dict) -> Dict[str, Any]:
        """Create a network resource.

        Args:
            network_id: Unique network identifier
            resource_data: Resource creation data

        Returns:
            Created network resource dictionary
        """
        data = self.client.post(f"networks/{network_id}/resources", data=resource_data)
        return self._parse_response(data)

    def get_resource(self, network_id: str, resource_id: str) -> Dict[str, Any]:
        """Get a specific network resource.

        Args:
            network_id: Unique network identifier
            resource_id: Unique resource identifier

        Returns:
            Network resource dictionary
        """
        data = self.client.get(f"networks/{network_id}/resources/{resource_id}")
        return self._parse_response(data)

    def update_resource(
        self, network_id: str, resource_id: str, resource_data: dict
    ) -> Dict[str, Any]:
        """Update a network resource.

        Args:
            network_id: Unique network identifier
            resource_id: Unique resource identifier
            resource_data: Resource update data

        Returns:
            Updated network resource dictionary
        """
        data = self.client.put(
            f"networks/{network_id}/resources/{resource_id}",
            data=resource_data,
        )
        return self._parse_response(data)

    def delete_resource(self, network_id: str, resource_id: str) -> None:
        """Delete a network resource.

        Args:
            network_id: Unique network identifier
            resource_id: Unique resource identifier
        """
        self.client.delete(f"networks/{network_id}/resources/{resource_id}")

    # Network Routers

    def list_routers(self, network_id: str) -> List[Dict[str, Any]]:
        """List all routers in a network.

        Args:
            network_id: Unique network identifier

        Returns:
            List of network router dictionaries
        """
        data = self.client.get(f"networks/{network_id}/routers")
        return self._parse_list_response(data)

    def create_router(self, network_id: str, router_data: dict) -> Dict[str, Any]:
        """Create a network router.

        Args:
            network_id: Unique network identifier
            router_data: Router creation data

        Returns:
            Created network router dictionary
        """
        data = self.client.post(f"networks/{network_id}/routers", data=router_data)
        return self._parse_response(data)

    def get_router(self, network_id: str, router_id: str) -> Dict[str, Any]:
        """Get a specific network router.

        Args:
            network_id: Unique network identifier
            router_id: Unique router identifier

        Returns:
            Network router dictionary
        """
        data = self.client.get(f"networks/{network_id}/routers/{router_id}")
        return self._parse_response(data)

    def update_router(
        self, network_id: str, router_id: str, router_data: dict
    ) -> Dict[str, Any]:
        """Update a network router.

        Args:
            network_id: Unique network identifier
            router_id: Unique router identifier
            router_data: Router update data

        Returns:
            Updated network router dictionary
        """
        data = self.client.put(
            f"networks/{network_id}/routers/{router_id}", data=router_data
        )
        return self._parse_response(data)

    def delete_router(self, network_id: str, router_id: str) -> None:
        """Delete a network router.

        Args:
            network_id: Unique network identifier
            router_id: Unique router identifier
        """
        self.client.delete(f"networks/{network_id}/routers/{router_id}")
