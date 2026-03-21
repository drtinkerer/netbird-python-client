"""
Cloud-only resources namespace for NetBird API.

Provides access to cloud-only features via client.cloud.
"""

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .client import APIClient
    from .resources.cloud.edr_falcon import EDRFalconResource
    from .resources.cloud.edr_huntress import EDRHuntressResource
    from .resources.cloud.edr_intune import EDRIntuneResource
    from .resources.cloud.edr_peers import EDRPeersResource
    from .resources.cloud.edr_sentinelone import EDRSentinelOneResource
    from .resources.cloud.event_streaming import EventStreamingResource
    from .resources.cloud.idp_scim import IDPScimResource
    from .resources.cloud.ingress import IngressResource
    from .resources.cloud.invoice import InvoiceResource
    from .resources.cloud.msp import MSPResource
    from .resources.cloud.services import ServicesResource
    from .resources.cloud.usage import UsageResource


class EDRResources:
    """Namespace for EDR (Endpoint Detection & Response) resources."""

    def __init__(self, client: "APIClient") -> None:
        self.client = client
        self._peers: Optional["EDRPeersResource"] = None
        self._falcon: Optional["EDRFalconResource"] = None
        self._huntress: Optional["EDRHuntressResource"] = None
        self._intune: Optional["EDRIntuneResource"] = None
        self._sentinelone: Optional["EDRSentinelOneResource"] = None

    @property
    def peers(self) -> "EDRPeersResource":
        """Access to EDR peer bypass endpoints."""
        if self._peers is None:
            from .resources.cloud.edr_peers import EDRPeersResource

            self._peers = EDRPeersResource(self.client)
        return self._peers

    @property
    def falcon(self) -> "EDRFalconResource":
        """Access to CrowdStrike Falcon EDR integration."""
        if self._falcon is None:
            from .resources.cloud.edr_falcon import EDRFalconResource

            self._falcon = EDRFalconResource(self.client)
        return self._falcon

    @property
    def huntress(self) -> "EDRHuntressResource":
        """Access to Huntress EDR integration."""
        if self._huntress is None:
            from .resources.cloud.edr_huntress import EDRHuntressResource

            self._huntress = EDRHuntressResource(self.client)
        return self._huntress

    @property
    def intune(self) -> "EDRIntuneResource":
        """Access to Microsoft Intune EDR integration."""
        if self._intune is None:
            from .resources.cloud.edr_intune import EDRIntuneResource

            self._intune = EDRIntuneResource(self.client)
        return self._intune

    @property
    def sentinelone(self) -> "EDRSentinelOneResource":
        """Access to SentinelOne EDR integration."""
        if self._sentinelone is None:
            from .resources.cloud.edr_sentinelone import EDRSentinelOneResource

            self._sentinelone = EDRSentinelOneResource(self.client)
        return self._sentinelone


class CloudResources:
    """Namespace for cloud-only NetBird API resources.

    Access via client.cloud.
    """

    def __init__(self, client: "APIClient") -> None:
        self.client = client
        self._services: Optional["ServicesResource"] = None
        self._ingress: Optional["IngressResource"] = None
        self._edr: Optional["EDRResources"] = None
        self._msp: Optional["MSPResource"] = None
        self._invoices: Optional["InvoiceResource"] = None
        self._usage: Optional["UsageResource"] = None
        self._event_streaming: Optional["EventStreamingResource"] = None
        self._idp_scim: Optional["IDPScimResource"] = None

    @property
    def services(self) -> "ServicesResource":
        """Access to reverse proxy services endpoints."""
        if self._services is None:
            from .resources.cloud.services import ServicesResource

            self._services = ServicesResource(self.client)
        return self._services

    @property
    def ingress(self) -> "IngressResource":
        """Access to ingress ports endpoints."""
        if self._ingress is None:
            from .resources.cloud.ingress import IngressResource

            self._ingress = IngressResource(self.client)
        return self._ingress

    @property
    def edr(self) -> "EDRResources":
        """Access to EDR integration endpoints."""
        if self._edr is None:
            self._edr = EDRResources(self.client)
        return self._edr

    @property
    def msp(self) -> "MSPResource":
        """Access to MSP tenant management endpoints."""
        if self._msp is None:
            from .resources.cloud.msp import MSPResource

            self._msp = MSPResource(self.client)
        return self._msp

    @property
    def invoices(self) -> "InvoiceResource":
        """Access to billing invoice endpoints."""
        if self._invoices is None:
            from .resources.cloud.invoice import InvoiceResource

            self._invoices = InvoiceResource(self.client)
        return self._invoices

    @property
    def usage(self) -> "UsageResource":
        """Access to billing usage endpoints."""
        if self._usage is None:
            from .resources.cloud.usage import UsageResource

            self._usage = UsageResource(self.client)
        return self._usage

    @property
    def event_streaming(self) -> "EventStreamingResource":
        """Access to event streaming integration endpoints."""
        if self._event_streaming is None:
            from .resources.cloud.event_streaming import EventStreamingResource

            self._event_streaming = EventStreamingResource(self.client)
        return self._event_streaming

    @property
    def idp_scim(self) -> "IDPScimResource":
        """Access to IDP/SCIM integration endpoints."""
        if self._idp_scim is None:
            from .resources.cloud.idp_scim import IDPScimResource

            self._idp_scim = IDPScimResource(self.client)
        return self._idp_scim
