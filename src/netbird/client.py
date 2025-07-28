"""
NetBird API Client

Core client implementation for the NetBird API.
"""

import asyncio
from typing import Any, Dict, Optional, Union
from urllib.parse import urljoin, urlparse

import httpx
from httpx import Response

from .auth import TokenAuth
from .exceptions import (
    NetBirdAPIError,
    NetBirdAuthenticationError,
    NetBirdNotFoundError,
    NetBirdRateLimitError,
    NetBirdServerError,
    NetBirdValidationError,
)


class APIClient:
    """NetBird API Client.
    
    Provides access to all NetBird API resources including users, peers, groups,
    networks, policies, routes, DNS settings, and events.
    
    Args:
        host: NetBird API host (e.g., 'api.netbird.io' or 'your-domain.com')
        api_token: API token for authentication
        use_ssl: Whether to use HTTPS (default: True)
        timeout: Request timeout in seconds (default: 30)
        base_path: API base path (default: '/api')
        
    Example:
        >>> client = APIClient(host="api.netbird.io", api_token="your-token")
        >>> peers = client.peers.list()
        >>> users = client.users.list()
        
        # For self-hosted instances
        >>> client = APIClient(
        ...     host="netbird.yourcompany.com:33073",
        ...     api_token="your-token"
        ... )
    """
    
    def __init__(
        self,
        host: str,
        api_token: str,
        use_ssl: bool = True,
        timeout: float = 30.0,
        base_path: str = "/api",
    ) -> None:
        self.host = host.strip().rstrip("/")
        self.base_path = base_path.strip()
        self.use_ssl = use_ssl
        self.timeout = timeout
        
        # Build base URL - if host already has protocol, use as-is
        if self.host.startswith(("http://", "https://")):
            self.base_url = f"{self.host}{self.base_path}"
        else:
            scheme = "https" if use_ssl else "http"
            self.base_url = f"{scheme}://{self.host}{self.base_path}"
        
        # Set up authentication
        self.auth = TokenAuth(api_token)
        
        # Create HTTP client
        self.client = httpx.Client(
            timeout=httpx.Timeout(timeout),
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                **self.auth.get_auth_headers(),
            },
        )
        
        # Lazy-load resource handlers
        self._accounts = None
        self._users = None
        self._tokens = None
        self._peers = None
        self._setup_keys = None
        self._groups = None
        self._networks = None
        self._policies = None
        self._routes = None
        self._dns = None
        self._events = None
    
    @property
    def accounts(self):
        """Access to accounts API endpoints."""
        if self._accounts is None:
            from .resources.accounts import AccountsResource
            self._accounts = AccountsResource(self)
        return self._accounts
    
    @property
    def users(self):
        """Access to users API endpoints."""
        if self._users is None:
            from .resources.users import UsersResource
            self._users = UsersResource(self)
        return self._users
    
    @property
    def tokens(self):
        """Access to tokens API endpoints."""
        if self._tokens is None:
            from .resources.tokens import TokensResource
            self._tokens = TokensResource(self)
        return self._tokens
    
    @property
    def peers(self):
        """Access to peers API endpoints."""
        if self._peers is None:
            from .resources.peers import PeersResource
            self._peers = PeersResource(self)
        return self._peers
    
    @property
    def setup_keys(self):
        """Access to setup keys API endpoints."""
        if self._setup_keys is None:
            from .resources.setup_keys import SetupKeysResource
            self._setup_keys = SetupKeysResource(self)
        return self._setup_keys
    
    @property
    def groups(self):
        """Access to groups API endpoints."""
        if self._groups is None:
            from .resources.groups import GroupsResource
            self._groups = GroupsResource(self)
        return self._groups
    
    @property
    def networks(self):
        """Access to networks API endpoints."""
        if self._networks is None:
            from .resources.networks import NetworksResource
            self._networks = NetworksResource(self)
        return self._networks
    
    @property
    def policies(self):
        """Access to policies API endpoints."""
        if self._policies is None:
            from .resources.policies import PoliciesResource
            self._policies = PoliciesResource(self)
        return self._policies
    
    @property
    def routes(self):
        """Access to routes API endpoints."""
        if self._routes is None:
            from .resources.routes import RoutesResource
            self._routes = RoutesResource(self)
        return self._routes
    
    @property
    def dns(self):
        """Access to DNS API endpoints."""
        if self._dns is None:
            from .resources.dns import DNSResource
            self._dns = DNSResource(self)
        return self._dns
    
    @property
    def events(self):
        """Access to events API endpoints."""
        if self._events is None:
            from .resources.events import EventsResource
            self._events = EventsResource(self)
        return self._events
    
    def _build_url(self, path: str) -> str:
        """Build full URL from path."""
        return urljoin(self.base_url + "/", path.lstrip("/"))
    
    def _handle_response(self, response: Response) -> Any:
        """Handle HTTP response and raise appropriate exceptions."""
        try:
            data = response.json() if response.content else {}
        except ValueError:
            data = {"error": "Invalid JSON response"}
        
        if response.is_success:
            return data
        
        # Extract error message
        error_msg = data.get("message") or data.get("error") or f"HTTP {response.status_code}"
        
        # Map status codes to exceptions
        if response.status_code in [400, 409, 422]:
            raise NetBirdValidationError(error_msg, response.status_code, data)
        elif response.status_code == 401:
            raise NetBirdAuthenticationError(error_msg, response.status_code, data)
        elif response.status_code == 404:
            raise NetBirdNotFoundError(error_msg, response.status_code, data)
        elif response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            retry_seconds = int(retry_after) if retry_after else None
            raise NetBirdRateLimitError(error_msg, response.status_code, data, retry_seconds)
        elif response.status_code >= 500:
            raise NetBirdServerError(error_msg, response.status_code, data)
        else:
            raise NetBirdAPIError(error_msg, response.status_code, data)
    
    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Make a GET request.
        
        Args:
            path: API endpoint path
            params: Query parameters
            
        Returns:
            Response data
        """
        url = self._build_url(path)
        response = self.client.get(url, params=params)
        return self._handle_response(response)
    
    def post(
        self,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Make a POST request.
        
        Args:
            path: API endpoint path
            data: Request body data
            params: Query parameters
            
        Returns:
            Response data
        """
        url = self._build_url(path)
        response = self.client.post(url, json=data, params=params)
        return self._handle_response(response)
    
    def put(
        self,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Make a PUT request.
        
        Args:
            path: API endpoint path
            data: Request body data
            params: Query parameters
            
        Returns:
            Response data
        """
        url = self._build_url(path)
        response = self.client.put(url, json=data, params=params)
        return self._handle_response(response)
    
    def delete(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Make a DELETE request.
        
        Args:
            path: API endpoint path
            params: Query parameters
            
        Returns:
            Response data
        """
        url = self._build_url(path)
        response = self.client.delete(url, params=params)
        return self._handle_response(response)
    
    def close(self) -> None:
        """Close the HTTP client."""
        self.client.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
    
    def __repr__(self) -> str:
        return f"APIClient(host={self.host}, base_url={self.base_url})"