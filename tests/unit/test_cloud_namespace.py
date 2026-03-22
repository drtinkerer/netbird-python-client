"""Tests for CloudResources and EDRResources namespace lazy-loading."""

import pytest
from unittest.mock import MagicMock

from netbird.cloud import CloudResources, EDRResources
from netbird.resources.cloud.edr_falcon import EDRFalconResource
from netbird.resources.cloud.edr_huntress import EDRHuntressResource
from netbird.resources.cloud.edr_intune import EDRIntuneResource
from netbird.resources.cloud.edr_peers import EDRPeersResource
from netbird.resources.cloud.edr_sentinelone import EDRSentinelOneResource
from netbird.resources.cloud.event_streaming import EventStreamingResource
from netbird.resources.cloud.idp_scim import IDPScimResource
from netbird.resources.cloud.ingress import IngressResource
from netbird.resources.cloud.invoice import InvoiceResource
from netbird.resources.cloud.msp import MSPResource
from netbird.resources.cloud.services import ServicesResource
from netbird.resources.cloud.usage import UsageResource


@pytest.mark.unit
class TestEDRResources:
    def setup_method(self):
        self.mock_client = MagicMock()
        self.edr = EDRResources(self.mock_client)

    @pytest.mark.parametrize(
        "attr,expected_type",
        [
            ("peers", EDRPeersResource),
            ("falcon", EDRFalconResource),
            ("huntress", EDRHuntressResource),
            ("intune", EDRIntuneResource),
            ("sentinelone", EDRSentinelOneResource),
        ],
    )
    def test_property_lazy_loaded(self, attr, expected_type):
        resource = getattr(self.edr, attr)
        assert isinstance(resource, expected_type)
        assert getattr(self.edr, attr) is resource  # cached


@pytest.mark.unit
class TestCloudResources:
    def setup_method(self):
        self.mock_client = MagicMock()
        self.cloud = CloudResources(self.mock_client)

    @pytest.mark.parametrize(
        "attr,expected_type",
        [
            ("services", ServicesResource),
            ("ingress", IngressResource),
            ("edr", EDRResources),
            ("msp", MSPResource),
            ("invoices", InvoiceResource),
            ("usage", UsageResource),
            ("event_streaming", EventStreamingResource),
            ("idp_scim", IDPScimResource),
        ],
    )
    def test_property_lazy_loaded(self, attr, expected_type):
        resource = getattr(self.cloud, attr)
        assert isinstance(resource, expected_type)
        assert getattr(self.cloud, attr) is resource  # cached
