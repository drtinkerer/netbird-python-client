"""
Setup keys resource handler for NetBird API.
"""

from typing import List

from ..models import SetupKey, SetupKeyCreate, SetupKeyUpdate
from .base import BaseResource


class SetupKeysResource(BaseResource):
    """Handler for NetBird setup keys API endpoints.
    
    Provides methods to manage NetBird setup keys including listing,
    creating, retrieving, updating, and deleting setup keys.
    """
    
    def list(self) -> List[SetupKey]:
        """List all setup keys.
        
        Returns:
            List of SetupKey objects
            
        Example:
            >>> keys = client.setup_keys.list()
            >>> for key in keys:
            ...     print(f"Key: {key.name} (Type: {key.type})")
        """
        data = self.client.get("setup-keys")
        return self._parse_list_response(data, SetupKey)
    
    def create(self, key_data: SetupKeyCreate) -> SetupKey:
        """Create a new setup key.
        
        Args:
            key_data: Setup key creation data
            
        Returns:
            Created SetupKey object
            
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
        return self._parse_response(data, SetupKey)
    
    def get(self, key_id: str) -> SetupKey:
        """Retrieve a specific setup key.
        
        Args:
            key_id: Unique setup key identifier
            
        Returns:
            SetupKey object
            
        Example:
            >>> key = client.setup_keys.get("key-123")
            >>> print(f"Key: {key.name} - Valid: {key.valid}")
        """
        data = self.client.get(f"setup-keys/{key_id}")
        return self._parse_response(data, SetupKey)
    
    def update(self, key_id: str, key_data: SetupKeyUpdate) -> SetupKey:
        """Update a setup key.
        
        Args:
            key_id: Unique setup key identifier
            key_data: Setup key update data
            
        Returns:
            Updated SetupKey object
            
        Example:
            >>> key_data = SetupKeyUpdate(revoked=True)
            >>> key = client.setup_keys.update("key-123", key_data)
        """
        data = self.client.put(
            f"setup-keys/{key_id}",
            data=key_data.model_dump(exclude_unset=True)
        )
        return self._parse_response(data, SetupKey)
    
    def delete(self, key_id: str) -> None:
        """Delete a setup key.
        
        Args:
            key_id: Unique setup key identifier
            
        Example:
            >>> client.setup_keys.delete("key-123")
        """
        self.client.delete(f"setup-keys/{key_id}")
