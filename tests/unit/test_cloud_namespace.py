"""Tests for CloudResources and EDRResources namespace lazy-loading."""

import warnings
from unittest.mock import MagicMock

import pytest

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
        self.mock_client.host = "api.netbird.io"
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
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


@pytest.mark.unit
class TestCloudHostWarning:
    def test_no_warning_for_cloud_host(self):
        mock_client = MagicMock()
        mock_client.host = "api.netbird.io"
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            CloudResources(mock_client)
            assert len(w) == 0

    def test_no_warning_for_app_host(self):
        mock_client = MagicMock()
        mock_client.host = "app.netbird.io"
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            CloudResources(mock_client)
            assert len(w) == 0

    def test_warning_for_self_hosted(self):
        mock_client = MagicMock()
        mock_client.host = "netbird.mycompany.com"
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            CloudResources(mock_client)
            assert len(w) == 1
            assert issubclass(w[0].category, UserWarning)
            assert "Cloud endpoints" in str(w[0].message)
            assert "self-hosted" in str(w[0].message)

    def test_warning_for_self_hosted_with_https(self):
        mock_client = MagicMock()
        mock_client.host = "https://netbird.internal:33073"
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            CloudResources(mock_client)
            assert len(w) == 1

    def test_still_works_after_warning(self):
        """Cloud resources should still be usable after warning."""
        mock_client = MagicMock()
        mock_client.host = "netbird.mycompany.com"
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            cloud = CloudResources(mock_client)
        assert isinstance(cloud.services, ServicesResource)
