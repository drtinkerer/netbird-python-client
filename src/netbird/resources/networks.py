"""
Networks resource handler for NetBird API.
"""

from typing import List

from ..models import Network, NetworkCreate, NetworkResource, NetworkRouter, NetworkUpdate
from .base import BaseResource


class NetworksResource(BaseResource):
    """Handler for NetBird networks API endpoints.
    
    Provides methods to manage NetBird networks including listing,
    creating, retrieving, updating, and deleting networks, as well as
    managing network resources and routers.
    """
    
    def list(self) -> List[Network]:
        """List all networks.
        
        Returns:
            List of Network objects
            
        Example:
            >>> networks = client.networks.list()
            >>> for network in networks:
            ...     print(f"Network: {network.name}")
        """
        data = self.client.get("networks")
        return self._parse_list_response(data, Network)
    
    def create(self, network_data: NetworkCreate) -> Network:
        """Create a new network.
        
        Args:
            network_data: Network creation data
            
        Returns:
            Created Network object
            
        Example:
            >>> network_data = NetworkCreate(
            ...     name="Production Network",
            ...     description="Main production environment"
            ... )
            >>> network = client.networks.create(network_data)
        """
        data = self.client.post(
            "networks",
            data=network_data.model_dump(exclude_unset=True)
        )
        return self._parse_response(data, Network)
    
    def get(self, network_id: str) -> Network:
        """Retrieve a specific network.
        
        Args:
            network_id: Unique network identifier
            
        Returns:
            Network object
            
        Example:
            >>> network = client.networks.get("network-123")
            >>> print(f"Network: {network.name}")
        """
        data = self.client.get(f"networks/{network_id}")
        return self._parse_response(data, Network)
    
    def update(self, network_id: str, network_data: NetworkUpdate) -> Network:
        """Update a network.
        
        Args:
            network_id: Unique network identifier
            network_data: Network update data
            
        Returns:
            Updated Network object
            
        Example:
            >>> network_data = NetworkUpdate(
            ...     name="Updated Production Network"
            ... )
            >>> network = client.networks.update("network-123", network_data)
        """
        data = self.client.put(
            f"networks/{network_id}",
            data=network_data.model_dump(exclude_unset=True)
        )
        return self._parse_response(data, Network)
    
    def delete(self, network_id: str) -> None:
        """Delete a network.
        
        Args:
            network_id: Unique network identifier
            
        Example:
            >>> client.networks.delete("network-123")
        """
        self.client.delete(f"networks/{network_id}")
    
    # Network Resources
    
    def list_resources(self, network_id: str) -> List[NetworkResource]:
        """List all resources in a network.
        
        Args:
            network_id: Unique network identifier
            
        Returns:
            List of NetworkResource objects
            
        Example:
            >>> resources = client.networks.list_resources("network-123")
        """
        data = self.client.get(f"networks/{network_id}/resources")
        return self._parse_list_response(data, NetworkResource)
    
    def create_resource(self, network_id: str, resource_data: dict) -> NetworkResource:
        """Create a network resource.
        
        Args:
            network_id: Unique network identifier
            resource_data: Resource creation data
            
        Returns:
            Created NetworkResource object
        """
        data = self.client.post(f"networks/{network_id}/resources", data=resource_data)
        return self._parse_response(data, NetworkResource)
    
    def get_resource(self, network_id: str, resource_id: str) -> NetworkResource:
        """Get a specific network resource.
        
        Args:
            network_id: Unique network identifier
            resource_id: Unique resource identifier
            
        Returns:
            NetworkResource object
        """
        data = self.client.get(f"networks/{network_id}/resources/{resource_id}")
        return self._parse_response(data, NetworkResource)
    
    def update_resource(self, network_id: str, resource_id: str, resource_data: dict) -> NetworkResource:
        """Update a network resource.
        
        Args:
            network_id: Unique network identifier
            resource_id: Unique resource identifier
            resource_data: Resource update data
            
        Returns:
            Updated NetworkResource object
        """
        data = self.client.put(f"networks/{network_id}/resources/{resource_id}", data=resource_data)
        return self._parse_response(data, NetworkResource)
    
    def delete_resource(self, network_id: str, resource_id: str) -> None:
        """Delete a network resource.
        
        Args:
            network_id: Unique network identifier
            resource_id: Unique resource identifier
        """
        self.client.delete(f"networks/{network_id}/resources/{resource_id}")
    
    # Network Routers
    
    def list_routers(self, network_id: str) -> List[NetworkRouter]:
        """List all routers in a network.
        
        Args:
            network_id: Unique network identifier
            
        Returns:
            List of NetworkRouter objects
        """
        data = self.client.get(f"networks/{network_id}/routers")
        return self._parse_list_response(data, NetworkRouter)
    
    def create_router(self, network_id: str, router_data: dict) -> NetworkRouter:
        """Create a network router.
        
        Args:
            network_id: Unique network identifier
            router_data: Router creation data
            
        Returns:
            Created NetworkRouter object
        """
        data = self.client.post(f"networks/{network_id}/routers", data=router_data)
        return self._parse_response(data, NetworkRouter)
    
    def get_router(self, network_id: str, router_id: str) -> NetworkRouter:
        """Get a specific network router.
        
        Args:
            network_id: Unique network identifier
            router_id: Unique router identifier
            
        Returns:
            NetworkRouter object
        """
        data = self.client.get(f"networks/{network_id}/routers/{router_id}")
        return self._parse_response(data, NetworkRouter)
    
    def update_router(self, network_id: str, router_id: str, router_data: dict) -> NetworkRouter:
        """Update a network router.
        
        Args:
            network_id: Unique network identifier
            router_id: Unique router identifier
            router_data: Router update data
            
        Returns:
            Updated NetworkRouter object
        """
        data = self.client.put(f"networks/{network_id}/routers/{router_id}", data=router_data)
        return self._parse_response(data, NetworkRouter)
    
    def delete_router(self, network_id: str, router_id: str) -> None:
        """Delete a network router.
        
        Args:
            network_id: Unique network identifier
            router_id: Unique router identifier
        """
        self.client.delete(f"networks/{network_id}/routers/{router_id}")
