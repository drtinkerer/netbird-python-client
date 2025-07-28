"""
Routes resource handler for NetBird API.
"""

from typing import Dict, List, Any

from ..models import RouteCreate, RouteUpdate
from .base import BaseResource


class RoutesResource(BaseResource):
    """Handler for NetBird routes API endpoints.
    
    Provides methods to manage NetBird network routes including
    listing, creating, retrieving, updating, and deleting routes.
    """
    
    def list(self) -> List[Dict[str, Any]]:
        """List all routes.
        
        Returns:
            List of route dictionaries
            
        Example:
            >>> routes = client.routes.list()
            >>> for route in routes:
            ...     print(f"Route: {route.network} (Enabled: {route.enabled})")
        """
        data = self.client.get("routes")
        return self._parse_list_response(data)
    
    def create(self, route_data: RouteCreate) -> Dict[str, Any]:
        """Create a new route.
        
        Args:
            route_data: Route creation data
            
        Returns:
            Created route dictionary
            
        Example:
            >>> route_data = RouteCreate(
            ...     description="Internal network route",
            ...     network_id="192.168.1.0/24",
            ...     network_type="ipv4",
            ...     peer="peer-123",
            ...     metric=100
            ... )
            >>> route = client.routes.create(route_data)
        """
        data = self.client.post(
            "routes",
            data=route_data.model_dump(exclude_unset=True)
        )
        return self._parse_response(data)
    
    def get(self, route_id: str) -> Dict[str, Any]:
        """Retrieve a specific route.
        
        Args:
            route_id: Unique route identifier
            
        Returns:
            Route dictionary
            
        Example:
            >>> route = client.routes.get("route-123")
            >>> print(f"Route: {route.network}")
        """
        data = self.client.get(f"routes/{route_id}")
        return self._parse_response(data)
    
    def update(self, route_id: str, route_data: RouteUpdate) -> Dict[str, Any]:
        """Update a route.
        
        Args:
            route_id: Unique route identifier
            route_data: Route update data
            
        Returns:
            Updated route dictionary
            
        Example:
            >>> route_data = RouteUpdate(
            ...     enabled=False,
            ...     description="Route disabled for maintenance"
            ... )
            >>> route = client.routes.update("route-123", route_data)
        """
        data = self.client.put(
            f"routes/{route_id}",
            data=route_data.model_dump(exclude_unset=True)
        )
        return self._parse_response(data)
    
    def delete(self, route_id: str) -> None:
        """Delete a route.
        
        Args:
            route_id: Unique route identifier
            
        Example:
            >>> client.routes.delete("route-123")
        """
        self.client.delete(f"routes/{route_id}")
