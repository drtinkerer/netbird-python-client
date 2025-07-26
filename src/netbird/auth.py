"""
NetBird API Authentication

Handles token-based authentication for the NetBird API.
"""

from typing import Dict


class TokenAuth:
    """Token-based authentication for NetBird API.
    
    NetBird uses token-based authentication with personal access tokens
    or service user tokens.
    
    Args:
        token: The API token to use for authentication
        
    Example:
        >>> auth = TokenAuth("your-api-token-here")
        >>> headers = auth.get_auth_headers()
        >>> print(headers)
        {'Authorization': 'Token your-api-token-here'}
    """
    
    def __init__(self, token: str) -> None:
        if not token:
            raise ValueError("Token cannot be empty")
        self.token = token.strip()
    
    def get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers for API requests.
        
        Returns:
            Dictionary containing the Authorization header
        """
        return {"Authorization": f"Token {self.token}"}
    
    def __repr__(self) -> str:
        masked_token = f"{self.token[:8]}..." if len(self.token) > 8 else "***"
        return f"TokenAuth(token={masked_token})"