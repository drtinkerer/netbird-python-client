"""
Groups resource handler for NetBird API.
"""

from typing import Dict, List, Any

from ..models import GroupCreate, GroupUpdate
from .base import BaseResource


class GroupsResource(BaseResource):
    """Handler for NetBird groups API endpoints.
    
    Provides methods to manage NetBird groups including listing,
    creating, retrieving, updating, and deleting groups.
    """
    
    def list(self) -> List[Dict[str, Any]]:
        """List all groups.
        
        Returns:
            List of group dictionaries
            
        Example:
            >>> groups = client.groups.list()
            >>> for group in groups:
            ...     print(f"Group: {group.name} ({group.peers_count} peers)")
        """
        data = self.client.get("groups")
        return self._parse_list_response(data)
    
    def create(self, group_data: GroupCreate) -> Dict[str, Any]:
        """Create a new group.
        
        Args:
            group_data: Group creation data
            
        Returns:
            Created group dictionary
            
        Example:
            >>> group_data = GroupCreate(
            ...     name="Developers",
            ...     peers=["peer-1", "peer-2"]
            ... )
            >>> group = client.groups.create(group_data)
        """
        data = self.client.post(
            "groups",
            data=group_data.model_dump(exclude_unset=True)
        )
        return self._parse_response(data)
    
    def get(self, group_id: str) -> Dict[str, Any]:
        """Retrieve a specific group.
        
        Args:
            group_id: Unique group identifier
            
        Returns:
            Group dictionary
            
        Example:
            >>> group = client.groups.get("group-123")
            >>> print(f"Group: {group.name}")
        """
        data = self.client.get(f"groups/{group_id}")
        return self._parse_response(data)
    
    def update(self, group_id: str, group_data: GroupUpdate) -> Dict[str, Any]:
        """Update a group.
        
        Args:
            group_id: Unique group identifier
            group_data: Group update data
            
        Returns:
            Updated group dictionary
            
        Example:
            >>> group_data = GroupUpdate(
            ...     name="Senior Developers",
            ...     peers=["peer-1", "peer-2", "peer-3"]
            ... )
            >>> group = client.groups.update("group-123", group_data)
        """
        data = self.client.put(
            f"groups/{group_id}",
            data=group_data.model_dump(exclude_unset=True)
        )
        return self._parse_response(data)
    
    def delete(self, group_id: str) -> None:
        """Delete a group.
        
        Args:
            group_id: Unique group identifier
            
        Example:
            >>> client.groups.delete("group-123")
        """
        self.client.delete(f"groups/{group_id}")
