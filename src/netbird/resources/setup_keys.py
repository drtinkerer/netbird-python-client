"""
Setup keys resource handler for NetBird API.
"""

from typing import Dict, List, Any

from ..models import SetupKeyCreate, SetupKeyUpdate
from .base import BaseResource


class SetupKeysResource(BaseResource):
    """Handler for NetBird setup keys API endpoints.
    
    Provides methods to manage NetBird setup keys including listing,
    creating, retrieving, updating, and deleting setup keys.
    """
    
    def list(self) -> List[Dict[str, Any]]:
        """List all setup keys.
        
        Returns:
            List of setup key dictionaries
            
        Example:
            >>> keys = client.setup_keys.list()
            >>> for key in keys:
            ...     print(f"Key: {key['name']} (Type: {key['type']})")
        """
        data = self.client.get("setup-keys")
        return self._parse_list_response(data)
    
    def create(self, key_data: SetupKeyCreate) -> Dict[str, Any]:
        """Create a new setup key.
        
        Args:
            key_data: Setup key creation data
            
        Returns:
            Created setup key dictionary
            
        Example:
            >>> key_data = SetupKeyCreate(
            ...     name="Development Key",
            ...     type="reusable",
            ...     expires_in=86400,  # 24 hours
            ...     usage_limit=10
            ... )
            >>> key = client.setup_keys.create(key_data)
        """
        data = self.client.post(
            "setup-keys",
            data=key_data.model_dump(exclude_unset=True)
        )
        return self._parse_response(data)
    
    def get(self, key_id: str) -> Dict[str, Any]:
        """Retrieve a specific setup key.
        
        Args:
            key_id: Unique setup key identifier
            
        Returns:
            Setup key dictionary
            
        Example:
            >>> key = client.setup_keys.get("key-123")
            >>> print(f"Key: {key['name']} - Valid: {key['valid']}")
        """
        data = self.client.get(f"setup-keys/{key_id}")
        return self._parse_response(data)
    
    def update(self, key_id: str, key_data: SetupKeyUpdate) -> Dict[str, Any]:
        """Update a setup key.
        
        Args:
            key_id: Unique setup key identifier
            key_data: Setup key update data
            
        Returns:
            Updated setup key dictionary
            
        Example:
            >>> key_data = SetupKeyUpdate(revoked=True)
            >>> key = client.setup_keys.update("key-123", key_data)
        """
        data = self.client.put(
            f"setup-keys/{key_id}",
            data=key_data.model_dump(exclude_unset=True)
        )
        return self._parse_response(data)
    
    def delete(self, key_id: str) -> None:
        """Delete a setup key.
        
        Args:
            key_id: Unique setup key identifier
            
        Example:
            >>> client.setup_keys.delete("key-123")
        """
        self.client.delete(f"setup-keys/{key_id}")
