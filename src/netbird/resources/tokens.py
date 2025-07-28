"""
Tokens resource handler for NetBird API.
"""

from typing import Dict, List, Any

from ..models import TokenCreate
from .base import BaseResource


class TokensResource(BaseResource):
    """Handler for NetBird tokens API endpoints.
    
    Provides methods to manage user API tokens including listing,
    creating, retrieving, and deleting tokens.
    """
    
    def list(self, user_id: str) -> List[Dict[str, Any]]:
        """List all tokens for a user.
        
        Args:
            user_id: Unique user identifier
            
        Returns:
            List of token dictionaries
            
        Example:
            >>> tokens = client.tokens.list("user-123")
            >>> for token in tokens:
            ...     print(f"Token: {token.name}")
        """
        data = self.client.get(f"users/{user_id}/tokens")
        return self._parse_list_response(data)
    
    def create(self, user_id: str, token_data: TokenCreate) -> Dict[str, Any]:
        """Create a new token for a user.
        
        Args:
            user_id: Unique user identifier
            token_data: Token creation data
            
        Returns:
            Created token dictionary
            
        Example:
            >>> token_data = TokenCreate(
            ...     name="API Access Token",
            ...     expires_in=30  # 30 days
            ... )
            >>> token = client.tokens.create("user-123", token_data)
        """
        data = self.client.post(
            f"users/{user_id}/tokens",
            data=token_data.model_dump()
        )
        return self._parse_response(data)
    
    def get(self, user_id: str, token_id: str) -> Dict[str, Any]:
        """Retrieve a specific token.
        
        Args:
            user_id: Unique user identifier
            token_id: Unique token identifier
            
        Returns:
            Token dictionary
            
        Example:
            >>> token = client.tokens.get("user-123", "token-456")
            >>> print(f"Token expires: {token.expiration_date}")
        """
        data = self.client.get(f"users/{user_id}/tokens/{token_id}")
        return self._parse_response(data)
    
    def delete(self, user_id: str, token_id: str) -> None:
        """Delete a token.
        
        Args:
            user_id: Unique user identifier
            token_id: Unique token identifier
            
        Example:
            >>> client.tokens.delete("user-123", "token-456")
        """
        self.client.delete(f"users/{user_id}/tokens/{token_id}")
