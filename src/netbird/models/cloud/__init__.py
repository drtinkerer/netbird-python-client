"""
Cloud-only models for NetBird API.
"""

from .edr import (
    EDRFalconConfig,
    EDRHuntressConfig,
    EDRIntuneConfig,
    EDRSentinelOneConfig,
)
from .event_streaming import (
    EventStreamingCreate,
    EventStreamingIntegration,
    EventStreamingUpdate,
)
from .idp_scim import SCIMIntegration, SCIMIntegrationCreate, SCIMIntegrationUpdate
from .ingress import (
    IngressPeer,
    IngressPeerCreate,
    IngressPeerUpdate,
    PortAllocation,
    PortAllocationCreate,
    PortAllocationUpdate,
)
from .msp import MSPTenant, MSPTenantCreate, MSPTenantUpdate
from .service import (
    Service,
    ServiceCreate,
    ServiceDomain,
    ServiceDomainCreate,
    ServiceUpdate,
)

__all__ = [
    "Service",
    "ServiceCreate",
    "ServiceUpdate",
    "ServiceDomain",
    "ServiceDomainCreate",
    "PortAllocation",
    "PortAllocationCreate",
    "PortAllocationUpdate",
    "IngressPeer",
    "IngressPeerCreate",
    "IngressPeerUpdate",
    "EDRFalconConfig",
    "EDRHuntressConfig",
    "EDRIntuneConfig",
    "EDRSentinelOneConfig",
    "MSPTenant",
    "MSPTenantCreate",
    "MSPTenantUpdate",
    "EventStreamingIntegration",
    "EventStreamingCreate",
    "EventStreamingUpdate",
    "SCIMIntegration",
    "SCIMIntegrationCreate",
    "SCIMIntegrationUpdate",
]
