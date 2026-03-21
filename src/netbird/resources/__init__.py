"""
NetBird API Resource Handlers

Resource handler classes for interacting with NetBird API endpoints.
"""

from .accounts import AccountsResource
from .dns import DNSResource
from .dns_zones import DNSZonesResource
from .events import EventsResource
from .geo_locations import GeoLocationsResource
from .groups import GroupsResource
from .identity_providers import IdentityProvidersResource
from .instance import InstanceResource
from .networks import NetworksResource
from .peers import PeersResource
from .policies import PoliciesResource
from .posture_checks import PostureChecksResource
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
    "DNSZonesResource",
    "EventsResource",
    "PostureChecksResource",
    "GeoLocationsResource",
    "IdentityProvidersResource",
    "InstanceResource",
]
