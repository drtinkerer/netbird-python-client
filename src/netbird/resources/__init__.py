"""
NetBird API Resource Handlers

Resource handler classes for interacting with NetBird API endpoints.
"""

from .accounts import AccountsResource
from .dns import DNSResource
from .events import EventsResource
from .groups import GroupsResource
from .networks import NetworksResource
from .peers import PeersResource
from .policies import PoliciesResource
from .routes import RoutesResource
from .setup_keys import SetupKeysResource
from .tokens import TokensResource
from .users import UsersResource

__all__ = [
    "AccountsResource",
    "UsersResource",
    "TokensResource",
    "PeersResource",
    "SetupKeysResource",
    "GroupsResource",
    "NetworksResource",
    "PoliciesResource",
    "RoutesResource",
    "DNSResource",
    "EventsResource",
]
