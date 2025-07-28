"""
NetBird Python Client

Python client library for the NetBird API.
Provides complete access to all NetBird API resources including users, peers,
groups, networks, policies, routes, DNS settings, and more.

Example:
    >>> from netbird import APIClient
    >>> client = APIClient(host="api.netbird.io", api_token="your-token")
    >>> peers = client.peers.list()
    >>> users = client.users.list()
"""

__version__ = "1.0.1"

from .client import APIClient
from .exceptions import (
    NetBirdAPIError,
    NetBirdAuthenticationError,
    NetBirdNotFoundError,
    NetBirdRateLimitError,
    NetBirdServerError,
    NetBirdValidationError,
)

__all__ = [
    "APIClient",
    "NetBirdAPIError",
    "NetBirdAuthenticationError",
    "NetBirdNotFoundError",
    "NetBirdRateLimitError",
    "NetBirdServerError",
    "NetBirdValidationError",
]
