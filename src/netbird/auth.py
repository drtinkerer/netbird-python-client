"""
NetBird API Authentication

Handles token-based authentication for the NetBird API.
"""

from typing import Dict, Literal

AuthScheme = Literal["Token", "Bearer"]


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

    def __init__(self, token: str, scheme: AuthScheme = "Token") -> None:
        token = (token or "").strip()
        if not token:
            raise ValueError("Token cannot be empty")
        if scheme not in ("Token", "Bearer"):
            raise ValueError("Authentication scheme must be 'Token' or 'Bearer'")
        self.token = token
        self.scheme = scheme

    def get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers for API requests.

        Returns:
            Dictionary containing the Authorization header
        """
        return {"Authorization": f"{self.scheme} {self.token}"}

    def __repr__(self) -> str:
        masked_token = f"{self.token[:8]}..." if len(self.token) > 8 else "***"
        # Preserve the historical representation for compatibility. The
        # authentication scheme is intentionally omitted to avoid exposing
        # more credential metadata than older callers expect.
        return f"TokenAuth(token={masked_token})"
